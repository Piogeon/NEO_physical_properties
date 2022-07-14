# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:10:00 2022

@author: pio-r
"""

import numpy as np
from astroquery.jplsbdb import SBDB
from function.is_nan import isNaN
from function.protolog import protolog
import re

def neorocks_diam(df):
    df["Prov.Desig"] = df["Number"]
    if all(isNaN(df["Name"].iloc[i]) for i in range(len(df))):
        for j in range(len(df)):
            try:
                if not isNaN(df["Number"].iloc[j]) and np.str(df["Number"].iloc[j]).isdigit():
                    sbdb = SBDB.query(np.int(df["Number"].iloc[j]))
                else:
                    sbdb = SBDB.query(df["Prov.Desig"].iloc[j])
                if "object" in sbdb:
                    if "shortname" in sbdb["object"]:
                        df["Name"].iloc[j] = sbdb["object"]["shortname"]
                        df["Prov.Desig"].iloc[j] = sbdb["object"]["fullname"]
                        start = df["Prov.Desig"].iloc[j].find("(")
                        end = df["Prov.Desig"].iloc[j].find(")")
                        if '=' in df["Prov.Desig"].iloc[j][start+1:end]:
                            eq = df["Prov.Desig"].iloc[j].find("=")
                            df["Prov.Desig"].iloc[j] = df["Prov.Desig"].iloc[j][start+1:eq-1]
                            if '(' in df["Name"].iloc[j]:
                                start = df["Name"].iloc[j].find("(")
                                end = df["Name"].iloc[j].find(")")
                                if not any(char.isdigit() for char in df["Name"].iloc[j][start+1:end]):
                                    df["Name"].iloc[j] = df["Name"].iloc[j][start+1:end]
                                else:
                                    df["Number"].iloc[j] = df["Name"].iloc[j][:start]
                                    df["Name"].iloc[j] = np.nan
                            else:
                                df["Name"].iloc[j] = df["Name"].iloc[j]
                        else:
                            df["Prov.Desig"].iloc[j] = df["Prov.Desig"].iloc[j][start+1:end]
                        if not isNaN(df["Name"].iloc[j]):
                            if ' ' in df["Name"].iloc[j]:
                                start = df["Name"].iloc[j].find(" ")
                                df["Number"].iloc[j] = df["Name"].iloc[j][:start]
                                df["Name"].iloc[j] = df["Name"].iloc[j][start+1:]
                            else:
                                df["Name"].iloc[j] = df["Name"].iloc[j]
                        else:
                            continue
                    else:
                        protolog("inf", "The asteroid {} has no name".format(df["Prov.Desig"].iloc[j]))
                        if "=" in sbdb["object"]["fullname"]:
                            df["Prov.Desig"].iloc[j] = sbdb["object"]["des"]
                            df["Number"].iloc[j] = np.nan
                            df["Name"].iloc[j] = np.nan
                        elif "(" in sbdb["object"]["fullname"]:
                            df['Prov.Desig'].iloc[j] = sbdb["object"]["fullname"]
                            start = df["Prov.Desig"].iloc[j].find("(")
                            end = df["Prov.Desig"].iloc[j].find(")")
                            df["Number"].iloc[j] = df["Prov.Desig"].iloc[j][:start]
                            df["Prov.Desig"].iloc[j] = df["Prov.Desig"].iloc[j][start+1:end]
                            df["Name"].iloc[j] = np.nan
                        else:
                            df['Prov.Desig'].iloc[j] = sbdb["object"]["fullname"]
                            df["Prov.Desig"].iloc[j] = df["Prov.Desig"].iloc[j]
                            df["Number"].iloc[j] = np.nan
                            df["Name"].iloc[j] = np.nan
                else:
                    continue
            except ValueError:
                print("Unable to retrieve the asteroid "
                      "{}".format(df["Prov.Desig"].iloc[j]))
                continue
    for i in range(len(df["Albedo"])):
        if "*" in df["Albedo"].iloc[i]:
            df["Albedo"].iloc[i] = df["Albedo"].iloc[i].replace("*", "")
            df["Approx A."].iloc[i] = "*"
        elif "::" in df["Albedo"].iloc[i]:
            df["Albedo"].iloc[i] = df["Albedo"].iloc[i].replace("::", "")
            df["Approx A."].iloc[i] = "::"
        elif ":" in df["Albedo"].iloc[i]:
            df["Albedo"].iloc[i] = df["Albedo"].iloc[i].replace(":", "")
            df["Approx A."].iloc[i] = ":"
        elif "?" in df["Albedo"].iloc[i]:
            df["Albedo"].iloc[i] = df["Albedo"].iloc[i].replace("?", "")
            df["Approx A."].iloc[i] = "?"
        else:
            continue
    return df
        
                