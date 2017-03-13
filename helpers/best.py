#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 22:51:00 2017

@author: georg
"""

from multiprocessing import Pool, cpu_count


def _fit_with(leverage):
    global add_leverage
    add_leverage = leverage


def _bic_of(model):
    if add_leverage and hasattr(model, 'add_leverage'):
        model.add_leverage()
    return model.fit().bic, model.model_name


def best_of(model_iter, n_cores=None, leverage=False):
    '''Find the best (leveraged) model and return it.

    ----------------

    Parameters
    ----------
    model_iter : iterable
        An iterable with the models to test.
    n_cores : int, optional
        The number of CPU cores to use in the search for the best model.
        Defaults to the maximum number of cores available.
    leverage : boolean, optional
        Whether or not to add a leverage term to models that provide that
        option. Defaults to ``False`` and is ignored if the model object
        has neither an attribute nor a method named 'add_leverage'.

    Returns
    -------
    The model with the lowest BIC.

    '''
    models = dict((model.model_name, model) for model in model_iter)

    n_procs = n_cores if n_cores else max(cpu_count(), len(models))

    with Pool(n_procs, _fit_with, (leverage,)) as procs:
        bics = procs.imap_unordered(_bic_of, models.values())
        procs.close()
        procs.join()

    minimalBIC = min(bics)[1]
    best_model = models.get(minimalBIC)

    if leverage and hasattr(best_model, 'add_leverage'):
        best_model.add_leverage()

    return best_model
