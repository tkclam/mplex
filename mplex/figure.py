from matplotlib import pyplot as plt

from mplex.units import convert
from mplex.utils import safe_unpack


class Figure:
    def __init__(self, size, unit="pt", **kwargs):
        self.size = safe_unpack(size)
        size_inch = convert(self.size, unit, "in")
        self._fig = plt.figure(figsize=size_inch, **kwargs)
        self._fig.subplots_adjust(0, 0, 1, 1, 0, 0)
        self.unit = unit
        self.savefig = self._fig.savefig

    @property
    def width_pt(self):
        return convert(self.size[0], self.unit, "pt")

    @property
    def height_pt(self):
        return convert(self.size[1], self.unit, "pt")
