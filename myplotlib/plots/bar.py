import matplotlib.pyplot as plt
import numpy as np

def bar(
    y,
    labels=None,
    colors=None,
    ax=None,
    annotate_y=True,
    annotation_kwargs=dict(ha="center", va="bottom", fontsize="small"),
):
    """
    Create a customizable bar plot with optional annotations.

    Parameters
    ----------
    y : list or array-like
        Heights of the bars (e.g., frequencies or counts).
    labels : list or array-like, optional
        Labels for the bars (displayed on the x-axis). If None, numeric indices will be used as labels.
    colors : list, optional
        Colors for the bars. If None, default Matplotlib categorical colors are used.
    ax : matplotlib.axes.Axes, optional
        Pre-existing Matplotlib Axes to plot on. If None, the current active Axes (plt.gca()) is used.
    annotate_y : bool, optional
        Whether to annotate the bars with their corresponding heights. Default is True.
    annotation_kwargs : dict, optional
        Additional keyword arguments for `ax.annotate` to style the annotations (e.g., font size, alignment).
        Default is `dict(ha="center", va="bottom", fontsize="small")`.

    Returns
    -------
    matplotlib.axes.Axes
        The Axes object with the bar plot.

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> y = [5, 10, 15]
    >>> labels = ["A", "B", "C"]
    >>> bar(y, labels=labels)
    >>> plt.show()

    Notes
    -----
    - If `labels` is None, numeric indices will be used as default x-axis labels.
    - This function uses the default Matplotlib categorical color palette unless `colors` is provided.
    - Ensure that `len(labels)` and `len(colors)` (if provided) match the length of `y` to avoid errors.

    """
    xs = np.arange(len(y))

    if labels is None:
        labels = xs

    if colors is None:
        colors = [f"C{i}" for i in xs]
    if ax is None:
        ax = plt.gca()

    # Plot
    ax.bar(xs, y, color=colors)

    # Ticks and labels
    ax.set_ylabel("Freq.")
    ax.set_xticks(xs)
    ax.set_xticklabels(labels)

    # Annotate counts
    if annotate_y:
        for x, c in zip(xs, y):
            ax.annotate(c, (x, c), **annotation_kwargs)

    return ax
