# myplotlib

![myplotlib style](examples/combination.png)

My custom matplotlib stuff. I got inspired to do this by [this blogpost](https://colcarroll.github.io/yourplotlib/) and this [PyData Talk](https://www.youtube.com/watch?v=NV4Y75ZUDJA).

This is very much a work in progress. See the [gallery notebook](https://github.com/moltaire/myplotlib/blob/master/gallery.ipynb) for function calls.

Currently included:

## Plots

### Histogram

![histogram](examples/histogram.png)

### Violin plot

![violin](examples/violin.png)

### Scatter plot

![scatter](examples/scatter.png)

### Linear Model plot

![lm](examples/lm.png)

### Factorial heatmap

![factorial](examples/factorial_heatmap.png)

### Model recovery plot

adapted from

- Findling, C., Chopin, N., & Koechlin, E. (2020). Imprecise neural computations as a source of adaptive behaviour in volatile environments. Nature Human Behaviour. https://doi.org/10.1038/s41562-020-00971-z

![model_recovery](examples/model_recovery.png)

## Utilities

### Subplot labelling

![label axes](examples/labelAxes.png)

### Annotation

![annotation](examples/hTextLine.png)

### Axis breaking

**Note that this is purely visual, and does not change the actual plotted data**. I use it to better communicate if I set limits so that 0 is excluded from the range of values, but still want the axis origin to be labelled 0.

![axis breaking](examples/breakAxes.png)

## Stats

### BMS

Basic, sampling based python implementation of the model selection procedure described in

- Stephan, K. E., Penny, W. D., Daunizeau, J., Moran, R. J., & Friston, K. J. (2009). Bayesian model selection for group studies. NeuroImage, 46(4), 1004–1017. https://doi.org/10.1016/j.neuroimage.2009.03.025

`bmsResult = bms(L=L, cores=1)`

The `bmsResult` is a dictionary that contains a `summary` of the MCMC chain, an array of exceedance probabilities `xp` and an array of model rates `r`.