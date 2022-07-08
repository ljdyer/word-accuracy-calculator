"""
main.py

Main module for WordAccuracyCalculator class
"""

import pandas as pd

from wac_helper import (Int_or_Str, Str_or_List_or_Series, display_or_print,
                        get_num_edits, get_tqdm, str_or_list_or_series_to_list)

NON_EQUAL_LENGTH_ERROR = \
    "Hypothesis and reference lists must have equal length."
INIT_COMPLETE_MSG = "Initialisation complete."

tqdm_ = get_tqdm()


# ====================
class WordAccuracyCalculator:

    # ====================
    def __init__(self,
                 reference: Str_or_List_or_Series,
                 hypothesis: Str_or_List_or_Series,
                 calculate_wer_on_init: bool = True):
        """
        Initialize an instance of the WordAccuracyCalculator class

        Required arguments:
        -------------------
        reference:                  Either a single string, or a list or
            Str_or_List_or_Series   pandas.Series object of strings
                                    ('documents') to use as the reference
                                    corpus.
        hypothesis:                 Either a single string, or a list or
            Str_or_List_or_Series   pandas.Series object of strings
                                    ('documents') to use as the hypothesis
                                    corpus.
                                    (Number of documents must be the same
                                    as reference.)

        Optional keyword arguments:
        ---------------------------
        calculate_wer_on_init:      Whether or not to calculate word accuracy
            bool                    for all reference/hypothesis documents
                                    on intiialization. Set to false and access
                                    manually to save time if only looking at
                                    metrics for a subset of documents in a
                                    large corpus.
        """

        self.reference = str_or_list_or_series_to_list(reference)
        self.hypothesis = str_or_list_or_series_to_list(hypothesis)
        if len(self.reference) != len(self.hypothesis):
            raise ValueError(NON_EQUAL_LENGTH_ERROR)
        if calculate_wer_on_init:
            self.get_metrics()
            self.get_metrics_all()
        print(INIT_COMPLETE_MSG)

    # ====================
    def get_metrics(self):
        """Calculate minimum edit distance, reference length, and
        word accuracy for each document in the corpus"""

        print("Calculating word error rates...")
        self.metrics = {}
        for doc_idx in tqdm_(range(len(self.hypothesis))):
            self.metrics[doc_idx] = self.get_metrics_doc(doc_idx)

    # ====================
    def get_metrics_doc(self, doc_idx: int):
        """Calculate minimum edit distance, reference length, and
        word accuracy for a single document"""

        ref = self.reference[doc_idx].strip()
        hyp = self.hypothesis[doc_idx].strip()
        len_ref = len(ref.split())
        num_edits = get_num_edits(ref, hyp)
        acc = self.word_accuracy(len_ref, num_edits)
        return {'len_ref': len_ref, 'num_edits': num_edits,
                'acc': acc}

    # ====================
    def get_metrics_all(self):
        """Calculate minimum edit distance, reference length, and
        word accuracy for the entire corpus"""

        len_ref_all = sum([
            self.metrics[doc_idx]['len_ref']
            for doc_idx in range(len(self.reference))
        ])
        num_edits_all = sum([
            self.metrics[doc_idx]['num_edits']
            for doc_idx in range(len(self.reference))
        ])
        acc_all = self.word_accuracy(len_ref_all, num_edits_all)
        self.metrics['all'] = {'len_ref': len_ref_all,
                               'num_edits': num_edits_all,
                               'acc': acc_all}

    # ====================
    def show_metrics(self, doc_idx: Int_or_Str = 'all'):
        """
        Show minimum edit distance, reference length, and word accuracy
        for either a single document or the entire corpus.

        Optional keyword arguments:
        ---------------------------
        doc_idx: Int_or_Str         Either an integer indicating the index of
                                    the document to show metrics for, or 'all'
                                    to show metrics for all documents in the
                                    corpus (the default behaviour).
        """

        metrics = self.metrics[doc_idx]
        row_labels = [
            'Length of reference (words)',
            'Minimum edit distance (S+D+I)',
            'Word accuracy (%)'
        ]
        metrics_ = [
            f"{metrics['len_ref']:,}",
            f"{metrics['num_edits']:,}",
            f"{(metrics['acc']*100):.3f}%"
        ]
        display_or_print(pd.DataFrame(metrics_, index=row_labels,
                                      columns=['Value']))

    @staticmethod
    def word_accuracy(len_ref: int, num_edits: int) -> float:
        """Calculate word accuracy from reference length and minimum edit
        distance.

        https://en.wikipedia.org/wiki/Word_error_rate"""

        return (len_ref - num_edits) / len_ref
