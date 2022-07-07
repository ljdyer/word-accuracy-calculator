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
