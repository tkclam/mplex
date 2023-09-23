import matplotlib.pyplot as plt
import numpy as np

from mplex.transforms import get_shifted_trans_axes


def add_scale_bars(
    xy,
    dx=None,
    dy=None,
    xlabel=None,
    ylabel=None,
    xpad=0,
    ypad=0,
    plot_kw=None,
    text_kw=None,
    as_units=True,
    lc="k",
    ax=None,
):
    if ax is None:
        ax = plt.gca()

    if plot_kw is None:
        plot_kw = {}

    if text_kw is None:
        text_kw = {}

    x0, y0 = xy

    line_x = text_x = line_y = text_y = None

    if dx:
        line_x = ax.plot([x0, x0 + dx], [y0, y0], color=lc, **plot_kw)[0]

        if xlabel is not None:
            if as_units:
                xlabel = f"{dx} {xlabel}"

            under = dy and (dy > 0) == (np.subtract(*ax.get_ylim()) < 0)
            va = "top" if under else "bottom"
            transform = get_shifted_trans_axes(
                dy=-xpad if under else xpad, ax=ax, transform="data"
            )
            text_x = ax.text(
                x0 + dx / 2,
                y0,
                xlabel,
                va=va,
                ha="center",
                transform=transform,
                **text_kw,
            )

    if dy:
        line_y = ax.plot([x0, x0], [y0, y0 + dy], color=lc, **plot_kw)[0]

        if ylabel is not None:
            if as_units:
                ylabel = f"{dy} {ylabel}"

            left = dx and (dx > 0) == (np.subtract(*ax.get_xlim()) < 0)
            ha = "right" if left else "left"
            transform = get_shifted_trans_axes(
                dx=-ypad if left else ypad, ax=ax, transform="data"
            )
            rotation = 90 if left else 270
            text_y = ax.text(
                x0,
                y0 + dy / 2,
                ylabel,
                va="center",
                ha=ha,
                transform=transform,
                rotation=rotation,
                **text_kw,
            )

    return dict(line_x=line_x, text_x=text_x, line_y=line_y, text_y=text_y)
