# /usr/bin/python

import matplotlib.pyplot as plt


def hist(x, ax=None, **kwargs):
    """Make a custom histogram.

    Args:
        x (array like): x values
        ax (matplotlib.axis, optional): Axis to plot on. Defaults to current axis.
        **kwargs: Keyword arguments passed onto plt.hist function.

    Returns:
        matplotlib.axis: Axis with the histogram.
    """
    if ax is None:
        ax = plt.gca()

    ax.hist(x, linewidth=0.75, edgecolor="white", **kwargs)

    return ax
