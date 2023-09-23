import numpy as np


def to_array(a, n: int):
    if isinstance(a, (np.ndarray, list, tuple)):
        return np.asarray(a)

    return np.array([a] * n)


def safe_unpack(a, *, default1=None, default2=None):
    try:
        a1, a2 = a
    except (TypeError, ValueError):
        if default1 is None:
            if default2 is None:
                a1 = a2 = a
            else:
                a1, a2 = a, default2
        else:
            if default2 is None:
                a1, a2 = default1, a
            else:
                a1, a2 = default1, default2

    return a1, a2


def safe_len(a):
    try:
        return len(a)
    except TypeError:
        return 1
