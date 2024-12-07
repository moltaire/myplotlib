#!/usr/bin/python
import matplotlib.pyplot as plt


def hTextLine(
    text,
    x0,
    x1,
    y,
    ax=None,
    linewidth=0.5,
    lineTextGap=0,
    fontsize=5,
    coord_type="data",
    **kwargs,
):
    """Add a horizontal line and some text. Good for p-values and similar stuff.

    Args:
        text (str): Text.
        x0 (float): Line start value.
        x1 (float): Line end value.
        y (float): Height of the line.
        ax (matplotlib.axis, optional): Axis to annotate. Defaults to current axis.
        linewidth (float, optional): Linewidth. Defaults to 0.5.
        lineTextGap (float, optional): Distance between the line and the text. Defaults to 0.02.
        fontsize (int, optional): Fontsize. Defaults to 5.

    Returns:
        matplotlib.axis: Annotated axis.
    """

    if ax is None:
        ax = plt.gca()

    if coord_type == "axes":
        transform = ax.transAxes  # Axis-relative coordinates
    elif coord_type == "data":
        transform = ax.transData  # Data coordinates (default behavior)
    else:
        raise ValueError("coord_type must be 'data' or 'axes'.")

    ax.hlines(
        y,
        x0,
        x1,
        linewidth=linewidth,
        clip_on=False,
        color="black",
        transform=transform,
    )
    ax.text(
        x=(x0 + x1) / 2,
        y=y + lineTextGap,
        s=text,
        ha="center",
        va="bottom",
        fontsize=fontsize,
        transform=transform,
        **kwargs,
    )
    return ax


def format_p(p, lower_cutoff=0.001, upper_cutoff=0.1, ns=False):
    """
    Plots a p-value into a nicer string, based on some cutoffs.
    """
    if p < lower_cutoff:
        return "p < 0.001"
    elif p >= upper_cutoff:
        if ns:
            return "n.s."
        else:
            return f"p = {p:.2f}"
    else:
        return f"p = {p:.3f}"
