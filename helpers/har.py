#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:09:34 2017

@author: georg
"""

from arch.univariate import HARX
from helpers import ScoreOf


class HarModel():
    '''Find the best HARX mean model.

    This class wraps around the HAR class from Kevin Shepard's arch package.
    Given a set of fixed parameters, it provides two methods that allow
    refining and extending a given set of HAR-lags, resepectively. Convenient
    attributes allow monitoring the progress of an iterative optimization.

    Parameters
    ----------
    params : dict
        Dictionary of all parameters to pass to the HARX model *except* the
        HAR-lag(s). Specifically, the paramter `hold-back` is *mandatory*,
        as it determines the maximum value for the HAR-Lags that are tried.
    lags : list of int, optional
        List of HAR-lags to initialize the model, defaults to [1].

    Attributes
    ----------
    bic : ScoreOf
        The BIC of the current HARX model. Being of type ScoreOf means that it
        can tell if it got smaller since the last invocation of either the
        `refine` or the `extend` method, or not.
    lags : list of int
        List of HAR-lags in the current model.
    model : HAR
        An instance of the HAR class with parameters `params` and current
        HAR-lag(s) `lags`.

    Examples
    --------
    >>> parameters = {'y': some_data,
                      'constant': False,
                      'hold-back': 22,
                      'distribution': StudentsT()}
    >>> har = HarModel(parameters)
    >>> har.lags
    [1]

    '''

    def __init__(self, params, lags=[1]):
        self.__params = params
        self.__lags = lags
        self.__bic = ScoreOf(self.__bic_with(self.__lags))

    @property
    def bic(self):
        return self.__bic

    @property
    def lags(self):
        return self.__lags

    @property
    def model(self):
        return HARX(**self.__params, lags=self.__lags)

    def refine(self):
        '''Refine the current set of HAR-lags.

        Since trying all possible models with a given number of HAR-lags is
        prohibitively expensive, only a pretty good list of HAR-lags can be
        found with no guarantee that it is actually the best possible. Here,
        HAR-lags are iteratively forward-selected. Specifically, the
        refinement assumes that a new HAR-lag has just been added, either by
        initial instantiation or by having successfully called the `extend`
        method. It then consecutively takes each HAR-lag that existed prior to
        adding the current one and:
            1. Deletes it.
            2. Scans through all possible HAR-lags (up to the maximum specified
               by `hold_back`) to find the one that yields the minimum BIC in
               conjunction with the remaining ones.
            3. Appends the HAR-lag so obtained to the list of the remaining
               ones, if no already contained.
        This procedure is repeated until it no longer leads to a decrease in
        BIC. Note that the a given list of HAR-lags can also be shortened by
        this algorithm.

        '''
        bic = ScoreOf(self.__bic)
        while bic.gets_smaller():
            bic.changes_to(self.__cycled(bic))
        self.__bic.changes_to(bic)

    def extend(self):
        '''Extend the current set of HAR-lags.

        Cycles through all possible HAR-lags up to the maximum specified by
        `hold_back`, tentatively adds them to the list of existing HAR-lags,
        and keeps the one yielding the smallest BIC. If no additional HAR-lag
        can be found that lowers the current BIC, then the list of current
        HAR-lags is not extended.

        '''
        min_lag, min_bic = self.__improved_over(self.__bic)
        if min_lag not in self.__lags:
            self.__lags.append(min_lag)
        self.__bic.changes_to(min_bic)

    def __bic_with(self, lag_list):
        model = HARX(**self.__params, lags=lag_list)
        result = model.fit(update_freq=0, disp='off')
        return round(result.bic, 4)

    def __cycled(self, min_bic):
        min_len = len(self.__lags) - 1 or 1
        for i in range(min_len):
            del self.__lags[0]
            min_lag, min_bic = self.__improved_over(min_bic)
            if min_lag not in self.__lags:
                self.__lags.append(min_lag)
        return min_bic

    def __improved_over(self, min_bic):
        max_lag = self.__params['hold_back']
        for lag in range(1, max_lag+1):
            try_lags = list(set(self.__lags).union([lag]))
            bic = self.__bic_with(try_lags)
            if bic <= min_bic:
                min_bic = bic
                min_lag = lag
        return min_lag, min_bic
