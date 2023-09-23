from typing import Optional, Union

import matplotlib.pyplot as plt
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Colormap, Normalize


def add_colorbar(
    cax: plt.Axes,
    vmin: float,
    vmax: float,
    cmap: Union[str, Colormap],
    clip=False,
    mappable: Optional[ScalarMappable] = None,
    **kwargs,
):
    fig = cax.figure
    if mappable is None:
        norm = Normalize(vmin, vmax, clip)
        mappable = ScalarMappable(norm, cmap)
    cb = fig.colorbar(mappable, cax=cax, **kwargs)
    return cb
