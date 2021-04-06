import matplotlib.pyplot as plt
import numpy as np


def model_recovery(
    mpp,
    xp,
    model_labels,
    ax=None,
    cmap="viridis",
    fontcolor_threshold=0.7,
    color_belowthresh="white",
    color_abovethresh="black",
    fontsize_main=5,
    fontsize_inset=3,
    round_main_values=2,
    round_inset_values=2,
    inset_aspect=0.75
):
    """Plots a confusion matrix of model probabilities and a smaller one of exceedance probabilities. This plot is adapted from Findling et al. (Nature Human Behaviour, 2020).

    Args:
        mpp (numpy.array): Array (n_models, n_models) of model probabilities. Each row corresponds to data generated from one model
        xp (numpy.array): Like `mpp`, but contains exceedance probabilities.
        model_labels (list): Model labels.
        ax (matplotlib.axis, optional): Axis to plot on. Defaults to creating a new one.
        cmap (str, optional): Colormap name. Defaults to "viridis".
        fontcolor_threshold (float, optional): Value threshold where to switch from `colow_belowthresh` to `color_abovethresh` for value labels in each cell. Defaults to 0.7.
        color_belowthresh (str, optional): Fontcolor for value labels below `fontcolor_threshold`. Defaults to "white".
        color_abovethresh (str, optional): Fontcolor for value labels above `fontcolor_threshold`. Defaults to "black".
        fontsize_main (int, optional): Fontsize of value labels in main plot. Defaults to 5.
        fontsize_inset (int, optional): Fontsize of value labels in inset xp plot. Defaults to 3.
        round_main_values (int, optional): Precision of value labels in main plot. Defaults to 2.
        round_inset_values (int, optional): Precision of value labels in inset xp plot. Defaults to 2.
        inset_aspect (float, optional): Aspect ratio modifier for inset plot. Somehow matplotlib does not make a square plot if it is set to `"equal"` or `1`. Defaults to 0.75.

    Returns:
        matplotlib.axis: Axis with inset axis.
    """
    if ax is None:
        ax = plt.gca()

    # Plot heatmap
    ax.matshow(mpp, cmap=cmap, vmin=0, vmax=1)
    ax.xaxis.set_ticks_position("bottom")
    ax.tick_params(axis="both", which="both", length=0)  # Hide ticks

    ## Add heatmap values
    for (i, j), z in np.ndenumerate(mpp):
        if z < fontcolor_threshold:
            color = color_belowthresh
        else:
            color = color_abovethresh
        ax.text(
            j,
            i,
            "{0:0.{prec}f}".format(z, prec=round_main_values),
            ha="center",
            va="center",
            color=color,
            fontsize=fontsize_main,
        )

    # Plot inset with xp heatmap
    ax_inset = ax.inset_axes([1.05, 0.5, 0.5, 0.5], transform=ax.transAxes)
    ax_inset.matshow(xp, cmap=cmap, vmin=0, vmax=1, aspect=inset_aspect)

    ## Add heatmap values
    for (i, j), z in np.ndenumerate(xp):
        if z < fontcolor_threshold:
            color = color_belowthresh
        else:
            color = color_abovethresh
        ax_inset.text(
            j,
            i,
            "{0:0.{prec}f}".format(z, prec=round_inset_values),
            ha="center",
            va="center",
            color=color,
            fontsize=fontsize_inset,
        )

    # Draw full bounding boxes
    for side in ["right", "top"]:
        for axis in [ax, ax_inset]:
            axis.spines[side].set_visible(True)

    # Set ticks and labels
    ax.set_xticks(range(len(model_labels)))
    ax.set_xticklabels(model_labels, rotation=45)
    ax.set_xlabel("Recovered model")
    ax.set_yticks(range(len(model_labels)))
    ax.set_yticklabels(model_labels)
    ax.set_ylabel("Generating model")
    ax.set_title("Posterior probabilities")

    ## Inset axis
    ax_inset.set_xticks([])
    ax_inset.set_yticks([])
    ax_inset.set_xlabel("Exceedance\nprobabilities")

    return ax