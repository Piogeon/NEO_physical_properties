# -*- coding: utf-8 -*-
"""
Created on Mon May 23 10:43:33 2022

@author: pio-r
"""

import pandas as pd

from function.is_nan import isNaN
from function.format_rotation import format_rotation
from function.are_there_NEO import are_there_NEO
from function.write_fdf import write_fdf


# LOADING URLS FOR DATASETS FOR TAXONOMY
CSS3_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/CS3/'

NEAPS_URL = ('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article'
             '/Lowell Observatory NEAPS/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

ref = pd.read_fwf('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/'
                  'Programs/Primary_Pipelines/Reference.txt',
                  names=colname, colspecs=colwidth, header=None)
# CS3


numb = [1, 2, 3, 4, 5, 6, 12]

for i in range(len(numb)):
    if i == 0:
        df_sv = pd.read_csv(CSS3_URL + 'tabula-NEA Lightcurve Analysis at the Center for Solar System Studies_{}.csv'.format(numb[i]), float_precision='round_trip', dtype='str')
        df_CS3 = format_rotation(df_sv)
        df_CS3["Reference"] = ref["ID"][0][2:]

    else:
        df_sv = pd.read_csv(CSS3_URL + 'tabula-NEA Lightcurve Analysis at the Center for Solar System Studies_{}.csv'.format(numb[i]),  float_precision='round_trip', dtype='str')
        sv_prova = format_rotation(df_sv)
        if i == 1:
            sv_prova["Reference"] = ref["ID"][1][2:]
        elif i == 2:
            sv_prova["Reference"] = ref["ID"][2][2:]
        elif i == 3:
            sv_prova["Reference"] = ref["ID"][4][2:]
        elif i == 4:
            sv_prova["Reference"] = ref["ID"][3][2:]
        elif i == 5:
            sv_prova["Reference"] = ref["ID"][9][2:]
        elif i == 6:
            sv_prova["Reference"] = ref["ID"][16][2:]
        df_CS3 = pd.concat([df_CS3, sv_prova])

list_non_NEO, idx = are_there_NEO(df_CS3)

if len(list_non_NEO) != 0:
    df_CS3.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

# NEAPS

for k in range(1, 5):
    if k == 1:
        df_sv = pd.read_csv(NEAPS_URL + 'tabula-Lowell Observatory Near-Earth Asteroid Photometric Survey (NEAPS) - {}.csv'.format(k),  float_precision='round_trip', dtype='str')
        df_sv.rename(columns={'Period (h)': 'Period(h)'}, inplace=True)

        # Clean the column if there are other useless information

        for i in range(len(df_sv)):
            if not isNaN(df_sv.at[i, "Amp A.E."]):
                if " " in df_sv.at[i, "Amp A.E."]:
                    ws = df_sv.at[i, "Amp A.E."].find(" ")
                    if " " in df_sv.at[i, "Amp A.E."][ws+1:]:
                        ws_1 = df_sv.at[i, "Amp A.E."][ws+1:].find(" ")
                        df_sv.at[i, "Amp A.E."] = df_sv.at[i, "Amp A.E."][:ws+1+ws_1]
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # Drop NaN values
        drp = []
        for i in range(len(df_sv)):
            if isNaN(df_sv.at[i, "Period(h)"]) and isNaN(df_sv.at[i, "Amp A.E."]):
                drp.append(i)
            else:
                continue
        df_sv.drop(drp, axis=0, inplace=True)

        df_sv = df_sv.reset_index(drop=True)

        df_NEAPS = format_rotation(df_sv)

        drp = []
        for i in range(len(df_NEAPS)-1):
            if "T" in df_NEAPS.at[i, "Period(h)"]:
                drp.append(i)
                df_NEAPS.at[i+1, "Approx."] = "T"
            else:
                continue
        df_NEAPS.drop(drp, axis=0, inplace=True)

        df_NEAPS = df_NEAPS.reset_index(drop=True)

        df_NEAPS["Reference"] = ref["ID"][6][2:]

    else:
        df_sv = pd.read_csv(NEAPS_URL + 'tabula-Lowell Observatory Near-Earth Asteroid Photometric Survey (NEAPS) - {}.csv'.format(k),  float_precision='round_trip', dtype='str')

        #

        data = []
        if "P.E. Amp A.E." in df_sv.columns:
            for i in range(len(df_sv)):
                if not isNaN(df_sv.at[i, "P.E. Amp A.E."]):
                    if " " in df_sv.at[i, "P.E. Amp A.E."]:
                        ws = df_sv.at[i, "P.E. Amp A.E."].find(" ")
                        data.append(df_sv.at[i, "P.E. Amp A.E."][ws+1:])
                        df_sv.at[i, "P.E. Amp A.E."] = df_sv.at[i, "P.E. Amp A.E."][:ws]
                    else:
                        continue
                else:
                    data.append(" ")

        if 'P.E. Amp A.E.' in df_sv.columns:
            df_sv.insert(8, 'Amp A.E.', value=data)
            df_sv.rename(columns={'P.E. Amp A.E.': 'P.E.'}, inplace=True)

        # Divede the column "Period(h) P.E."

        data = []
        for i in range(len(df_sv)):
            if 'Period (h) P.E.' in df_sv.columns:
                if not isNaN(df_sv.at[i, "Period (h) P.E."]):
                    if " " in df_sv.at[i, "Period (h) P.E."]:
                        ws = df_sv.at[i, "Period (h) P.E."].find(" ")
                        data.append(df_sv.at[i, "Period (h) P.E."][ws+1:])
                        df_sv.at[i, "Period (h) P.E."] = df_sv.at[i, "Period (h) P.E."][:ws]
                    else:
                        continue
                else:
                    data.append(" ")
                    continue
            else:
                continue

        if 'Period (h) P.E.' in df_sv.columns:
            df_sv.insert(8, 'P.E.', value=data)
            df_sv.rename(columns={'Period (h) P.E.': 'Period(h)'}, inplace=True)

        data = []
        for i in range(len(df_sv)):
            if 'Period(h) P.E.' in df_sv.columns:
                if not isNaN(df_sv.at[i, "Period(h) P.E."]):
                    if " " in df_sv.at[i, "Period(h) P.E."]:
                        ws = df_sv.at[i, "Period(h) P.E."].find(" ")
                        data.append(df_sv.at[i, "Period(h) P.E."][ws+1:])
                        df_sv.at[i, "Period(h) P.E."] = df_sv.at[i, "Period(h) P.E."][:ws]
                    else:
                        continue
                else:
                    data.append(" ")
                    continue
            else:
                continue

        if 'Period(h) P.E.' in df_sv.columns:
            df_sv.insert(7, 'P.E.', value=data)
            df_sv.rename(columns={'Period(h) P.E.': 'Period(h)'}, inplace=True)

        data = []

        if not "Amp A.E." in df_sv.columns and "A.E. Grp" in df_sv.columns:
            for i in range(len(df_sv)):
                if "." in df_sv.at[i, "A.E. Grp"]:
                    ws = df_sv.at[i, "A.E. Grp"].find(" ")
                    data.append(df_sv.at[i, "A.E. Grp"][:ws])
                else:
                    data.append("")
        if 'A.E. Grp' in df_sv.columns:
            df_sv.insert(9, 'A.E.', value=data)
            df_sv.rename(columns={'A.E. Grp': 'Grp'}, inplace=True)

        # Check if there are more than expected values in the column P.E.
        for i in range(len(df_sv)):
            if "Amp A.E." in df_sv.columns:
                if not isNaN(df_sv.at[i, "P.E."]):
                    if " " in df_sv.at[i, "P.E."] and isNaN(df_sv.at[i, "Amp A.E."]):
                        ws = df_sv.at[i, "P.E."].find(" ")
                        df_sv.at[i, "Amp A.E."] = df_sv.at[i, "P.E."][ws+1:]
                        df_sv.at[i, "P.E."] = df_sv.at[i, "P.E."][:ws]
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # Clean the column if there are other useless information

        for i in range(len(df_sv)):
            if "Amp A.E." in df_sv.columns:
                if not isNaN(df_sv.at[i, "Amp A.E."]):
                    if " " in df_sv.at[i, "Amp A.E."]:
                        ws = df_sv.at[i, "Amp A.E."].find(" ")
                        if " " in df_sv.at[i, "Amp A.E."][ws+1:]:
                            ws_1 = df_sv.at[i, "Amp A.E."][ws+1:].find(" ")
                            df_sv.at[i, "Amp A.E."] = df_sv.at[i, "Amp A.E."][:ws+1+ws_1]
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # Drop NaN values
        drp = []
        for i in range(len(df_sv)):
            if "Amp A.E." in df_sv.columns:
                if (isNaN(df_sv.at[i, "Period(h)"]) and isNaN(df_sv.at[i, "Amp A.E."])):
                    drp.append(i)
                else:
                    continue
            else:
                continue

        df_sv.drop(drp, axis=0, inplace=True)

        df_sv = df_sv.reset_index(drop=True)

        drp = []

        for i in range(len(df_sv)):
            if "Amp A.E." in df_sv.columns:
                if (df_sv.at[i, "P.E."] == "" and df_sv.at[i, "Amp A.E."] == ""):
                    drp.append(i)
                else:
                    continue
            else:
                continue
        df_sv.drop(drp, axis=0, inplace=True)

        df_sv = df_sv.reset_index(drop=True)

        sv = format_rotation(df_sv)

        drp = []
        for i in range(len(sv)-1):
            if not isNaN(sv.at[i, "Period(h)"]):
                if "T" in sv.at[i, "Period(h)"]:
                    drp.append(i)
                    sv.at[i+1, "Approx."] = "T"
                elif "?" in sv.at[i, "P.E."] and "?" in sv.at[i, "A.E."]:
                    sv.at[i, "P.E."] = ""
                    sv.at[i, "A.E."] = ""
                    continue
            else:
                continue
        sv.drop(drp, axis=0, inplace=True)

        sv = sv.reset_index(drop=True)

        drp = []
        for i in range(len(sv)):
            if isNaN(sv.at[i, "Period(h)"]) and isNaN(sv.at[i, "Amp"]):
                drp.append(i)
            else:
                continue
        sv.drop(drp, axis=0, inplace=True)

        sv = sv.reset_index(drop=True)

        drp = []
        for i in range(len(sv)):
            if isNaN(sv.at[i, "Period(h)"]) and sv.at[i, "Amp"] == "":
                drp.append(i)
            else:
                continue
        sv.drop(drp, axis=0, inplace=True)

        sv = sv.reset_index(drop=True)

        for i in range(len(sv)):
            if not isNaN(sv.at[i, "P.E."]):
                if " " in sv.at[i, "P.E."] and isNaN(sv.at[i, "Amp"]):
                    ws = sv.at[i, "P.E."].find(" ")
                    sv.at[i, "Amp"] = sv.at[i, "P.E."][ws+1:]
                    sv.at[i, "P.E."] = sv.at[i, "P.E."][:ws]
                elif sv.at[i, "P.E."].startswith(" "):
                    ws = sv.at[i, "P.E."].find(" ")
                    sv.at[i, "P.E."] = sv.at[i, "P.E."][ws+1:]
                else:
                    continue
            else:
                continue

        if k == 2:
            sv["Reference"] = ref["ID"][6][2:]
        elif k == 3:
            sv["Reference"] = ref["ID"][7][2:]
        elif k == 4:
            sv["Reference"] = ref["ID"][7][2:]
        elif k == 5:
            sv["Reference"] = ref["ID"][7][2:]

        df_NEAPS = pd.concat([df_NEAPS, sv])

df_NEAPS = df_NEAPS.reset_index(drop=True)

list_non_NEO, idx = are_there_NEO(df_NEAPS)

if len(list_non_NEO) != 0:
    df_NEAPS.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

# Merge dataset

df_total = pd.concat([df_CS3, df_NEAPS]).reset_index(drop=True)
df_total.fillna('', inplace=True)

for i in range(len(df_total)):
    if "A924 UB" in df_total["Prov.Desig"].iloc[i]:
        df_total["Prov.Desig"].iloc[i] = "1924 TD"
    elif "A911 TB" in df_total["Prov.Desig"].iloc[i]:
        df_total["Prov.Desig"].iloc[i] = "1911 MT"
    elif "A918 AA" in df_total["Prov.Desig"].iloc[i]:
        df_total["Prov.Desig"].iloc[i] = "1918 DB"
    elif "A898 PA" in df_total["Prov.Desig"].iloc[i]:
        df_total["Prov.Desig"].iloc[i] = "1898 DQ"
    else:
        continue

df_total = df_total.sort_values("Prov.Desig").reset_index(drop=True)


colspecs = [
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <10} ",
    "{: <10} ",
    "{: <10} ",
    "{: <10} ",
    "{: <5} ",
    "{: <2} ",
    "{: <5} ",
    "{: <3} ",
    "{: <5} ",
    "{: <5} ",
    "{: <5} ",
    "{: <7} ",
    "{: <5} ",
    "{: <8} ",
    "{: <2} "
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/rotation.txt", df_total, colspecs)
