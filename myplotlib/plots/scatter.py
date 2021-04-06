# /usr/bin/python
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter


def scatter(
    x,
    y,
    color=None,
    facealpha=0.8,
    edgealpha=1,
    size=4,
    edgewidth=0.5,
    ax=None,
    **kwargs
):
    """Make a custom scatterplot, with solid outlines and translucent faces.

    Args:
        x (array like): x values
        y (array like): y values
        color (optional): color to use for scatter faces. Defaults to default color.
        ax (matplotlib.axis, optional): Axis to plot on. Defaults to None.
        kwargs: Keyword arguments passed on to matplotlib.pyplot.plot

    Returns:
        matplotlib.axis: Axis with the violinplot.
    """
    if ax is None:
        ax = plt.gca()

    if color is None:
        color = next(ax._get_lines.prop_cycler)["color"]

    # Solid outlines and translucent faces
    scatterArtists = ax.plot(
        x,
        y,
        "o",
        color="none",
        markeredgewidth=edgewidth,
        markersize=size,
        markerfacecolor=colorConverter.to_rgba(color, alpha=facealpha),
        markeredgecolor="none",
        clip_on=False,
        **kwargs
    )
    scatterArtists[0].set_markeredgecolor(
        (0, 0, 0, edgealpha)
    )  # change edge to solid black

    return ax
