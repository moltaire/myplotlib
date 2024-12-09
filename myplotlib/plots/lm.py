import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
from scipy.stats import pearsonr
from myplotlib.utilities.annotation import format_p


def lm(
    x,
    y,
    ax=None,
    xbounds=None,
    ybounds=None,
    ci_alpha=0.05,
    color=None,
    annotation_pos="auto",
    annotate=["b0", "b1", "r"],
):
    """
    Plots a linear regression of two variables, including a confidence band, regression line,
    and annotated statistics.

    Parameters
    ----------
    x : array-like or pandas.Series
        The independent variable (predictor) for the regression. If a pandas.Series, its name
        will be used as the x-axis label.

    y : array-like or pandas.Series
        The dependent variable (response) for the regression. If a pandas.Series, its name
        will be used as the y-axis label.

    ax : matplotlib.axes.Axes, optional
        The axes to plot on. If None, the current axes will be used. Default is None.

    xbounds : tuple, optional
        The lower and upper bounds for the x-axis. Default is the range of `x`.

    ybounds : tuple, optional
        The lower and upper bounds for the y-axis. Default is the range of `y`.

    ci_alpha : float, optional
        Significance level for confidence intervals around the regression line.
        Default is 0.05 (95% confidence intervals).

    color : str, optional
        Color for the regression line, scatter points, and confidence band.
        Default is the next available color in the current axis.

    annotation_pos : str, optional
        Position of the annotation in the plot, specified as "vertical horizontal"
        (e.g., "lower right"). Vertical options: "lower", "center", "upper".
        Horizontal options: "left", "center", "right". Default is "auto", where it tries
        to find the best corner on its own.

    annotate : list of str, optional
        List specifying which statistics to include in the annotation. Possible values:
        - 'b0': Intercept (β₀) with its p-value
        - 'b1': Slope (β₁) with its p-value
        - 'r': Pearson correlation coefficient (r) with its p-value
        Default is ['b0', 'b1', "r"].

    Returns
    -------
    matplotlib.axes.Axes
        The axes containing the plotted linear regression, confidence band, and annotation.
    """
    # Validate annotate argument
    valid_annotations = {"b0", "b1", "r"}
    if not set(annotate).issubset(valid_annotations):
        raise ValueError(
            f"Invalid annotation type(s) in {annotate}. Valid options are {valid_annotations}."
        )

    # Set defaults if None given
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = ax._get_lines.get_next_color()
    if xbounds is None:
        xbounds = [np.min(x), np.max(x)]
    if ybounds is None:
        ybounds = [np.min(y), np.max(y)]

    # Handle pandas.Series and get labels
    x_label = x.name if isinstance(x, pd.Series) else None
    y_label = y.name if isinstance(y, pd.Series) else None

    x = x.values if isinstance(x, pd.Series) else x
    y = y.values if isinstance(y, pd.Series) else y

    # Run Regression
    X = sm.add_constant(x)
    model = sm.OLS(y, X)
    results = model.fit()

    # Regression Estimates
    intercept, slope = results.params
    p_values = results.pvalues

    # Calculate the Pearson correlation coefficient and its p-value
    correlation, corr_p_value = pearsonr(x, y)

    # Predictions and Confidence Intervals
    x_pred = np.linspace(*xbounds, 100)
    X_pred = sm.add_constant(x_pred)
    y_pred = results.predict(X_pred)
    pred = results.get_prediction(X_pred)
    pred_summary_frame = pred.summary_frame(alpha=ci_alpha)

    # Scatter Plot
    ax.scatter(
        x,
        y,
        color=color,
        clip_on=False,
        zorder=9,
        lw=0.5,
        s=12,
        edgecolor="k",
        alpha=0.7,
    )

    # Regression Line
    ax.plot(x_pred, y_pred, lw=1.5, color=color)

    # Confidence Band
    ax.fill_between(
        x_pred,
        pred_summary_frame["mean_ci_lower"],
        pred_summary_frame["mean_ci_upper"],
        alpha=0.5,
        color=color,
        lw=0,
    )

    # Generate Annotation Text
    annotation_text = generate_annotation(
        intercept, slope, p_values, correlation, corr_p_value, annotate
    )

    # Position Annotation
    if annotation_pos == "auto":
        annotation_pos = find_best_corner(x, y, ax)
    apos_vertical, apos_horizontal = annotation_pos.split()
    if apos_vertical == "lower":
        y_pos = 0.05
        va = "bottom"
    elif apos_vertical == "center":
        y_pos = 0.5
        va = "center"
    else:
        y_pos = 1
        va = "top"

    if apos_horizontal == "left":
        x_pos = 0.05
        ha = "left"
    elif apos_horizontal == "center":
        x_pos = 0.5
        ha = "center"
    else:
        x_pos = 1
        ha = "right"

    ax.text(
        x_pos,
        y_pos,
        annotation_text,
        fontsize="xx-small",
        transform=ax.transAxes,
        va=va,
        ha=ha,
    )

    # Set Labels if Available
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    # Limits and Final Touches
    ax.set_xlim(xbounds)
    ax.set_ylim(ybounds)
    sns.despine()

    return ax


def generate_annotation(
    intercept, slope, p_values, correlation, corr_p_value, annotate
):
    """
    Generate annotation text based on specified statistics.

    Parameters
    ----------
    intercept : float
        The intercept of the regression line.

    slope : float
        The slope of the regression line.

    p_values : array-like
        p-values for the regression parameters.

    correlation : float
        Pearson correlation coefficient.

    corr_p_value : float
        p-value for the correlation coefficient.

    annotate : list of str
        List specifying which statistics to include in the annotation.

    Returns
    -------
    str
        The formatted annotation text.
    """
    annotations = []
    if "b0" in annotate:
        annotations.append(rf"$\beta_0$ = {intercept:.2f} ({format_p(p_values[0])})")
    if "b1" in annotate:
        annotations.append(rf"$\beta$ = {slope:.2f} ({format_p(p_values[1])})")
    if "r" in annotate:
        annotations.append(rf"$r$ = {correlation:.2f} ({format_p(corr_p_value)})")
    return "\n".join(annotations)



def find_best_corner(x, y, ax):
    """
    Determines the best corner of the plot to place an annotation
    such that it overlaps the least with the data points.

    Parameters:
    - x: array-like, x-coordinates of the data points.
    - y: array-like, y-coordinates of the data points.
    - ax: Matplotlib Axes object, the axis where the scatter plot is drawn.

    Returns:
    - best_corner: str, the name of the best corner.
    """
    # Get plot limits
    x_min, x_max = ax.get_xlim()
    y_min, y_max = ax.get_ylim()

    # Define the four corners
    corners = {
        "top left": (x_min, y_max),
        "top right": (x_max, y_max),
        "bottom left": (x_min, y_min),
        "bottom right": (x_max, y_min),
    }

    # Calculate the number of points in each corner region
    counts = {}
    for corner, (cx, cy) in corners.items():
        if "top" in corner:
            y_condition = y > (y_max + y_min) / 2
        else:
            y_condition = y <= (y_max + y_min) / 2
        if "right" in corner:
            x_condition = x > (x_max + x_min) / 2
        else:
            x_condition = x <= (x_max + x_min) / 2

        counts[corner] = np.sum(x_condition & y_condition)

    # Find the least populated corner
    best_corner = min(counts, key=counts.get)
    return best_corner
