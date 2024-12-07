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
    """
    Plots a confusion matrix of model probabilities (mpp) alongside a smaller inset of exceedance probabilities (xp).
    This plot is adapted from Findling et al. (Nature Human Behaviour, 2020).

    Parameters
    ----------
    mpp : numpy.ndarray
        A 2D array of shape (n_models, n_models) containing model probabilities. Each row represents data 
        generated from one model, and the values correspond to the probability of each model given the data.
    
    xp : numpy.ndarray
        A 2D array of shape (n_models, n_models) containing exceedance probabilities. Exceedance probability 
        indicates the likelihood that a given model outperforms the other models.
    
    model_labels : list of str
        A list of model labels to be displayed on the axes. The length of the list should match the number of models.
    
    ax : matplotlib.axes.Axes, optional
        The axes to plot on. If None, a new axis is created. Default is None.
    
    cmap : str, optional
        The colormap to use for the heatmap. Defaults to "viridis", but other options like "inferno", "plasma", etc. 
        are supported.
    
    fontcolor_threshold : float, optional
        The value threshold above which the font color for the heatmap values will switch. Default is 0.7.
    
    color_belowthresh : str, optional
        The font color to use for values below the threshold specified by `fontcolor_threshold`. Default is "white".
    
    color_abovethresh : str, optional
        The font color to use for values above the threshold specified by `fontcolor_threshold`. Default is "black".
    
    fontsize_main : int, optional
        The font size for the value labels in the main plot. Default is 5.
    
    fontsize_inset : int, optional
        The font size for the value labels in the inset plot. Default is 3.
    
    round_main_values : int, optional
        The number of decimal places to round the values in the main plot. Default is 2.
    
    round_inset_values : int, optional
        The number of decimal places to round the values in the inset plot. Default is 2.
    
    inset_aspect : float, optional
        The aspect ratio for the inset plot. A value of 1 is square, but setting it to 0.75 improves the layout. Default is 0.75.

    Returns
    -------
    matplotlib.axes.Axes
        The axis containing the full plot, including the confusion matrix and inset for exceedance probabilities.
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