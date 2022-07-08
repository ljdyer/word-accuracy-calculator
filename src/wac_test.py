"""
test.py

Basic tests for WordAccuracyCalculator class
"""

from wac_main import WordAccuracyCalculator


if __name__ == "__main__":

    reference = [
        'This is a sentence.',
        'This is the second sentence.',
        'This is Sentence 3.'
    ]
    hypothesis = [
        'This is a sentence...',
        'This the second sentence.',
        'This isn\t Sentence 7.'
    ]
    wac = WordAccuracyCalculator(
        reference, hypothesis
    )

    assert wac.metrics[0]['len_ref'] == 4
    # 'sentence.' -> 'sentence...' ==> 1 * substitution = 1
    assert wac.metrics[0]['num_edits'] == 1
    assert wac.metrics[0]['acc'] == 0.75

    assert wac.metrics[1]['len_ref'] == 5
    # 'is' removed ==> 1 * deletion = 1
    assert wac.metrics[1]['num_edits'] == 1
    assert wac.metrics[1]['acc'] == 0.8

    assert wac.metrics[2]['len_ref'] == 4
    # 'is' -> 'isn\'t', '3.' -> '7.'
    # ==> 2 * substitution = 2
    assert wac.metrics[2]['num_edits'] == 2
    assert wac.metrics[2]['acc'] == 0.5

    assert wac.metrics['all']['len_ref'] == 13
    assert wac.metrics['all']['num_edits'] == 4
    # (13-4)/13 = 9/13 = 0.69
    assert round(wac.metrics['all']['acc'], 2) == 0.69

    print("All tests passed.")
