# /usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
from seaborn import violinplot


def violin(
    data, value_name="value", violin_width=0.8, box_width=0.1, palette=None, ax=None
):
    """Make a custom violinplot, with nice inner boxplot.

    Args:
        data (pandas.DataFrame): Data to plot. Each column will be made into one violin.
        violin_width (float, optional): Width of the violins. Defaults to 0.8.
        box_width (float, optional): Width of the boxplot. Defaults to 0.1.
        palette (list, optional): list of colors to use for violins. Defaults to default colors.
        ax (matplotlib.axis, optional): Axis to plot on. Defaults to None.

    Returns:
        matplotlib.axis: Axis with the violinplot.
    """
    if ax is None:
        ax = plt.gca()

    # transform data into long format for seaborn violinplot
    if data.columns.name is None:
        data.columns.name = "variable"
    data_long = pd.melt(data, value_name=value_name)

    # Violinplot
    violinplot(
        x=data.columns.name,
        y=value_name,
        data=data_long,
        palette=palette,
        linewidth=0,
        inner=None,
        scale="width",
        width=violin_width,
        saturation=1,
        ax=ax,
    )

    # Boxplot
    # Matplotlib boxplot uses a different data format (list of arrays)
    boxplot_data = [data[var].values for var in data.columns]

    boxplotArtists = ax.boxplot(
        boxplot_data,
        positions=range(len(boxplot_data)),
        widths=box_width,
        showcaps=False,
        boxprops=dict(linewidth=0.5),
        medianprops=dict(linewidth=0.5, color="black"),
        whiskerprops=dict(linewidth=0.5),
        flierprops=dict(
            marker="o",
            markersize=2,
            markerfacecolor="white",
            markeredgecolor="black",
            markeredgewidth=0.25,
            alpha=0.9,
        ),
        manage_ticks=False,
        patch_artist=True,
    )
    for patch in boxplotArtists["boxes"]:
        patch.set_facecolor("white")

    # Adjust x-limits
    ax.set_xlim(-0.5, len(data.columns) + -0.5)

    return ax
