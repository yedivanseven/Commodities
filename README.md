# Commodities
## The Volatility of Futures Indices

This repository contains several `IPython` notebooks that explore various
methods of _time series analysis_. In particular, we are looking at _financial_
time series, which (not untypically):

1. show no (partial) autocorrelation but
2. exhibit volatility bunching.

## Maximum Likelihood Methods
The three notebooks
+ Daily
+ Monthly
+ Recently.

do the same thing but for differrent time horizons, as the names imply.
Sepcifically, we use [Kevin Shepard](https://www.kevinsheppard.com/Main_Page)'s excellent [`arch`-package](https://pypi.python.org/pypi/arch/4.0) to find
(within limits) the best of various types of autoregressive conditionally heteroscedastic (ARCH) models to the returns.

Most of the heavy lifting in finding the optimal model parameters is outsourced
from the notebooks into a decently documented `helpers` package.

## Baysian Methods
In the _Bayesian_ notebook, we explore the possibilities and models offered by
Ross Taylor's [`PyFlux`-package](http://www.pyflux.com/). As there is a lot to
play with, optimal model selection can take some time. To speed things up
considerably, we leverage the python `multiprocessing` module and crunch
through several models at the same time, in parallel. This is again outsourced
into the `helpers` package.

### Dependencies
Everything seems to run smoothly with a fairly fresh install of Anaconda 4.3.
Other than [`arch`](https://pypi.python.org/pypi/arch/4.0) or [`PyFlux`](http://www.pyflux.com/), there are no additional dependencies.
This is for `python 3.6`.

### Data
The financial time series I used for these notebooks are, unfortunatley,
proprietary and cannot be released under the same license as the notebooks. The notebooks themselves, however, should be really easy to adapt to any time
series.
