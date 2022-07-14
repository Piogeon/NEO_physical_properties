# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:26:28 2022

@author: pio-r
"""

import pandas as pd
from function.is_nan import isNaN
from astroquery.jplsbdb import SBDB


def format_spin_vector(df_sv):
    if "Number Name" not in df_sv.columns:
        df_sv.columns = df_sv.iloc[0]
        df_sv = df_sv[1:]
        df_sv = df_sv.reset_index(drop=True)
    else:
        pass

    for i in range(len(df_sv)):
        if "yyyymm/dd" in df_sv.columns:
            if not isNaN(df_sv["yyyymm/dd"].iloc[i]):
                if "*" in df_sv["yyyymm/dd"].iloc[i]:
                    ast = df_sv["yyyymm/dd"].iloc[i].find("*")
                    df_sv["LPAB"].iloc[i] = df_sv["yyyymm/dd"].iloc[i][ast+1:]
                else:
                    count = 0
                    for value in df_sv["yyyymm/dd"].iloc[i]:
                        if value == " ":
                            count += 1
                        else:
                            continue
                    if count > 1:
                        ws = df_sv["yyyymm/dd"].iloc[i].find(" ")
                        df_sv["yyyymm/dd"].iloc[i] = df_sv["yyyymm/dd"].iloc[i][ws+1:]
                        ws = df_sv["yyyymm/dd"].iloc[i].find(" ")
                        if " " in df_sv["yyyymm/dd"].iloc[i][ws+1:]:
                            ws_1 = df_sv["yyyymm/dd"].iloc[i][ws+1:].find(" ")
                            ws = ws + 1 + ws_1
                            df_sv["LPAB"].iloc[i] = df_sv["yyyymm/dd"].iloc[i][ws+1:]
                        else:
                            df_sv["LPAB"].iloc[i] = df_sv["yyyymm/dd"].iloc[i][ws+1:]
                    else:
                        continue

            else:
                continue
        else:
            continue

    try:
        df_sv = df_sv[["Number Name", "LPAB BPAB"]]
    except:
        df_sv = df_sv[["Number Name", "LPAB", "BPAB"]]

    # Drop NaN values

    try:
        nan_val = []
        for i in range(len(df_sv)):
            if (isNaN(df_sv["Number Name"].iloc[i]) and isNaN(df_sv["LPAB BPAB"].iloc[i])) or isNaN(df_sv["LPAB BPAB"].iloc[i]):
                nan_val.append(i)
            else:
                continue

        for value in nan_val:
            df_sv.drop(value, axis=0, inplace=True)

        df_sv = df_sv.reset_index(drop=True)
        # Create the df with the right formatting

        sv = pd.DataFrame(columns=["Number Name", "Name", "Prov.Desig", "LPAB BPAB", "BPAB", "Reference"])

        sv["Number Name"] = df_sv["Number Name"]
        sv["LPAB BPAB"] = df_sv["LPAB BPAB"]

        # Fill NaN value of Name/Number

        for i in range(1, len(sv)):
            if isNaN(sv["Number Name"].iloc[i]) and not isNaN(sv["LPAB BPAB"].iloc[i]):
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i-1]
            else:
                continue

        # Split Name Number column

        for i in range(len(sv)):
            ws = sv["Number Name"].iloc[i].find(" ")
            if all(char.isalpha() for char in sv["Number Name"].iloc[i][ws+1:].replace(" ", "")) and len(sv["Number Name"].iloc[i][ws+1:]) > 2:
                sv["Name"].iloc[i] = sv["Number Name"].iloc[i][ws+1:]
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i][:ws]
            elif " " in sv["Number Name"].iloc[i][ws+1:]:
                sv["Prov.Desig"].iloc[i] = sv["Number Name"].iloc[i][ws+1:]
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i][:ws]
            elif "’" in sv["Number Name"].iloc[i][ws+1:]:
                sv["Name"].iloc[i] = sv["Number Name"].iloc[i][ws+1:]
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i][:ws]
            else:
                sv["Prov.Desig"].iloc[i] = sv["Number Name"].iloc[i]
                sv["Number Name"].iloc[i] = ""

        sv.rename(columns={'Number Name': 'Number'}, inplace=True)

        # Split LPAB BPAB column

        for i in range(len(sv)):
            ws = sv["LPAB BPAB"].iloc[i].find(" ")
            sv["BPAB"].iloc[i] = sv["LPAB BPAB"].iloc[i][ws+1:]
            sv["LPAB BPAB"].iloc[i] = sv["LPAB BPAB"].iloc[i][:ws]

        sv.rename(columns={'LPAB BPAB': 'LPAB'}, inplace=True)

        # Find the Prov.Desig for NEO that have a Name and Number

        for i in range(len(sv)):
            if not (isNaN(sv["Number"].iloc[i]) and isNaN(sv["Name"].iloc[i])):
                if isNaN(sv["Prov.Desig"].iloc[i]):
                    sbdb = SBDB.query('{}'.format(sv["Number"].iloc[i]))
                    sv["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                    start = sv["Prov.Desig"].iloc[i].find("(")
                    end = sv["Prov.Desig"].iloc[i].find(")")
                    sv["Prov.Desig"].iloc[i] = sv["Prov.Desig"].iloc[i][start+1:end]
                else:
                    continue
            else:
                continue
    except:
        nan_val = []
        for i in range(len(df_sv)):
            if (isNaN(df_sv["Number Name"].iloc[i]) and isNaN(df_sv["LPAB"].iloc[i]) and isNaN(df_sv["BPAB"].iloc[i])) or (isNaN(df_sv["LPAB"].iloc[i]) and isNaN(df_sv["BPAB"].iloc[i])):
                nan_val.append(i)
            else:
                continue

        for value in nan_val:
            df_sv.drop(value, axis=0, inplace=True)

        df_sv = df_sv.reset_index(drop=True)

        # Create the df with the right formatting

        sv = pd.DataFrame(columns=["Number Name", "Name", "Prov.Desig", "LPAB", "BPAB", "Reference"])

        sv["Number Name"] = df_sv["Number Name"]
        sv["LPAB"] = df_sv["LPAB"]
        sv["BPAB"] = df_sv["BPAB"]

        # Fill NaN value of Name/Number

        for i in range(1, len(sv)):
            if isNaN(sv["Number Name"].iloc[i]) and not (isNaN(sv["LPAB"].iloc[i]) and isNaN(sv["BPAB"].iloc[i])):
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i-1]
            else:
                continue

        # Find if there is a sum of two tables with the row Number Name ... and remove it

        try:
            idx = sv.loc[sv["Number Name"] == "Number Name"].index
            sv.drop(idx[0], axis=0, inplace=True)
        except:
            print('No internal table')

        # Change the word revised and alternate

        for i in range(1, len(sv)):
            if "Revised" in sv["Number Name"].iloc[i] or "Alternate" in sv["Number Name"].iloc[i]:
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i-1]
            else:
                continue

        # Split Name Number column

        for i in range(len(sv)):
            ws = sv["Number Name"].iloc[i].find(" ")
            if (all(char.isalpha() for char in sv["Number Name"].iloc[i][ws+1:].replace(" ", "")) and len(sv["Number Name"].iloc[i][ws+1:]) > 2) or "-" in sv["Number Name"].iloc[i][ws+1:]:
                sv["Name"].iloc[i] = sv["Number Name"].iloc[i][ws+1:]
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i][:ws]
            elif " " in sv["Number Name"].iloc[i][ws+1:]:
                sv["Prov.Desig"].iloc[i] = sv["Number Name"].iloc[i][ws+1:]
                sv["Number Name"].iloc[i] = sv["Number Name"].iloc[i][:ws]
            else:
                sv["Prov.Desig"].iloc[i] = sv["Number Name"].iloc[i]
                sv["Number Name"].iloc[i] = ""

        sv.rename(columns={'Number Name': 'Number'}, inplace=True)

        # Find the Prov.Desig for NEO that have a Name and Number

        for i in range(len(sv)):
            if not (isNaN(sv["Number"].iloc[i]) and isNaN(sv["Name"].iloc[i])):
                if isNaN(sv["Prov.Desig"].iloc[i]):
                    sbdb = SBDB.query('{}'.format(sv["Number"].iloc[i]))
                    sv["Prov.Desig"].iloc[i] = sbdb["object"]["fullname"]
                    start = sv["Prov.Desig"].iloc[i].find("(")
                    end = sv["Prov.Desig"].iloc[i].find(")")
                    sv["Prov.Desig"].iloc[i] = sv["Prov.Desig"].iloc[i][start+1:end]
                else:
                    continue
            else:
                continue
    return sv
