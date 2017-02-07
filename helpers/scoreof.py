#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:08:59 2017

@author: georg
"""


class ScoreOf():
    '''

    A floating point number that remembers if it got smaller since the last
    update.

    Parameters
    ----------
    value : numeric
        Initial value of the Score.

    Examples
    --------
    >>> a = ScoreOf(3.1)
    >>> a
    3.1

    >>> a.changes_to(2.0)
    >>> a
    2.0

    >>> a.gets_smaller()
    True

    >>> a.changes_to(2.7)
    >>> a
    2.7

    >>> a.gets_smaller
    False


    '''

    def __init__(self, value):
        self.__new = float(value)
        self.__old = float(value) + 1.0

    def __repr__(self):
        return repr(self.__new)

    def __float__(self):
        return self.__new

    def __ge__(self, other):
        return self.__new >= float(other)

    def changes_to(self, new):
        '''Update the value of the Score.

        ----------------

        Parameters
        ----------
        new : numeric
            New value of the Score.

        Examples
        --------
        >>> a = ScoreOf(3.1)
        >>> a
        3.1

        >>> a.changes_to(2.0)
        >>> a
        2.0

        '''
        self.__old = self.__new
        self.__new = float(new)

    def gets_smaller(self):
        '''Check if the Score got smaller since the last update.

        ----------------

        Returns
        -------
        boolean
            Whether the score got smaller since the last update.

        Examples
        --------
        >>> a = Score(3.1)
        >>> a.gets_smaller()
        True

        >>> a.changes_to(2.0)
        >>> a.gets_smaller()
        True

        >>> a.changes_to(2.7)
        >>> a.gets_smaller()
        False

        Notes
        -----
        Always yields ``True`` after inital instantiation of a Score.

        '''
        return self.__new < self.__old

    def got_smaller(self):
        '''Alias to method `gets_smaller()`'''
        return self.gets_smaller()
