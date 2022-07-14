# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:03:22 2022

@author: pio-r
"""

def hasRepeatedChars(s):
    for i in range(len(s)):
        if i != s.rfind(s[i]):
            return True
    return False