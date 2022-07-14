# -*- coding: utf-8 -*-
"""
Created on Wed May 18 12:18:44 2022

@author: pio-r
"""
import pandas as pd
import numpy as np
from astroquery.jplsbdb import SBDB
from tqdm import tqdm
from function.is_nan import isNaN
from function.protolog import protolog


def neowise_clean_dataset(NEO_URL):
    df_prova = []
    for i in range(0, len(NEO_URL)):
        URL = NEO_URL[i]
        NAME = ['Name',
                'Diam.',
                'Uncert.D.',
                'Albedo',
                'Upper A.',
                'Lower A.']
        COLWIDTH = [(0, 7), (20, 26), (27, 33), (34, 39), (40, 45), (46, 51)]
        try:
            temp_df = pd.read_fwf(URL, skiprows=36, names=NAME, colspecs=COLWIDTH, header=None,
                                  dtype='str', keep_default_na=False)
            temp_df = pd.DataFrame(temp_df, columns=("Number", "Name", "Prov.Desig",
                                                  "Albedo", "Lower A.", "Upper A.",
                                                  "Uncert.A.", "Approx A.",
                                                  "Diam.", "Lower D.", "Upper D.",
                                                  "Uncert.D.", "Approx D.",
                                                  "X", "Y", "Z", "Radar",
                                                  "Multiple System", "Ref."))
            temp_df["Albedo"] = temp_df["Albedo"].astype('float64')
            temp_df["Lower A."] = temp_df["Lower A."].astype('float64')
            temp_df["Upper A."] = temp_df["Upper A."].astype('float64')
            temp_df["Uncert.A."] = temp_df["Uncert.A."].astype('float64')
            temp_df["Diam."] = temp_df["Diam."].astype('float64')
            temp_df["Lower D."] = temp_df["Lower D."].astype('float64')
            temp_df["Upper D."] = temp_df["Upper D."].astype('float64')
            temp_df["Uncert.D."] = temp_df["Uncert.D."].astype('float64')
            for j in tqdm(range(len(temp_df['Name']))):
                try:
                    if not isNaN(temp_df["Number"].iloc[j]):
                        sbdb = SBDB.query(np.int(temp_df["Number"].iloc[j]))
                    else:
                        sbdb = SBDB.query(temp_df["Name"].iloc[j])
                    if "object" in sbdb:
                        if "shortname" in sbdb["object"]:
                            temp_df["Name"].iloc[j] = sbdb["object"]["shortname"]
                            temp_df["Prov.Desig"].iloc[j] = sbdb["object"]["fullname"]
                            start = temp_df["Prov.Desig"].iloc[j].find("(")
                            end = temp_df["Prov.Desig"].iloc[j].find(")")
                            if '=' in temp_df["Prov.Desig"].iloc[j][start+1:end]:
                                eq = temp_df["Prov.Desig"].iloc[j].find("=")
                                temp_df["Prov.Desig"].iloc[j] = temp_df["Prov.Desig"].iloc[j][start+1:eq-1]
                                if '(' in temp_df["Name"].iloc[j]:
                                    start = temp_df["Name"].iloc[j].find("(")
                                    end = temp_df["Name"].iloc[j].find(")")
                                    if not any(char.isdigit() for char in temp_df["Name"].iloc[j][start+1:end]):
                                        temp_df["Name"].iloc[j] = temp_df["Name"].iloc[j][start+1:end]
                                    else:
                                        temp_df["Number"].iloc[j] = temp_df["Name"].iloc[j][:start]
                                        temp_df["Name"].iloc[j] = np.nan
                                else:
                                    temp_df["Name"].iloc[j] = temp_df["Name"].iloc[j]
                            else:
                                temp_df["Prov.Desig"].iloc[j] = temp_df["Prov.Desig"].iloc[j][start+1:end]
                            if not isNaN(temp_df["Name"].iloc[j]):
                                if ' ' in temp_df["Name"].iloc[j]:
                                    start = temp_df["Name"].iloc[j].find(" ")
                                    temp_df["Number"].iloc[j] = temp_df["Name"].iloc[j][:start]
                                    temp_df["Name"].iloc[j] = temp_df["Name"].iloc[j][start+1:]
                                else:
                                    temp_df["Name"].iloc[j] = temp_df["Name"].iloc[j]
                            else:
                                continue
                        else:
                            protolog("inf", "The asteroid {} has no name".format(temp_df["Prov.Desig"].iloc[j]))
                            if "=" in sbdb["object"]["fullname"]:
                                temp_df["Prov.Desig"].iloc[j] = sbdb["object"]["des"]
                                temp_df["Number"].iloc[j] = np.nan
                                temp_df["Name"].iloc[j] = np.nan
                            elif "(" in sbdb["object"]["fullname"]:
                                temp_df['Prov.Desig'].iloc[j] = sbdb["object"]["fullname"]
                                start = temp_df["Prov.Desig"].iloc[j].find("(")
                                end = temp_df["Prov.Desig"].iloc[j].find(")")
                                temp_df["Number"].iloc[j] = temp_df["Prov.Desig"].iloc[j][:start]
                                temp_df["Prov.Desig"].iloc[j] = temp_df["Prov.Desig"].iloc[j][start+1:end]
                                temp_df["Name"].iloc[j] = np.nan
                            else:
                                temp_df['Prov.Desig'].iloc[j] = sbdb["object"]["fullname"]
                                temp_df["Prov.Desig"].iloc[j] = temp_df["Prov.Desig"].iloc[j]
                                temp_df["Number"].iloc[j] = np.nan
                                temp_df["Name"].iloc[j] = np.nan
                    else:
                        continue
                except ValueError:
                    print("Unable to retrieve the asteroid "
                          "{}".format(temp_df["Prov.Desig"].iloc[j]))
                    continue
            df_prova.append(temp_df)
        except ValueError:
            print('Probably the URL link for NEOWISE has been updated, go to: '
                  'https://doi.org/10.3847/PSJ/ab7820 or https://doi.org/10.3847/PSJ/ac15fb')

    df_NEOW = pd.concat(df_prova).reset_index(drop=True)

    list_non_neo = []
    idx = []
    for i in tqdm(range(len(df_NEOW["Name"]))):
        try:
            sbdb = SBDB.query(df_NEOW["Prov.Desig"].iloc[i])
            if "object" in sbdb:
                if not sbdb["object"]["neo"]:
                    list_non_neo.append(sbdb["object"]["fullname"])
                    idx.append(i)
                else:
                    continue
            elif "object" not in sbdb and not isNaN(df_NEOW["Number"].iloc[i]):
                sbdb = SBDB.query(df_NEOW["Number"].iloc[i])
                if not sbdb["object"]["neo"]:
                    list_non_neo.append(sbdb["object"]["fullname"])
                    idx.append(i)
                else:
                    continue
            else:
                continue
        except ValueError:
            continue

    # list_non_NEO, idx = are_there_NEO(df_NEOW)
    if len(list_non_neo) != 0:
        df_NEOW.drop(idx, axis=0, inplace=True)
    else:
        print('All the objects are NEOs')

    df_NEOW.reset_index(drop=True, inplace=True)

    idx = []

    neo = []

    for i in range(len(df_NEOW)):
        if not isNaN(df_NEOW["Name"]).iloc[i] and df_NEOW["Name"].iloc[i].startswith("a"):
            idx.append(i)
            neo.append(df_NEOW["Name"].iloc[i])

    for value in idx:
        df_NEOW.drop(value, inplace=True)

    df_NEOW = df_NEOW.reset_index(drop=True)
    return df_NEOW, idx, neo
