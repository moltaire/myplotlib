import numpy as np
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
    annotation_pos="lower right",
):
    """
    Plots a linear regression of two variables, including
    a confidence band around the regression line and
    some annotation.
    """
    # Set defaults if None given
    if ax is None:
        ax = plt.gca()
    if color is None:
        color = ax._get_lines.get_next_color()
    if xbounds is None:
        xbounds = [np.min(x), np.max(x)]
    if ybounds is None:
        ybounds = [np.min(y), np.max(y)]

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

    # Data
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

    # Annotation
    annotation_text = (
        r"$\beta_0$ = " + f"{intercept:.2f} ({format_p(p_values.iloc[0])})\n"
        r"$\beta$ = " + f"{slope:.2f} ({format_p(p_values.iloc[1])})\n"
        r"$r$ = " + f"{correlation:.2f} ({format_p(corr_p_value)})"
    )
    apos_vertical, apos_horizontal = annotation_pos.split()
    if apos_vertical == "lower":
        y = 0.05
        va = "bottom"
    elif apos_vertical == "center":
        y = 0.5
        va = "center"
    else:
        y = 1
        va = "top"
    if apos_horizontal == "left":
        x = 0.05
        ha = "left"
    elif apos_horizontal == "center":
        x = 0.5
        ha = "center"
    else:
        x = 1
        ha = "right"
    ax.text(
        x,
        y,
        annotation_text,
        fontsize=4.5,
        transform=ax.transAxes,
        va=va,
        ha=ha,
    )

    # Limits
    ax.set_xlim(xbounds)
    ax.set_ylim(ybounds)
    sns.despine()

    return ax
