# -*- coding: utf-8 -*-
"""
Created on Tue May 10 10:34:08 2022

@author: pio-r
"""
from function.is_nan import isNaN


def start_space(string):
    if not isNaN(string) and string.startswith(' '):
        string = string.lstrip()
    else:
        string
    return string