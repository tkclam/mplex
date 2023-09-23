from fractions import Fraction
from numbers import Real
from typing import Any

import numpy as np

_to_inch = {
    "pt": Fraction(1 / 72),
    "inch": Fraction(1),
    "in": Fraction(1),
    "cm": Fraction(50, 127),
}


def convert(x, fro: str, to: str) -> Any:
    if isinstance(x, Real):
        return float(_to_inch[fro] / _to_inch[to] * x)
    else:
        return (_to_inch[fro] / _to_inch[to] * np.asarray(x)).astype(float)
