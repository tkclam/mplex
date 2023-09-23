from typing import Tuple, Union

import numpy as np
from matplotlib import pyplot as plt

import mplex.axes
from mplex import core
from mplex.annotate import add_bar
from mplex.axes import (
    add_axes,
    get_col_span,
    get_row_span,
    remove_ticklabels_trailing_zeros,
    set_visible,
)
from mplex.colorbar import add_colorbar


class AxArray:
    def __init__(self, axs):
        if isinstance(axs, plt.Axes):
            axs = [axs]

        self._axs = np.asarray(list(axs))

    def __iter__(self):
        return iter(self._axs.ravel())

    def __getitem__(self, item):
        return self._axs.__getitem__(item)

    def __getattr__(self, name: str):
        a = np.array([getattr(ax, name) for ax in self._axs.ravel()], object).reshape(
            (*self._axs.shape, -1)
        )

        if all(map(callable, a.ravel())):
            return lambda *args, **kwargs: np.array(
                [i(*args, **kwargs) for i in a.ravel()]
            ).reshape((*self._axs.shape, -1))

        return a

    @property
    def axs(self):
        return self._axs

    def item(self):
        return self._axs.item()

    def make_ax(self, sharex=None, sharey=None, behind=True):
        axs = list(self)
        gs = axs[0].get_gridspec()
        fig: plt.Figure = axs[0].figure

        assert all(ax.get_gridspec() is gs for ax in axs)
        assert all(ax.figure is fig for ax in axs)

        row0, row1 = get_row_span(*axs)
        col0, col1 = get_col_span(*axs)

        if sharex is True:
            sharex = axs[0]

        if sharey is True:
            sharey = axs[0]

        kwargs = dict()

        if behind:
            kwargs["zorder"] = min(ax.zorder for ax in axs) - 1

        ax: plt.Axes = fig.add_subplot(
            gs[row0:row1, col0:col1], sharex=sharex, sharey=sharey, **kwargs
        )
        ax.axis("off")
        return ax

    def add_axes(
        self,
        rect,
        unit: Union[str, Tuple[str, str], Tuple[str, str, str, str]] = "pt",
        loc0="r",
        loc1=None,
        pad=0,
        pad_unit="pt",
        relocate_ticks=False,
        **kwargs,
    ):
        temp_ax = self.make_ax()

        ax = add_axes(
            rect,
            unit,
            loc0,
            loc1,
            pad,
            pad_unit,
            relocate_ticks,
            ax=temp_ax,
            **kwargs,
        )

        temp_ax.remove()

        return ax

    def add_colorbar(
        self,
        vmin=0,
        vmax=1,
        cmap="viridis",
        mappable=None,
        length=100,
        thick=10,
        pad=10,
        pad_unit="pt",
        orientation="v",
        loc0="r",
        loc1="l",
        clip=False,
        length_unit="pt",
        thick_unit="pt",
        ax_kwargs=None,
        **kwargs,
    ):
        orientation = core.get_orientation(orientation)

        if orientation == "vertical":
            size = thick, length
            unit = thick_unit, length_unit
        else:
            size = length, thick
            unit = length_unit, thick_unit

        if ax_kwargs is None:
            ax_kwargs = dict()

        cax = self.add_axes(
            size, unit, loc0, loc1, pad=pad, pad_unit=pad_unit, **ax_kwargs
        )
        cb = add_colorbar(
            cax,
            vmin,
            vmax,
            cmap,
            clip,
            mappable=mappable,
            orientation=orientation,
            **kwargs,
        )
        return cb

    def set_visible(self, sides=None, *, spines=None, ticks=None, ticklabels=None):
        for ax in self:
            set_visible(sides, spines=spines, ticks=ticks, ticklabels=ticklabels, ax=ax)

    def set_tight_bounds(self, x=True, y=True):
        for ax in self:
            mplex.axes.set_tight_bounds(x, y, ax=ax)

    def set_tick_direction(self, directions: str):
        for ax in self:
            mplex.axes.set_tick_direction(directions, ax=ax)

    def remove_ticklabels_trailing_zeros(self, which="both"):
        for ax in self:
            remove_ticklabels_trailing_zeros(which, ax=ax)


class AxArray2D(AxArray):
    def __init__(self, axs):
        if isinstance(axs, plt.Axes):
            axs = [[axs]]

        super().__init__(axs)
        assert self._axs.ndim == 2

    def remove_inner_ticklabels(
        self, sharex="col", sharey="row", ticklabels_sides=("left", "bottom")
    ):
        sharex = core.get_share_ax_name(sharex)
        sharey = core.get_share_ax_name(sharey)
        ticklabels_sides = core.get_side_names(ticklabels_sides)

        axs = self._axs
        assert axs.ndim == 2

        if sharex in ("all", "col"):
            if "bottom" in ticklabels_sides:
                for ax in axs[:-1].ravel():
                    ax.tick_params(labelbottom=False)
            if "top" in ticklabels_sides:
                for ax in axs[1:].ravel():
                    ax.tick_params(labeltop=False)

        if sharey in ("all", "row"):
            if "left" in ticklabels_sides:
                for ax in axs[:, 1:].ravel():
                    ax.tick_params(labelleft=False)
            if "right" in ticklabels_sides:
                for ax in axs[:, :-1].ravel():
                    ax.tick_params(labelright=False)

    def add_bar(self, fro=0, to=-1, side="t", pad=0, **kwargs):
        add_bar(self._axs, fro, to, side, pad, **kwargs)
