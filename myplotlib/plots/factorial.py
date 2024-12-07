import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from itertools import groupby


def factorial_heatmap(
    df,
    row_factors,
    col_factors,
    value_var,
    factor_labels={},
    level_labels={},
    cmap="viridis_r",
    ax=None,
    ylabel_rotation=0,
    xlabel_rotation=0,
    pad_label_bar=0.2,
    pad_per_factor=1.5,
    pad_colorbar=0.05,
):
    """
    Create a heatmap for visualizing interactions between categorical factors and a numerical value.

    This function generates a heatmap where the rows and columns correspond to categorical factors,
    and the cell values represent a numerical variable. It also includes labeled bars for factor levels
    along both axes and a colorbar indicating the range of the value variable.

    Parameters
    ----------
    df : pd.DataFrame
        A pandas DataFrame containing the categorical factor columns and the numerical value variable.

    row_factors : list of str
        A list of column names in `df` that determine the rows of the heatmap. Each factor corresponds to
        a categorical variable.

    col_factors : list of str
        A list of column names in `df` that determine the columns of the heatmap. Each factor corresponds
        to a categorical variable.

    value_var : str
        The name of the column in `df` that contains the numerical values to be visualized in the heatmap.

    factor_labels : dict, optional
        A dictionary that maps factor column names to custom labels for display. Default is an empty dictionary.

    level_labels : dict, optional
        A dictionary of dictionaries, each mapping factor level names to custom labels. Default is an empty dictionary.

    cmap : str, optional
        The colormap to use for the heatmap. This is passed to `matplotlib.pyplot.imshow`. Default is "viridis_r",
        but options like "inferno", "magma", and others are available.

    ax : matplotlib.axes.Axes, optional
        The axes to plot on. If None, the current axes will be used. Default is None.

    ylabel_rotation : float, optional
        The rotation angle of the y-axis labels. Default is 0 degrees (horizontal).

    xlabel_rotation : float, optional
        The rotation angle of the x-axis labels. Default is 0 degrees (horizontal).

    pad_label_bar : float, optional
        The padding between factor labels and the bars marking factor levels. Default is 0.2.

    pad_per_factor : float, optional
        The vertical or horizontal spacing between factor level bars. Default is 1.5.

    pad_colorbar : float, optional
        The padding between the heatmap and the colorbar. Default is 0.05.

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the plotted heatmap, including factor labels, factor level bars, and colorbar.
    """
    all_factors = row_factors + col_factors
    default_factor_labels = {factor: factor for factor in all_factors}
    factor_labels = {**default_factor_labels, **factor_labels}
    default_level_labels = {
        factor_labels[factor]: {
            level: f"{factor_labels[factor]}={level}" for level in df[factor].unique()
        }
        for factor in all_factors
    }
    level_labels = {**default_level_labels, **level_labels}

    if ax is None:
        ax = plt.gca()

    n_row = np.prod([df[row_factor].unique().size for row_factor in row_factors])
    n_col = np.prod([df[col_factor].unique().size for col_factor in col_factors])

    df_sorted = df.sort_values(row_factors + col_factors)
    values = df_sorted[value_var].values.reshape(n_row, n_col)

    # Make the heatmap
    im = plt.imshow(values, cmap=cmap)

    # x_labels = levels from last col_factor
    ax.set_xlabel(factor_labels[col_factors[-1]])
    ax.set_xticks(np.arange(n_col))
    ax.set_xticklabels(df_sorted[col_factors[-1]][:n_col], rotation=xlabel_rotation)
    ax.set_xlim(-0.5, n_col - 0.5)

    # other factors across columns:
    # from second-to-last to first, so that the first factor is the uppermost level
    for f, col_factor in enumerate(col_factors[-2::-1]):
        levels = df_sorted[col_factor].values[:n_col]
        bar_y = n_row - 0.25 + f * pad_per_factor

        # Identify blocks of same levels: https://stackoverflow.com/a/6352456
        index = 0
        for level, block in groupby(levels):
            length = sum(1 for i in block)
            bar_xmin = index
            bar_xmax = index + length - 1
            index += length
            ax.plot(
                [bar_xmin - 0.4, bar_xmax + 0.4],
                [bar_y, bar_y],
                linewidth=0.75,
                color="k",
                clip_on=False,
            )
            ax.annotate(
                level_labels[factor_labels[col_factor]][level],
                xy=(bar_xmin + (bar_xmax - bar_xmin) / 2, bar_y + pad_label_bar),
                xycoords="data",
                ha="center",
                va="bottom",
                ma="center",
                annotation_clip=False,
            )

    # y_labels = levels from last row_factor
    ax.set_ylabel(factor_labels[row_factors[-1]])
    ax.set_yticks(np.arange(n_row))
    ax.set_yticklabels(df_sorted[row_factors[-1]][::n_col], rotation=ylabel_rotation)
    ax.set_ylim(-0.5, n_row - 0.5)

    # other factors across rows:
    # from second-to-last to first, so that the first factor is the uppermost level
    for f, row_factor in enumerate(row_factors[-2::-1]):
        levels = df_sorted[row_factor].values[::n_col][:n_row]
        bar_x = n_col - 0.25 + f * pad_per_factor

        index = 0
        for level, block in groupby(levels):
            length = sum(1 for i in block)
            bar_ymin = index
            bar_ymax = index + length - 1
            index += length
            ax.plot(
                [bar_x, bar_x],
                [bar_ymin - 0.4, bar_ymax + 0.4],
                linewidth=0.75,
                color="k",
                clip_on=False,
            )
            ax.annotate(
                level_labels[factor_labels[row_factor]][level],
                xy=(bar_x + pad_label_bar, bar_ymin + (bar_ymax - bar_ymin) / 2),
                xycoords="data",
                rotation=270,
                ha="left",
                va="center",
                ma="center",
                annotation_clip=False,
            )

    # colorbar legend
    cb = plt.colorbar(im, pad=len(row_factors) * pad_colorbar)
    cb.ax.set_title(value_var)
    cb.outline.set_linewidth(0.75)

    return ax
