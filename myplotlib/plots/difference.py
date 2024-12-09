import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import TwoSlopeNorm
from scipy.stats import norm as normal


def difference(
    y0,
    y1,
    bins=20,
    vmin=None,
    vmax=None,
    cmap=plt.cm.coolwarm,
    jitter=0.02,
    ci_alpha=0.05,
):
    """
    Plot within-subject changes with a histogram of difference scores and individual change lines.

    Parameters:
    ----------
    y0 : array-like or pandas Series
        Baseline values for subjects.
    y1 : array-like or pandas Series
        Follow-up values for subjects.
    bins : int or array-like, optional, default=20
        Number of bins for the histogram of difference scores, or an array specifying bin edges.
    vmin : float, optional, default=None
        Minimum value for the colormap range. If None, it is inferred from the data.
    vmax : float, optional, default=None
        Maximum value for the colormap range. If None, it is inferred from the data.
    cmap : matplotlib.colors.Colormap, optional, default=plt.cm.coolwarm
        Colormap used for visualizing differences.
    jitter : float, optional, default=0.02
        Standard deviation for random jitter applied to x-coordinates in the line plot.
    ci_alpha : float, optional, default=0.05
        Significance level for the confidence intervals around mean values and mean difference.
        Determines the size of error bars (e.g., 0.05 for 95% confidence intervals).

    Returns:
    -------
    fig, axs : tuple
        Matplotlib figure and axes objects for further customization or saving.

    Notes:
    -----
    - The lower panel visualizes within-subject changes with individual lines and grand mean changes.
    - The upper panel shows a histogram of difference scores, color-coded by magnitude and direction.
    """

    # Set up normalization for colormap
    norm = TwoSlopeNorm(vmin=vmin, vcenter=0, vmax=vmax)

    # Calculate differences
    diffs = y1 - y0
    if vmin is None:
        vmin = diffs.min()
    if vmax is None:
        vmax = diffs.max()

    # Create figure and axes
    fig, axs = plt.subplots(2, 1, gridspec_kw={"height_ratios": [1, 3]})

    # Lower panel: Within-subject change lines
    ax = axs[1]
    xs = np.array([0, 1])

    # Individual subject lines
    for y0i, y1i in zip(y0, y1):
        diff = y1i - y0i
        color = cmap(norm(diff))
        ax.plot(
            xs + np.random.normal(scale=jitter),
            [y0i, y1i],
            alpha=0.1,
            marker="o",
            markeredgewidth=0.1,
            markersize=3,
            color=color,
            zorder=1,
            clip_on=False,
        )

    # Grand mean line
    y0mean = np.mean(y0)
    y0sem = np.std(y0) / np.sqrt(len(y0))
    y1mean = np.mean(y1)
    y1sem = np.std(y1) / np.sqrt(len(y1))
    meandiff = np.mean(diffs)
    meandiff_sem = np.std(diffs) / np.sqrt(len(diffs))
    meancolor = cmap(norm(meandiff))
    ## Error bars
    zcrit = normal.ppf(1 - ci_alpha / 2)
    for x, mean, sem in zip(xs, [y0mean, y1mean], [y0sem, y1sem]):
        ax.vlines(
            x,
            mean - zcrit * sem,
            mean + zcrit * sem,
            color="black",
            lw=0.75,
            zorder=2,
        )

    ax.plot(
        xs,
        [y0mean, y1mean],
        "d-",
        color="black",
        markerfacecolor=meancolor,
        markeredgewidth=0.5,
        markersize=5,
        zorder=3,
    )

    # Lower panel settings
    ax.set_xlim(-0.2, 1.25)
    ax.set_xticks(xs)
    y0ticklabel = y0.name if isinstance(y0, pd.Series) else "y0"
    y1ticklabel = y1.name if isinstance(y1, pd.Series) else "y1"
    ax.set_xticklabels([y0ticklabel, y1ticklabel])
    ax.set_ylabel("Value")

    # Upper panel: Histogram of differences
    ax = axs[0]
    if isinstance(bins, int):
        bins = np.linspace(vmin, vmax, n_bins)
    n, bins, patches = ax.hist(diffs, bins=bins, linewidth=0.5, edgecolor="white")

    ## Add mean difference
    ax.plot(
        meandiff,
        0,
        marker="d",
        markersize=5,
        markerfacecolor=meancolor,
        markeredgewidth=0.5,
        clip_on=False,
        zorder=9,
    )
    ax.hlines(
        0,
        meandiff - zcrit * meandiff_sem,
        meandiff + zcrit * meandiff_sem,
        color="black",
        linewidth=3,
        zorder=2,
    )

    # Color the bins
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    colors = cmap(norm(bin_centers))
    for patch, color in zip(patches, colors):
        patch.set_facecolor(color)

    # Upper panel settings
    ax.set_ylabel("Freq.")
    ax.set_xlim(vmin, vmax)
    ax.set_xlabel("Difference", labelpad=0.5)

    # Align and adjust layout
    fig.align_ylabels()
    fig.tight_layout()

    return fig, axs