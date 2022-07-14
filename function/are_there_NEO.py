# -*- coding: utf-8 -*-
"""
Created on Tue May 17 12:01:50 2022

@author: pio-r
"""
from astroquery.jplsbdb import SBDB
from tqdm import tqdm


def are_there_NEO(df):
    """
    

    Parameters
    ----------
    df : Dataframe

    Returns
    The list name of the non-NEOs in your dataframe and the lsit of indexes.
    -------
    None.

    """
    list_non_neo = []
    idx = []
    for i in tqdm(range(len(df["Name"]))):
        try:
            sbdb = SBDB.query(df["Prov.Desig"].iloc[i])
            if not sbdb["object"]["neo"]:
                list_non_neo.append(sbdb["object"]["fullname"])
                idx.append(i)
            else:
                continue
        except:
            continue
    return list_non_neo, idx