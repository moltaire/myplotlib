import matplotlib.pyplot as plt
import numpy as np
from myplotlib.plots import hist, lm


def pair(
    df,
    n_bins=21,
    ticks=None,
    labels=None,
    limits=None,
    panel_width=1.5,
    panel_height=1.5,
    hist_color="lightgray",
):
    """
    Generates a pair plot for all columns in the given DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the data to plot.
    bins : int, optional
        Number of bins for histograms on the diagonal. Default is 21.
    ticks : dict, optional
        Dictionary of tick positions for each variable.
    labels : dict, optional
        Dictionary of axis labels for each variable.
    limits : dict, optional
        Dictionary of axis limits for each variable.
    panel_width : float, optional
        Width of each subplot panel. Default is 1.5.
    panel_height : float, optional
        Height of each subplot panel. Default is 1.5.
    hist_color : str, optional
        Color of the histogram bars. Defaults to "lightgray".

    Returns:
    --------
    fig, axs : matplotlib.figure.Figure, numpy.ndarray
        The figure and axes array for the pair plot.
    """
    n_vars = len(df.columns)
    var_names = df.columns

    # Create figure and axes grid
    fig, axs = plt.subplots(
        n_vars,
        n_vars,
        figsize=(panel_width * n_vars, panel_height * n_vars),
        sharex="col",
    )

    if labels is None:
        labels = {var: var for var in var_names}
    if ticks is None:
        ticks = {}
    if limits is None:
        limits = {}

    i = 0
    for x, yvar in enumerate(var_names):
        for y, xvar in enumerate(var_names):
            ax = axs[x, y]
            if y > x:
                ax.axis("off")
                continue
            if xvar == yvar:
                # Histogram on the diagonal
                ax = hist(
                    x=df[xvar],
                    ax=ax,
                    color=hist_color,
                    bins=np.linspace(
                        *limits.get(xvar, (df[xvar].min(), df[xvar].max())), n_bins
                    ),
                )
                ax.set_title(labels.get(xvar, xvar))
                ax.set_ylabel("Frequency")
            else:
                # Scatterplot with regression
                ax = lm(x=df[xvar], y=df[yvar], color=f"C{i}", ax=ax)
                ax.set_ylim(*limits.get(yvar, (None, None)))
                if ticks.get(yvar) is not None:
                    ax.set_yticks(ticks[yvar])
                if y == 0:
                    ax.set_ylabel(labels.get(yvar, yvar))
                i += 1
            ax.set_xlim(*limits.get(xvar, (None, None)))

    fig.tight_layout()
    fig.align_ylabels()
    return fig, axs
