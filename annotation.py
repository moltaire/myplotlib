#!/usr/bin/python
import matplotlib.pyplot as plt


def hTextLine(
    text, x0, x1, y, ax=None, linewidth=0.5, lineTextGap=0.1, fontsize=5, **kwargs
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

    ax.hlines(y, x0, x1, linewidth=linewidth, clip_on=False)
    ax.text(
        x=(x0 + x1) / 2,
        y=y + lineTextGap,
        s=text,
        ha="center",
        va="bottom",
        fontsize=fontsize,
        **kwargs
    )
    return ax

