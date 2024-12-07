# /usr/bin/python

import matplotlib.pyplot as plt
import pandas as pd
from seaborn import violinplot


def violin(
    data, value_name="value", violin_width=0.8, box_width=0.1, color=None, ax=None
):
    """
    Create a custom violin plot with an inner boxplot.

    This function combines a violin plot with an inner boxplot for enhanced visualization.
    The violins represent the distribution of the data, while the inner boxplot shows
    the summary statistics (median, quartiles).

    Parameters
    ----------
    data : pandas.DataFrame
        The data to plot. Each column will be made into one violin.

    value_name : str, optional
        The name of the variable for the violin plot values. Defaults to "value".

    violin_width : float, optional
        The width of the violins. Default is 0.8.

    box_width : float, optional
        The width of the boxplot. Default is 0.1.

    color : str, optional
        The color to use for the violins. If None, the default seaborn color palette is used. Default is None.

    ax : matplotlib.axes.Axes, optional
        The axis to plot the violin plot on. If None, the current axis is used. Default is None.

    Returns
    -------
    matplotlib.axes.Axes
        The axis with the violin plot and inner boxplot.

    Example
    -------
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Example data
    data = pd.DataFrame({
        'Model A': np.random.normal(0, 1, 100),
        'Model B': np.random.normal(1, 1.5, 100),
        'Model C': np.random.normal(2, 2, 100),
    })

    # Create a violin plot
    fig, ax = plt.subplots()
    violin(data, ax=ax, violin_width=0.9, box_width=0.15, color='lightblue')
    plt.show()
    """
    if ax is None:
        ax = plt.gca()

    # Transform data into long format for seaborn violinplot
    if data.columns.name is None:
        data.columns.name = "variable"
    data_long = pd.melt(data, value_name=value_name)

    if color is None:
        hue = data.columns.name
    else:
        hue = None

    # Violin plot
    violinplot(
        x=data.columns.name,
        y=value_name,
        data=data_long,
        hue=hue,
        linewidth=0,
        inner=None,
        density_norm="width",
        width=violin_width,
        saturation=1,
        ax=ax,
        color=color,
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
