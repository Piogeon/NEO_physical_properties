# -*- coding: utf-8 -*-
"""
Created on Thu May 19 12:02:48 2022

@author: pio-r
"""

import numpy as np
from astroquery.jplsbdb import SBDB
from function.is_nan import isNaN
from function.protolog import protolog


def simda_dataset(df):
    if all(isNaN(df["Name"].iloc[i]) for i in range(0, len(df["Name"]))) and\
        any(not isNaN(df["Number"].iloc[i]) for i in range(0, len(df["Name"]))):
        for i in range(len(df["Name"])):
            try:
                if not isNaN(df["Number"].iloc[i]):
                    sbdb = SBDB.query(np.int(df["Number"].iloc[i]))
                else:
                    sbdb = SBDB.query(df["Prov.Desig"].iloc[i])
                if "shortname" in sbdb["object"]:
                    df["Name"].iloc[i] = sbdb["object"]["shortname"]
                    df["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                    start = df["Prov.Desig"].iloc[i].find("(")
                    end = df["Prov.Desig"].iloc[i].find(")")
                    df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
                    if ' ' in df["Name"].iloc[i]:
                        start = df["Name"].iloc[i].find(" ")
                        df["Name"].iloc[i] = df["Name"].iloc[i][start+1:]
                    else:
                        df["Name"].iloc[i] = df["Name"].iloc[i]
                else:
                   protolog("inf", "The asteroid {} has no name".format(df["Prov.Desig"].iloc[i]))
                   continue
            except ValueError:
                print("Unable to retrieve the asteroid {}".format(df["Prov.Desig"].iloc[i]))
    else:
        print("Nothing to do")
    
    return df