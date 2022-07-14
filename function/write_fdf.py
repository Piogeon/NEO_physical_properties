# -*- coding: utf-8 -*-
"""
Created on Mon May  9 14:04:08 2022

@author: pio-r
"""


import sys
from function.is_nan import isNaN
from function.protolog import protolog

def write_fdf(fpath, pd, specs):
    """
    Write a Pandas dataframe in fixed width column format with the given
    column specs

    Args:
        fpath: File path
        pd: Dataframe
        specs: A list of python formats
    """
    with open(fpath, "w") as f:                                                #For with statement (https://peps.python.org/pep-0343/); The open() function opens the file (if possible) and returns the corresponding file object.
        for _, row in pd.iterrows():                                           #df.iterrows() Iterate over DataFrame rows as (index, Series) pairs.
            for idx, value in enumerate(row):                                        #vedere funzione raise error/exception
                sys.stdout.write(specs[idx].format(value))
                f.write(specs[idx].format(value))

            f.write("\n")
            print("")
        
        
            