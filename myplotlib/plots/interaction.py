import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def interaction(data, line_var, x_var, y_var, dodge=0.05, ax=None):

    if ax is None:
        ax = plt.gca()

    # Summarise data
    df = (
        data.groupby([x_var, line_var])[y_var]
        .aggregate(["mean", "std", "sem", "count"])
        .reset_index()
    )

    # Get values
    line_vals = df[line_var].unique()
    x_vals = df[x_var].unique()
    x = np.arange(len(x_vals))

    dodge = dodge * (x - x.mean())

    for i, line_val in enumerate(line_vals):
        color = f"C{i}"
        df_i = df.loc[df[line_var] == line_val]
        eb = ax.errorbar(
            x + dodge[i],
            df_i["mean"],
            yerr=df_i["sem"],
            marker="o",
            mec=color,
            label=line_val,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(df_i[x_var])

    ax.set_ylabel(y_var)
    ax.set_xlabel(x_var)

    ax.legend(title=line_var)

    return ax
