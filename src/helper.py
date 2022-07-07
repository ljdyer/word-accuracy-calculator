"""
helper.py

Helper functions for WordAccuracyCalculator class
"""

from typing import Any, Union

import pandas as pd
from tqdm import tqdm as non_notebook_tqdm
from tqdm.notebook import tqdm as notebook_tqdm

Str_or_List_or_Series = Union[str, list, pd.Series]
Int_or_Str = Union[int, str]

REF_OR_HYP_TYPE_ERROR = """
reference and hypothesis parameters must have type list, str, \
or pandas.Series"""


# ====================
def get_tqdm() -> type:
    """Return tqdm.notebook.tqdm if code is being run from a notebook,
    or tqdm.tqdm otherwise"""

    if is_running_from_ipython():
        tqdm_ = notebook_tqdm
    else:
        tqdm_ = non_notebook_tqdm
    return tqdm_


# ====================
def is_running_from_ipython():
    """Determine whether or not the current script is being run from
    a notebook"""

    try:
        # Notebooks have IPython module installed
        from IPython import get_ipython
        return True
    except ModuleNotFoundError:
        return False


# ====================
def display_or_print(obj: Any):
    """'print' or 'display' an object, depending on whether the current
    script is running from a notebook or not."""

    if is_running_from_ipython():
        display(obj)
    else:
        print(obj)


# ====================
def str_or_list_or_series_to_list(
     input_: Str_or_List_or_Series) -> list:
    """Take either a single string, list, or pandas.Series object and
    return a list"""

    if isinstance(input_, str):
        return [input_]
    elif isinstance(input_, pd.Series):
        return input_.to_list()
    elif isinstance(input_, list):
        return input_
    else:
        raise TypeError(REF_OR_HYP_TYPE_ERROR)


# ====================
def create_matrix(m, n):
    """Create an m by n matrix"""

    return [[0 for _ in range(m)] for _ in range(n)]


# ====================
def get_num_edits(words_ref: list, words_hyp: list) -> dict:

    # Create separate matrices for edit distances and backpointers
    n = len(words_hyp) + 1
    m = len(words_ref) + 1
    matrix = create_matrix(m, n)

    # Initialize first row
    for m_ in range(m):
        matrix[0][m_] = m_

    # Initialize first column
    for n_ in range(n):
        matrix[n_][0] = n_

    # Populate remainder of matrix
    for n_ in range(1, n):
        for m_ in range(1, m):

            # Get distances from cells corresponding to each possible edit
            edit_options = [
                matrix[n_-1][m_-1],  # substitution
                matrix[n_-1][m_],  # deletion
                matrix[n_][m_-1]   # insertion
            ]

            # Find the minimum of the three distances
            min_ = min(edit_options)

            # If the words in the reference and hypothesis sentences match,
            # don't make any edits.
            if words_ref[m_-1] == words_hyp[n_-1]:
                matrix[n_][m_] = min_

            # If the words in the reference and hypothesis sentences are
            # different, make an appropriate edit and add one to the distance.
            else:
                matrix[n_][m_] = min_ + 1

    # Get minimum edit distance
    edits = matrix[n-1][m-1]
    
    return edits
