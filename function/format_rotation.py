# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 12:26:28 2022

@author: pio-r
"""

import pandas as pd
from function.is_nan import isNaN
from astroquery.jplsbdb import SBDB


def format_rotation(df_sv):
    if "Number Name" not in df_sv.columns:
        df_sv.columns = df_sv.iloc[0]
        df_sv = df_sv[1:]
        df_sv = df_sv.reset_index(drop=True)
    else:
        pass

    # Particular adjustment for table 5 because P.E. is joined with Amp

    if "P.E. Amp" in df_sv.columns:
        for i in range(len(df_sv)):
            if not isNaN(df_sv["P.E. Amp"].iloc[i]):
                if " " in df_sv["P.E. Amp"].iloc[i]:
                    ws = df_sv["P.E. Amp"].iloc[i].find(" ")
                    df_sv.at[i, "Amp"] = df_sv.at[i, "P.E. Amp"][ws+1:]
                    df_sv.at[i, "P.E. Amp"] = df_sv.at[i, "P.E. Amp"][:ws]
                else:
                    continue
            else:
                continue

    df_sv.rename(columns={'P.E. Amp': 'P.E.'}, inplace=True)

    try:
        df_sv = df_sv[["Number Name", "Period(h)", "P.E.", "Amp", "A.E."]]
    except:
        df_sv = df_sv[["Number Name", "Period(h)", "P.E.", "Amp A.E."]]

    try:
        # Drop NaN values

        nan_val = []
        for i in range(len(df_sv)):
            if (isNaN(df_sv["Number Name"].iloc[i]) and isNaN(df_sv["Period(h)"].iloc[i]) and isNaN(df_sv["Amp"].iloc[i])) or (isNaN(df_sv["Period(h)"].iloc[i] and isNaN(df_sv["Amp"].iloc[i]))):
                nan_val.append(i)
            else:
                continue

        for value in nan_val:
            df_sv.drop(value, axis=0, inplace=True)

        sv = pd.DataFrame(columns=["Number Name", "Name", "Prov.Desig", "Period(h)", "Lower P", "Upper P", "P.E.", "Approx.",
                                   "Quality", "Radar", "Multiple system", "Amp", "Lower A", "Upper A", "A.E.",
                                   "Approx. Amp", "Max", "Reference"])

        sv["Number Name"] = df_sv["Number Name"]
        sv["Period(h)"] = df_sv["Period(h)"]
        sv["P.E."] = df_sv["P.E."]
        sv["Amp"] = df_sv["Amp"]
        sv["A.E."] = df_sv["A.E."]
        sv = sv.reset_index(drop=True)
        # Fill NaN value of Name/Number

        for i in range(1, len(sv)):
            if isNaN(sv["Number Name"].iloc[i]) and (not isNaN(sv["Period(h)"].iloc[i]) or not isNaN(sv["Amp"].iloc[i])):
                sv.at[i, "Number Name"] = sv.at[i-1, "Number Name"]
            else:
                continue

        # Check if there are multiple system or approximations of the Period

        drp = []
        for i in range(1, len(sv)):
            if not isNaN(sv["Period(h)"].iloc[i]):
                if "P" in sv["Period(h)"].iloc[i]:
                    sv.at[i+1, "Multiple system"] = "B0"
                    drp.append(i)
                elif "A" in sv["Period(h)"].iloc[i]:
                    sv.at[i+1, "Approx."] = "a"
                    drp.append(i)
                else:
                    continue
            else:
                continue

        for value in drp:
            sv.drop(value, axis=0, inplace=True)

        sv = sv.reset_index(drop=True)

        # Change the word revised and alternate

        for i in range(1, len(sv)):
            if "Revised" in sv["Number Name"].iloc[i] or "Alternate" in sv["Number Name"].iloc[i]:
                sv.at[i, "Number Name"] = sv.at[i-1, "Number Name"]

            else:
                continue
        # Change if there is (satellite?)() in Number Name
        for i in range(1, len(sv)):
            if "(" in sv["Number Name"].iloc[i]:
                st = sv["Number Name"].iloc[i].find("(")
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:st-2]
            else:
                continue

        # Split Name Number column
        for i in range(len(sv)):
            ws = sv["Number Name"].iloc[i].find(" ")
            if all(char.isalpha() for char in sv["Number Name"].iloc[i][ws+1:].replace(" ", "")) and len(sv["Number Name"].iloc[i][ws+1:]) > 2:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif " " in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Prov.Desig"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif "’" in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif "-" in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            else:
                sv.at[i, "Prov.Desig"] = sv.at[i, "Number Name"]
                sv.at[i, "Number Name"] = ""

        sv.rename(columns={'Number Name': 'Number'}, inplace=True)

        # If there is "-" in Period remove it
        for i in range(len(sv)):
            if not isNaN(sv["Period(h)"].iloc[i]):
                if "-" in sv["Period(h)"].iloc[i]:
                    sv.at[i, "Period(h)"] = sv.at[i, "Period(h)"].replace("-", "")
                else:
                    continue
            else:
                continue
        # If there is "-" in Amp remove it
        for i in range(len(sv)):
            if not isNaN(sv["Amp"].iloc[i]):
                if "-" in sv["Amp"].iloc[i]:
                    sv.at[i, "Amp"] = sv.at[i, "Amp"].replace("-", "")
                else:
                    continue
            else:
                continue
        # If there is "-" in Amp remove it
        for i in range(len(sv)):
            if not isNaN(sv["P.E."].iloc[i]):
                if "-" in sv["P.E."].iloc[i]:
                    sv.at[i, "P.E."] = sv.at[i, "P.E."].replace("-", "")
                else:
                    continue
            else:
                continue
        # Check for lower limit or upper limit on Period

        for i in range(len(sv)):
            if not isNaN(sv["Period(h)"].iloc[i]):
                if ">" in sv["Period(h)"].iloc[i]:
                    lr = sv["Period(h)"].iloc[i].find(">")
                    sv.at[i, "Lower P"] = sv.at[i, "Period(h)"][lr+1:]
                    sv.at[i, "Period(h)"] = " "
                elif "<" in sv["Period(h)"].iloc[i]:
                    up = sv["Period(h)"].iloc[i].find("<")
                    sv.at[i, "Upper P"] = sv.at[i, "Period(h)"][up+1:]
                    sv.at[i, "Period(h)"] = " "
                else:
                    continue
            else:
                continue

        # Check for lower limit or upper limit on Amp

        for i in range(len(sv)):
            if not isNaN(sv["Amp"].iloc[i]):
                if ">" in sv["Amp"].iloc[i]:
                    lr = sv["Amp"].iloc[i].find(">")
                    sv.at[i, "Lower P"] = sv.at[i, "Amp"][lr+1:]
                    sv.at[i, "Amp"] = " "
                elif "<" in sv["Amp"].iloc[i]:
                    up = sv["Amp"].iloc[i].find("<")
                    sv.at[i, "Upper P"] = sv.at[i, "Amp"][up+1:]
                    sv.at[i, "Amp"] = " "
                else:
                    continue
            else:
                continue
        # Find the Prov.Desig for NEO that have a Name and Number

        for i in range(len(sv)):
            if not (isNaN(sv["Number"].iloc[i]) and isNaN(sv["Name"].iloc[i])):
                if isNaN(sv["Prov.Desig"].iloc[i]):
                    sbdb = SBDB.query('{}'.format(sv["Number"].iloc[i]))
                    sv.at[i, "Prov.Desig"] = sbdb["object"]["fullname"]
                    start = sv["Prov.Desig"].iloc[i].find("(")
                    end = sv["Prov.Desig"].iloc[i].find(")")
                    sv.at[i, "Prov.Desig"] = sv.at[i, "Prov.Desig"][start+1:end]
                else:
                    continue
            else:
                continue

        for i in range(len(sv)):
            if "A924 UB" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1924 TD"
            elif "A911 TB" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1911 MT"
            elif "A918 AA" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1918 DB"
            elif "A898 PA" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1898 DQ"
            else:
                continue
    except:
        # Drop NaN values

        nan_val = []
        for i in range(len(df_sv)):
            if (isNaN(df_sv["Number Name"].iloc[i]) and isNaN(df_sv["Period(h)"].iloc[i]) and isNaN(df_sv["Amp A.E."].iloc[i])) or (isNaN(df_sv["Period(h)"].iloc[i] and isNaN(df_sv["Amp A.E."].iloc[i]))):
                nan_val.append(i)
            else:
                continue

        for value in nan_val:
            df_sv.drop(value, axis=0, inplace=True)

        sv = pd.DataFrame(columns=["Number Name", "Name", "Prov.Desig", "Period(h)", "Lower P", "Upper P", "P.E.", "Approx.",
                                   "Quality", "Radar", "Multiple system", "Amp A.E.", "Lower A", "Upper A", "A.E.",
                                   "Approx. Amp", "Max", "Reference"])

        sv["Number Name"] = df_sv["Number Name"]
        sv["Period(h)"] = df_sv["Period(h)"]
        sv["P.E."] = df_sv["P.E."]
        sv["Amp A.E."] = df_sv["Amp A.E."]

        sv = sv.reset_index(drop=True)

        # Fill NaN value of Name/Number

        for i in range(1, len(sv)):
            if isNaN(sv["Number Name"].iloc[i]) and (not isNaN(sv["Period(h)"].iloc[i]) or not isNaN(sv["Amp A.E."].iloc[i])):
                sv.at[i, "Number Name"] = sv.at[i-1, "Number Name"]
            else:
                continue
        # Split Amp and A.E. columns

        for i in range(len(sv)):
            if not isNaN(sv["Amp A.E."].iloc[i]):
                if " " in sv["Amp A.E."].iloc[i]:
                    ws = sv["Amp A.E."].iloc[i].find(" ")
                    sv.at[i, "A.E."] = sv.at[i, "Amp A.E."][ws+1:]
                    sv.at[i, "Amp A.E."] = sv.at[i, "Amp A.E."][:ws]
                else:
                    continue
            else:
                continue

        sv.rename(columns={'Amp A.E.': 'Amp'}, inplace=True)

        # Check if there are particular approx value for period or approx values

        drp = []
        for i in range(1, len(sv)):
            if not isNaN(sv["Period(h)"].iloc[i]):
                if "P" in sv["Period(h)"].iloc[i]:
                    sv.at[i+1, "Multiple system"] = "B0"
                    drp.append(i)
                elif "A" in sv["Period(h)"].iloc[i]:
                    sv.at[i+1, "Approx."] = "a"
                    drp.append(i)
                else:
                    continue
            else:
                continue

        for value in drp:
            sv.drop(value, axis=0, inplace=True)

        sv = sv.reset_index(drop=True)

        # Find if there is a sum of two tables with the row Number Name ... and remove it

        try:
            idx = sv.loc[sv["Number Name"] == "Number Name"].index
            sv.drop(idx[0], axis=0, inplace=True)
        except:
            print('No internal table')

        # Change the word revised and alternate

        for i in range(1, len(sv)):
            if "Revised" in sv["Number Name"].iloc[i] or "Alternate" in sv["Number Name"].iloc[i]:
                sv.at[i, "Number Name"] = sv.at[i-1, "Number Name"]
            else:
                continue

        # Split Name Number column
        for i in range(len(sv)):
            ws = sv["Number Name"].iloc[i].find(" ")
            if all(char.isalpha() for char in sv["Number Name"].iloc[i][ws+1:].replace(" ", "")) and len(sv["Number Name"].iloc[i][ws+1:]) > 2:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif " " in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Prov.Desig"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif "’" in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            elif "-" in sv["Number Name"].iloc[i][ws+1:]:
                sv.at[i, "Name"] = sv.at[i, "Number Name"][ws+1:]
                sv.at[i, "Number Name"] = sv.at[i, "Number Name"][:ws]
            else:
                sv.at[i, "Prov.Desig"] = sv.at[i, "Number Name"]
                sv.at[i, "Number Name"] = ""
        sv.rename(columns={'Number Name': 'Number'}, inplace=True)

        # Check for lower limit or upper limit on Period

        for i in range(len(sv)):
            if not isNaN(sv["Period(h)"].iloc[i]):
                if ">" in sv["Period(h)"].iloc[i]:
                    lr = sv["Period(h)"].iloc[i].find(">")
                    sv.at[i, "Lower P"] = sv.at[i, "Period(h)"][lr+1:]
                    sv.at[i, "Period(h)"] = " "
                elif "<" in sv["Period(h)"].iloc[i]:
                    up = sv["Period(h)"].iloc[i].find("<")
                    sv.at[i, "Upper P"] = sv.at[i, "Period(h)"][up+1:]
                    sv.at[i, "Period(h)"] = " "
                else:
                    continue
            else:
                continue

        # Check for lower limit or upper limit on Amp

        for i in range(len(sv)):
            if not isNaN(sv["Amp"].iloc[i]):
                if ">" in sv["Amp"].iloc[i]:
                    lr = sv["Amp"].iloc[i].find(">")
                    sv.at[i, "Lower P"] = sv.at[i, "Amp"][lr+1:]
                    sv.at[i, "Amp"] = " "
                elif "<" in sv["Amp"].iloc[i]:
                    up = sv["Amp"].iloc[i].find("<")
                    sv.at[i, "Upper P"] = sv.at[i, "Amp"][up+1:]
                    sv.at[i, "Amp"] = " "
                else:
                    continue
            else:
                continue

        # Find the Prov.Desig for NEO that have a Name and Number

        for i in range(len(sv)):
            if not (isNaN(sv["Number"].iloc[i]) and isNaN(sv["Name"].iloc[i])):
                if isNaN(sv["Prov.Desig"].iloc[i]):
                    sbdb = SBDB.query('{}'.format(sv["Number"].iloc[i]))
                    sv.at[i, "Prov.Desig"] = sbdb["object"]["fullname"]
                    start = sv["Prov.Desig"].iloc[i].find("(")
                    end = sv["Prov.Desig"].iloc[i].find(")")
                    sv.at[i, "Prov.Desig"] = sv.at[i, "Prov.Desig"][start+1:end]
                else:
                    continue
            else:
                continue
        for i in range(len(sv)):
            if "A924 UB" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1924 TD"
            elif "A911 TB" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1911 MT"
            elif "A918 AA" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1918 DB"
            elif "A898 PA" in sv["Prov.Desig"].iloc[i]:
                sv.at[i, "Prov.Desig"] = "1898 DQ"
            else:
                continue
    return sv
