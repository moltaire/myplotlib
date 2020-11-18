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
    """Make a factorial heatmap.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame containing categorical factors and numerical value variable
    row_factors : list
        List of factors determining heatmap rows
    col_factors : list
        List of factors determining heatmap columns
    value_var : str
        Name of the value variable
    factor_labels : dict, optional
        Dictionary containing mappings from variable names in the DataFrame to displayed variable names, by default {}
    level_labels : dict, optional
        Dictionary containing dictionaries for each factor, containing mappings from level names to displayed level names, by default {}
    cmap : str, optional
        cmap argument passed on to matplotlib.pyplot.imshow, by default "viridis_r". But try "inferno", "magma", ...
    ax : matplotlib.axis, optional
        Axis to plot on, by default None

    Returns
    -------
    matplotlib.axis
        axis with plot
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
