import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from matplotlib.patches import Rectangle


def raincloud(
    df,
    scatter_kws=dict(dodge=0.25, jitter=0.15, lw=0.25, alpha=0.7, s=6),
    violin_kws=dict(alpha=0.5, width=0.5),
    box_kws=dict(lw=0.75, width=0.25, ci_alpha=0.95, capsize=2),
    ax=None,
    colors=None,
):
    """
        Create a composite plot with scatter, violin, and box plots for each column in the input DataFrame.
        Strongly inspired by - well ok copied from - Stefano Palminteri's papers (e.g., Vandendriessche et al., 2023; https://doi.org/10.1017/S0033291722001593)
    )

        This function generates a plot for each column of the input DataFrame (`df`) using three plot types:
        1. **Scatter Plot**: Displays individual data points with optional dodge and jitter for better visualization.
        2. **Violin Plot**: Displays the distribution of the data for each column with optional transparency and width.
        3. **Box Plot**: Displays the confidence interval (CI) for the mean, with mean and standard error bars, for each column. The CI is represented as a rectangle, and the mean ± SE is shown as a horizontal line with error bars.

        The plot uses various optional keyword arguments to customize the appearance of the scatter, violin, and box plots.

        Parameters:
        ----------
        df : pandas.DataFrame
            The DataFrame containing the data to be plotted. Each column represents a variable for which the plots will be generated.
        scatter_kws : dict, optional
            A dictionary of keyword arguments to customize the scatter plot, including:
            - `dodge` (float): Horizontal displacement of scatter points.
            - `jitter` (float): Amount of jitter applied to scatter points.
            - `lw` (float): Line width for scatter points.
            - `alpha` (float): Transparency of scatter points.
            - `s` (int): Size of scatter points. Default is 6.
        violin_kws : dict, optional
            A dictionary of keyword arguments to customize the violin plot, including:
            - `alpha` (float): Transparency of the violin bodies.
            - `width` (float): Width of the violins. Default is 0.5.
        box_kws : dict, optional
            A dictionary of keyword arguments to customize the box plot, including:
            - `lw` (float): Line width for box plot elements.
            - `width` (float): Width of the box plot.
            - `ci_alpha` (float): Confidence interval alpha for mean (default is 0.95).
            - `capsize` (int): Size of the cap at the end of error bars.
        ax : matplotlib.Axes, optional
            The axes on which to plot the data. If `None`, the current axes (`plt.gca()`) are used.
        colors : list of str, optional
            A list of colors for the plots. If `None`, a default color palette is used.

        Returns:
        -------
        ax : matplotlib.Axes
            The axes with the generated plots.

        Example:
        --------
        >>> import pandas as pd
        >>> import numpy as np
        >>> df = pd.DataFrame({
        >>>     "A": np.random.normal(0, 1, 100),
        >>>     "B": np.random.normal(0, 1, 100),
        >>>     "C": np.random.normal(0, 1, 100),
        >>> })
        >>> plotminteri(df)
    """
    if ax is None:
        ax = plt.gca()

    x = range(len(df.columns))

    if colors is None:
        colors = [f"C{i}" for i in x]

    # Violin Plot (this function works on each column at the same time)
    data_to_plot = [df[col].dropna() for col in df.columns]

    vp = ax.violinplot(
        data_to_plot,
        side="high",
        positions=x,
        showextrema=False,
        widths=violin_kws["width"],
    )
    for i, b in enumerate(vp["bodies"]):
        b.set_color(colors[i])
        b.set_linewidth(0)
        b.set_alpha(violin_kws["alpha"])

    # Per column
    for i, var in enumerate(df.columns):
        color = colors[i]

        # Box Plot / Error bars
        mean = np.mean(df[var].dropna())
        se = stats.sem(df[var].dropna())
        ci = stats.t.interval(box_kws["ci_alpha"], len(df[var]) - 1, loc=mean, scale=se)

        # CI rectangle
        rect = Rectangle(
            xy=(x[i], ci[0]),
            width=box_kws["width"],
            height=ci[1] - ci[0],
            linewidth=box_kws["lw"],
            edgecolor=color,
            facecolor="none",
        )
        ax.add_patch(rect)

        # Mean ± SE
        ax.hlines(
            mean,
            x[i],
            x[i] + box_kws["width"],
            color="black",
            lw=box_kws["lw"],
        )
        ax.errorbar(
            x[i] + box_kws["width"] / 2,
            y=mean,
            yerr=se,
            color="black",
            label="Mean ± SE",
            lw=box_kws["lw"],
            capsize=box_kws["capsize"],
            capthick=box_kws["lw"],
        )

        # Scatter Plot
        ax.scatter(
            np.ones(len(df)) * x[i]
            - scatter_kws["dodge"]
            + scatter_kws["jitter"] * np.random.uniform(size=len(df)),
            df[var],
            color=color,
            edgecolor="black",
            lw=scatter_kws["lw"],
            alpha=scatter_kws["alpha"],
            s=scatter_kws["s"],
            clip_on=False,
            zorder=5,
        )

    ax.set_xticks(x)
    ax.set_xticklabels(df.columns)

    return ax
