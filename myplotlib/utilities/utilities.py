#!/usr/bin/python
"""
This script contains plot utilities
"""

import matplotlib
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


def break_after_nth_tick(ax, n, axis="x", occHeight=None, occWidth=None, where=0.5):
    """Visually break an axis x or y spine after the nth tick.
    Places a white occluding box and black diagonals onto the axis.
    Axis ticklabels must be changed manually.

    Parameters
    ----------
    ax : matplotlib.axis
        Axis object to plot on
    n : int
        Index of tick after which the break should be made
    axis : str, optional
        must be "x" or "y", by default "x"
    occHeight : float, optional
        Height of the occluding box, by default a third of the space between ticks
    occWidth : float, optional
        Width of the occluding box, by default a third of the space between ticks
    where : float, optional
        Fine tuning of occluder position between ticks, by default 0.5 (right in the middle)
    
    Returns
    -------
    matplotlib.axis
        Axis object with occluder

    Raises
    ------
    ValueError
        If axis keyword not in ['x', 'y']
    """
    # Save current x and y limits
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Determine occluder position
    if axis == "x":
        occPos = (
            ax.get_xticks()[n] + where * (ax.get_xticks()[n + 1] - ax.get_xticks()[n]),
            ylim[0],
        )
        if occHeight is None:
            occHeight = 1 / 10 * (ax.get_yticks()[n + 1] - ax.get_yticks()[n])
        if occWidth is None:
            occWidth = 1 / 3 * (ax.get_xticks()[n + 1] - ax.get_xticks()[n])
    elif axis == "y":
        occPos = (
            xlim[0],
            ax.get_yticks()[n] + where * (ax.get_yticks()[n + 1] - ax.get_yticks()[n]),
        )
        if occHeight is None:
            occHeight = 1 / 3 * (ax.get_yticks()[n + 1] - ax.get_yticks()[n])
        if occWidth is None:
            occWidth = 1 / 10 * (ax.get_xticks()[n + 1] - ax.get_xticks()[n])
    else:
        raise ValueError(f"'which' must be 'x' or 'y' (is {which})")

    # Build occlusion rectangles
    occBox = matplotlib.patches.Rectangle(
        (occPos[0] - occWidth / 2, occPos[1] - occHeight / 2),
        width=occWidth,
        height=occHeight,
        color="white",
        clip_on=False,
        zorder=8,
    )
    ax.add_patch(occBox)

    # Breaker lines
    if axis == "x":
        ax.scatter(
            x=[occPos[0] - occWidth / 2, occPos[0] + occWidth / 2],
            y=[ylim[0], ylim[0]],
            marker=(2, 0, -45),
            color="black",
            s=18,
            linewidth=0.75,
            clip_on=False,
            zorder=9,
        )
    elif axis == "y":
        ax.scatter(
            x=[xlim[0], xlim[0]],
            y=[occPos[1] - occHeight / 2, occPos[1] + occHeight / 2],
            marker=(2, 0, -45),
            color="black",
            s=18,
            linewidth=0.75,
            clip_on=False,
            zorder=9,
        )

    # Restore x and y limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    return ax
