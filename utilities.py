#!/usr/bin/python
"""
This script contains plot utilities
"""

import matplotlib.pyplot as plt
from matplotlib import cycler
import string
from itertools import cycle
from six.moves import zip


def set_mpl_defaults(matplotlib):
    """This function updates the matplotlib library to adjust 
    some default plot parameters

    Parameters
    ----------
    matplotlib : matplotlib instance
    
    Returns
    -------
    matplotlib
        matplotlib instance
    """
    params = {
        "font.size": 6,
        "axes.labelsize": 6,
        "axes.titlesize": 6,
        "xtick.labelsize": 6,
        "ytick.labelsize": 6,
        "figure.titlesize": 6,
        "legend.fancybox": True,
        "legend.fontsize": 6,
        "legend.handletextpad": 0.25,
        "legend.handlelength": 1,
        "legend.labelspacing": 0.7,
        "legend.columnspacing": 1.5,
        "legend.edgecolor": (0, 0, 0, 1),  # solid black
        "patch.linewidth": 0.75,
        "figure.dpi": 300,
        "figure.figsize": (2, 2),
        "lines.linewidth": 1,
        "axes.linewidth": 0.75,
        "axes.spines.right": False,
        "axes.spines.top": False,
        "axes.prop_cycle": cycler(
            "color",
            [
                "slategray",
                "darksalmon",
                "mediumaquamarine",
                "indianred",
                "orchid",
                "paleturquoise",
                "tan",
                "lightpink",
            ],
        ),
        "lines.markeredgewidth": 1,
        "lines.markeredgecolor": "black",
    }

    # Update parameters
    matplotlib.rcParams.update(params)

    return matplotlib


def cm2inch(*tupl):
    """This function converts cm to inches

    Obtained from: https://stackoverflow.com/questions/14708695/
    specify-figure-size-in-centimeter-in-matplotlib/22787457
    
    Parameters
    ----------
    tupl : tuple
        Size of plot in cm
    
    Returns
    -------
    tuple
        Converted image size in inches
    """
    inch = 2.54
    if isinstance(tupl[0], tuple):
        return tuple(i / inch for i in tupl[0])
    else:
        return tuple(i / inch for i in tupl)


def label_axes(fig, labels=None, loc=None, **kwargs):
    """
    From https://gist.github.com/tacaswell/9643166
    Walks through axes and labels each.
    kwargs are collected and passed to `annotate`
    Parameters
    ----------
    fig : Figure
         Figure object to work on
    labels : iterable or None
        iterable of strings to use to label the axes.
        If None, lower case letters are used.
    loc : len=2 tuple of floats
        Where to put the label in axes-fraction units
    """
    if labels is None:
        labels = string.ascii_lowercase

    # re-use labels rather than stop labeling
    labels = cycle(labels)
    if loc is None:
        loc = (-0.3, 1)
    for ax, lab in zip(fig.axes, labels):
        ax.annotate(lab, xy=loc, xycoords="axes fraction", **kwargs)
