# /usr/bin/python

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymc3 as pm

from myplotlib.plots.scatter import scatter


def lm(
    x,
    y,
    trace=None,
    credible_interval=0.95,
    ax=None,
    bandalpha=0.6,
    scatter_kws={},
    **kwargs
):
    """Make a custom linear model plot with confidence bands.

    Args:
        x (array like): x values
        y (array like): y values
        trace (pymc3.MultiTrace, optional): GLM trace from PyMC3.
        ax (matplotlib.axis, optional): Axis to plot on. Defaults to current axis.
        bandalpha (float, optional): Opacity level of confidence band.
        scatter_kws (dict, optional): Dictionary of keyword arguments passed onto `scatter`.
        **kwargs: Keyword arguments passed onto plot of regression line.

    Returns:
        matplotlib.axis: Axis with the linear model plot.
    """
    if ax is None:
        ax = plt.gca()

    # Determine color (this is necessary so that the scatter and the line have the same color)
    color = next(ax._get_lines.prop_cycler)["color"]

    # Scatter

    print(scatter)
    ax = scatter(x, y, color=color, ax=ax, **scatter_kws)

    # Run GLM in PyMC3
    if trace is None:
        df = pd.DataFrame(dict(x=x, y=y))
        with pm.Model() as glm:
            pm.GLM.from_formula("y ~ x", data=df)
            trace = pm.sample()

    summary = pm.summary(trace)

    # Plot MAP regression line
    xs = np.linspace(np.min(x), np.max(x), 100)
    intercept = summary.loc["Intercept", "mean"]
    beta = summary.loc["x", "mean"]
    ax.plot(xs, intercept + beta * xs, color=color, zorder=4, **kwargs)

    # Plot posterior predictive credible region band
    intercept_samples = trace.get_values("Intercept")
    beta_samples = trace.get_values("x")
    ypred = intercept_samples + beta_samples * xs[:, None]
    ypred_lower = np.quantile(ypred, (1 - credible_interval) / 2, axis=1)
    ypred_upper = np.quantile(ypred, 1 - (1 - credible_interval) / 2, axis=1)
    ax.fill_between(
        xs,
        ypred_lower,
        ypred_upper,
        color=color,
        zorder=1,
        alpha=bandalpha,
        linewidth=0,
    )

    return ax, trace, summary
