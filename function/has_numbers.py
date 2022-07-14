# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:00:35 2022

@author: pio-r
"""


def has_numbers(inputString):
    """
    

    Parameters
    ----------
    inputString : string

    Returns
    -------
    Returns True if there are numbers in the string

    """
    return any(char.isdigit() for char in inputString)