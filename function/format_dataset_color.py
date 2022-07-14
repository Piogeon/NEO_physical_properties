# -*- coding: utf-8 -*-
"""
Created on Wed May 11 12:10:00 2022

@author: pio-r
"""

import pandas as pd
import numpy as np
from astroquery.jplsbdb import SBDB
from function.has_numbers import has_numbers
from function.is_nan import isNaN
from function.protolog import protolog
from function.start_space import start_space


def format_dataset_color(df, df1):
    if "complex" in df1:
        i = 0
        df1 = df1.drop(columns=['complex', 'complex1', 'complex2', 'nc', 'DynClass'])
        dft = df1.T[2:]
        idx = 0

        while i < len(df["Name"]):
            for j in range(len(dft.index)):
                if j == 0:
                    line = pd.DataFrame({"Number": df["Number"].iloc[i],
                                         "Name": df["Name"].iloc[i],
                                         "Prov.Desig": df["Prov.Desig"].iloc[i],
                                         "Type": dft.index[j],
                                         "Value": dft[idx][j],
                                         "Ref": df["Ref"].iloc[i]}, index=[i])
                    df.loc[line.index, :] = line[:]
                elif j == 14:
                    line = pd.DataFrame({"Number": df["Number"].iloc[i],
                                         "Name": df["Name"].iloc[i],
                                         "Prov.Desig": df["Prov.Desig"].iloc[i],
                                         "Type": dft.index[j],
                                         "Value": dft[idx][j],
                                         "Ref": df["Ref"].iloc[i]}, index=[i])
                    df = pd.concat([df.iloc[:i], line,
                                    df.iloc[i:]]).reset_index(drop=True)
                    i += (j + 1)
                else:
                    line = pd.DataFrame({"Number": df["Number"].iloc[i],
                                         "Name": df["Name"].iloc[i],
                                         "Prov.Desig": df["Prov.Desig"].iloc[i],
                                         "Type": dft.index[j],
                                         "Value": dft[idx][j],
                                         "Ref": df["Ref"].iloc[i]}, index=[i])
                    df = pd.concat([df.iloc[:i], line,
                                    df.iloc[i:]]).reset_index(drop=True)
            idx += 1
    else:
        protolog("inf", "This is not the SkyMapper database")

    if all(isNaN(df["Name"].iloc[i]) for i in range(0, len(df["Name"]))):
        for i in range(len(df["Name"])):
            df["Name"].iloc[i] = df["Prov.Desig"].iloc[i]
    else:
        protolog("inf", "No need to copy the column 'Prov. Desig' into the column 'Name'.")

    for i in range(0, len(df["Name"])):
        if not isNaN(df["Name"].iloc[i]) and has_numbers(df["Name"].iloc[i]):
            df["Name"].iloc[i] = np.nan
        else:
            continue

    for i in range(len(df["Name"])):
        if df["Name"].iloc[i] == df["Prov.Desig"].iloc[i]:
            try:
                sbdb = SBDB.query(np.int(df["Number"].iloc[i]))
                df["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                start = df["Prov.Desig"].iloc[i].find("(")
                end = df["Prov.Desig"].iloc[i].find(")")
                df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
            except:
                print("Unable to retrieve the asteroid {}".format(df["Name"].iloc[i]))
        else:
            continue

    for i in range(len(df["Prov.Desig"])):
        if "(" in df["Prov.Desig"].iloc[i]:
            start = df["Prov.Desig"].iloc[i].find("(")
            end = df["Prov.Desig"].iloc[i].find(")")
            df["Number"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
            start = df["Prov.Desig"].iloc[i].find(" ")
            df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:]
        else:
            continue
    if not any("r-z" in df["Type"].iloc[i] for i in range(0, len(df["Type"]))):
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
                except:
                    print("Unable to retrieve the asteroid {}".format(df["Prov.Desig"].iloc[i]))
        else:
            protolog("inf", "Nothing to do")

    df["Value"] = df["Value"].replace(np.nan, " ")

    for i in range(len(df["Value"])):
        if "±" in np.str(df["Value"].iloc[i]):
            start = df["Value"].iloc[i].find("±")
            df["Uncert."].iloc[i] = df["Value"].iloc[i][start+1:]
            df["Value"].iloc[i] = df["Value"].iloc[i][:start]
        else:
            protolog("inf", "There is no uncertainty for asteroid {}".format(df["Prov.Desig"].iloc[i]))

    for i in range(len(df["Name"])):
        df["Name"].iloc[i] = start_space(df["Name"].iloc[i])
        df["Prov.Desig"].iloc[i] = start_space(df["Prov.Desig"].iloc[i])
        df["Uncert."].iloc[i] = start_space(df["Uncert."].iloc[i])
    return df
