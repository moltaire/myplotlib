import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def interaction(data, line_var, x_var, y_var, dodge=0.05, ax=None):
    """
    Create an interaction plot, often used in psychological research, to show how
    different levels of one categorical variable (line_var) interact across
    levels of another categorical variable (x_var). The plot shows lines with error
    bars representing means and standard errors for each combination of the categorical variables.

    Parameters
    ----------
    data : pandas.DataFrame
        The data to plot. The dataframe must contain the variables specified by `line_var`,
        `x_var`, and `y_var`.

    line_var : str
        The categorical variable that defines the lines in the plot.

    x_var : str
        The categorical variable plotted on the x-axis.

    y_var : str
        The continuous variable plotted on the y-axis.

    dodge : float, optional
        The amount by which to shift the lines along the x-axis to avoid overlap.
        Default is 0.05.

    ax : matplotlib.axes.Axes, optional
        The axis to plot on. If None, the current axis is used. Default is None.

    Returns
    -------
    matplotlib.axes.Axes
        The axis with the interaction plot.

    Example
    -------
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    # Example data
    data = pd.DataFrame({
        'Condition': np.repeat(['A', 'B'], 10),
        'Group': np.tile(['Control', 'Experimental'], 10),
        'Score': np.random.randn(20) + np.tile([0, 1], 10)
    })

    # Create an interaction plot
    fig, ax = plt.subplots()
    interaction(data, line_var='Group', x_var='Condition', y_var='Score', ax=ax)
    plt.show()
    """
    if ax is None:
        ax = plt.gca()

    # Summarize data
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
