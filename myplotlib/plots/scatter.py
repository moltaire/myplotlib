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
    """
    Create a custom scatter plot with solid outlines and translucent faces.

    This function plots a scatter plot where the data points have solid black outlines and
    translucent faces. It allows customization of point size, transparency, edge color, and more.

    Parameters
    ----------
    x : array-like
        The x-values of the scatter plot.
    
    y : array-like
        The y-values of the scatter plot.
    
    color : str, optional
        The color to use for the face of the scatter points. If None, the default color from 
        the current color cycle is used. Default is None.
    
    facealpha : float, optional
        The transparency level of the scatter points. A value between 0 (fully transparent) 
        and 1 (fully opaque). Default is 0.8.
    
    edgealpha : float, optional
        The transparency level of the scatter point edges. A value between 0 (fully transparent) 
        and 1 (fully opaque). Default is 1.
    
    size : int, optional
        The size of the scatter points. Default is 4.
    
    edgewidth : float, optional
        The width of the scatter point edges. Default is 0.5.
    
    ax : matplotlib.axes.Axes, optional
        The axes to plot the scatter plot on. If None, the current axes are used. Default is None.
    
    kwargs : keyword arguments
        Additional keyword arguments passed on to `matplotlib.pyplot.plot` for customization 
        of the scatter plot (e.g., `label` for legend, `alpha` for overall transparency, etc.).

    Returns
    -------
    matplotlib.axes.Axes
        The axes with the scatter plot.
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
