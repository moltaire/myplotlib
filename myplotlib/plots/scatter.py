# /usr/bin/python
import matplotlib.pyplot as plt
from matplotlib.colors import colorConverter
from itertools import cycle


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
        # Ensure there's a color cycler on the Axes
        if not hasattr(ax, "_prop_cycle") or ax._prop_cycle is None:
            # Create a new cycle iterator if it doesn't exist
            prop_cycle = plt.rcParams["axes.prop_cycle"]
            ax._prop_cycle = cycle(prop_cycle)

        # Get the next color in the cycle
        color = next(ax._prop_cycle)["color"]

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
