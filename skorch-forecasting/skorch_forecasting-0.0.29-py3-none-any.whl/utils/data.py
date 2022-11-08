import inspect

import numpy as np
import pandas as pd


def empty_ndarray(shape):
    return np.ndarray(shape=shape)


def safe_hstack(arrays):
    """If :meth:`np.stack` raises TypeError, converts all arrays to object
    dtype and tries again.

    Parameters
    ----------
    arrays : sequence of ndarrays
        The arrays must have the same shape along all but the second axis,
        except 1-D arrays which can be any length.

    Returns
    -------
    stacked : ndarray
        The array formed by stacking the given arrays.
    """
    try:
        return np.hstack(arrays)
    except TypeError:
        obj_arrays = [arr.astype(object) for arr in arrays]
        return np.hstack(obj_arrays)


def series_to_2d(series):
    return series.values.reshape(-1, 1)


def numpy_2d_to_pandas(arrays, columns=None, dtypes=None):
    """Converts collection of 2-D numpy arrays to a single pandas DataFrame.

    Parameters
    ----------
    arrays : list of 2-D numpy arrays

    columns : array-like, default=None
        Column labels to use for resulting frame when data does not have them,
        defaulting to RangeIndex(0, 1, 2, …, n).

    dtypes : data type, or dict of column name -> data type, default=None

    Returns
    -------
    pandas_df : pd.DataFrame
    """
    pandas_df = pd.DataFrame(np.vstack(arrays), columns=columns)
    if dtypes is not None:
        return pandas_df.astype(dtype=dtypes)
    return pandas_df


def safe_math_eval(string):
    """Evaluates simple math expression

    Since built-in eval is dangerous, this function limits the possible
    characters to evaluate.

    Parameters
    ----------
    string : str

    Returns
    -------
    evaluated ``string`` : float
    """
    allowed_chars = "0123456789+-*(). /"
    for char in string:
        if char not in allowed_chars:
            raise ValueError("Unsafe eval character: {}".format(char))
    return eval(string, {"__builtins__": None}, {})


def loc_group(X, group_ids, id):
    """Auxiliary for locating rows in dataframes with one or multiple group_ids

    Parameters
    ----------
    X : pd.DataFrame
        Dataframe to filter

    group_ids: tuple
        Tuple of columns names

    id : tuple
        Id of the wanted group

    Returns
    -------
    pd.DataFrame
    """
    # Broadcasted numpy comparison
    return X[(X[group_ids].values == id).all(1)].copy()


def add_prefix(d, prefix, sep='__'):
    """Adds prefix to keys in d.

    Parameters
    ----------
    d : dict

    prefix : str
        Prefix to be added to each key in d

    sep : str
        Separator between prefix and original key

    Returns
    -------
    dict
    """
    return {prefix + sep + k: v for k, v in d.items()}


def get_init_params(cls):
    """Inspects given class using the inspect package and extracts the
    parameter attribute from its signature

    Parameters
    ----------
    cls : class

    Returns
    -------
    init params : list
    """
    if not inspect.isclass(cls):
        raise ValueError('cls param has to be of type class. Instead '
                         'got {}'.format(type(cls)))
    return inspect.signature(cls.__init__).parameters
