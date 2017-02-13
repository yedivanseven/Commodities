# Commodities
## The Volatility of Futures Indices

This repository contains three `IPython` notebooks, Daily, Monthly and Recently.
All three do the same thing for differrent time horizons, as the names imply.
In particular, we are looking at financial time series, which (not untypically):

1. show no (partial) autocorrelation but
2. exhibit volatility bunching.

We then use [Kevin Shepard](https://www.kevinsheppard.com/Main_Page)'s excellent
[`arch`-package](https://pypi.python.org/pypi/arch/4.0) to find (within limits)
the best of various types of autoregressive conditionally heteroscedastic (ARCH)
models to the returns.

Most of the heavy lifting in finding the optimal model parameters is outsourced
from the notebooks into a decently documented `helpers` module.

### Dependencies
Everything seems to run smoothly with a fairly fresh install of Anaconda 4.3.
Other than [`arch`](https://pypi.python.org/pypi/arch/4.0), there are no
additional dependencies.

### Data
The financial time series I used for these notebooks are, unfortunatley,
proprietary and cannot be released under the same license as the notebooks. The notebooks themselves, however, should be really easy to adapt to any time
series.
