# -*- coding: utf-8 -*-
"""
Created on Mon May  9 13:39:51 2022

@author: pio-r
"""
import pandas as pd
import re
import numpy as np
from astroquery.jplsbdb import SBDB
from function.has_numbers import has_numbers
from function.is_nan import isNaN
from function.protolog import protolog
from function.start_space import start_space


def format_clean_dataset(df):
    i = 0
    while i < len(df["Taxon"]):
        if ";" in df["Taxon"].iloc[i]:
            string = df["Taxon"].iloc[i]
            result = re.split(";", string)
            for j in range(len(result)):
                if j == 0:
                    df["Taxon"].iloc[i] = result[0]
                else:
                    line = pd.DataFrame({"Number": df["Number"].iloc[i],
                                         "Name": df["Name"].iloc[i],
                                         "Prov.Desig": df["Prov.Desig"].iloc[i],
                                         "Taxon": result[j],
                                         "Approx.Value": df["Approx.Value"].iloc[i],
                                         "Ref": df["Ref"].iloc[i]}, index=[i])
                    df = pd.concat([df.iloc[:i], line,
                                    df.iloc[i:]]).reset_index(drop=True)
            i += 1
        elif '/' in df["Taxon"].iloc[i]:
            string = df["Taxon"].iloc[i]
            result = re.split("/", string)
            for j in range(len(result)):
                if j == 0:
                    df["Taxon"].iloc[i] = result[0]
                else:
                    line = pd.DataFrame({"Number": df["Number"].iloc[i],
                                         "Name": df["Name"].iloc[i],
                                         "Prov.Desig": df["Prov.Desig"].iloc[i],
                                         "Taxon": result[j],
                                         "Approx.Value": df["Approx.Value"].iloc[i],
                                         "Ref": df["Ref"].iloc[i]}, index=[i])
                    df = pd.concat([df.iloc[:i],
                                    line, df.iloc[i:]]).reset_index(drop=True)
            i += 1
        else:
            i += 1
            continue

    protolog("inf", 'Database extended in multiple rows for asteroids'
             ' with more Taxonomy values')

    for i in range(len(df["Taxon"])):
        if "_comp" in df["Taxon"].iloc[i]:
            df["Taxon"].iloc[i] = df["Taxon"].iloc[i].replace("_comp", "")
            df["Approx.Value"].iloc[i] = "Comp"
        elif "::" in df["Taxon"].iloc[i]:
            df["Taxon"].iloc[i] = df["Taxon"].iloc[i].replace("::", "")
            df["Approx.Value"].iloc[i] = "::"
        elif ":" in df["Taxon"].iloc[i]:
            df["Taxon"].iloc[i] = df["Taxon"].iloc[i].replace(":", "")
            df["Approx.Value"].iloc[i] = ":"
        elif "?" in df["Taxon"].iloc[i]:
            df["Taxon"].iloc[i] = df["Taxon"].iloc[i].replace("?", "")
            df["Approx.Value"].iloc[i] = "?"
        else:
            continue
    df = df.drop_duplicates().reset_index(drop=True)

    protolog("inf", "Database approximate values corrected")

    if all(isNaN(df["Name"].iloc[i]) for i in range(0, len(df["Name"]))):
        for i in range(len(df["Name"])):
            df["Name"].iloc[i] = df["Prov.Desig"].iloc[i]
    else:
        protolog("inf", "No need to copy the column 'Prov. Desig'"
                 " into the column 'Name'.")

    for i in range(0, len(df["Name"])):
        if not isNaN(df["Name"].iloc[i]) and has_numbers(df["Name"].iloc[i]):
            df["Name"].iloc[i] = np.nan
        else:
            continue

    protolog("inf", "Equal the rows of the Designation and the Name to"
             " correct that the value of the Name sometimes is in"
             " the Designation column.")

    for i in range(len(df["Name"])):
        if df["Name"].iloc[i] == df["Prov.Desig"].iloc[i] and isNaN(df["Number"].iloc[i]):
            try:
                sbdb = SBDB.query('{}'.format(df["Name"].iloc[i]))
                df["Number"].iloc[i] = np.int(sbdb["object"]["des"])
            except:
                print("Unable to retrieve the asteroid {}".format(df["Name"].iloc[i]))
        else:
            continue
    protolog("inf", "Retrieve the Number for the Asteroid that are"
             " doubled except for the Number")

    for i in range(len(df["Number"])):
        if isNaN(df["Name"].iloc[i]) and isNaN(df["Prov.Desig"].iloc[i]):
            try:
                sbdb = SBDB.query('{}'.format(df["Number"].iloc[i]))
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
                   df["Name"].iloc[i] = np.nan
                   df["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                   start = df["Prov.Desig"].iloc[i].find("(")
                   end = df["Prov.Desig"].iloc[i].find(")")
                   df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
                   if "des" in sbdb["object"] and "ABCDEFGHIJKLMNOPQRSTUVWXYZ" in sbdb["object"]["des"]:
                       df["Number"].iloc[i] = sbdb["object"]["des"]
                   else:
                       protolog('inf', 'No number for asteroid {}'.format(df["Prov.Desig"].iloc[i]))
                       df["Number"].iloc[i] = np.nan
            except:
                print("Unable to retrieve the asteroid {}".format(df["Number"].iloc[i]))
        else:
            continue

    df = df.drop_duplicates().reset_index(drop=True)

    for i in range(len(df["Name"])):
        if df["Name"].iloc[i] == df["Prov.Desig"].iloc[i]:
            try:
                sbdb = SBDB.query(np.int(df["Number"].iloc[i]))
                df["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                start = df["Prov.Desig"].iloc[i].find("(")
                end = df["Prov.Desig"].iloc[i].find(")")
                df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
            except:
                print("Unable to retrieve the"
                      " asteroid {}".format(df["Name"].iloc[i]))
        else:
            continue

    protolog("inf", "Retrieve the precise Designation for the problematic asteroids.")

    for i in range(len(df["Name"])):
        df["Name"].iloc[i] = start_space(df["Name"].iloc[i])
        df["Prov.Desig"].iloc[i] = start_space(df["Prov.Desig"].iloc[i])
        df["Taxon"].iloc[i] = start_space(df["Taxon"].iloc[i])
        df["Approx.Value"].iloc[i] = start_space(df["Approx.Value"].iloc[i])
        df["Ref"].iloc[i] = start_space(df["Ref"].iloc[i])

    protolog("inf", "Databes columns checked if thye start with whitespace"
             " and if it is they have been removed.")

    for i in range(len(df["Prov.Desig"])):
        if "(" in df["Prov.Desig"].iloc[i]:
            start = df["Prov.Desig"].iloc[i].find("(")
            end = df["Prov.Desig"].iloc[i].find(")")
            df["Number"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:end]
            start = df["Prov.Desig"].iloc[i].find(" ")
            df["Prov.Desig"].iloc[i] = df["Prov.Desig"].iloc[i][start+1:]
        else:
            continue

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
        print("Nothing to do")
    return df
