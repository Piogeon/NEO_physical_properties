# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 08:53:09 2022

@author: pio-r
"""

import pandas as pd
import os

from function.are_there_NEO import are_there_NEO
from function.format_spin_vector import format_spin_vector
from function.write_fdf import write_fdf


# LOADING URLS FOR DATASETS FOR TAXONOMY
CSS3_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/CS3/')

NEAPS_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/Lowell Observatory NEAPS/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

REF_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/')

ref = pd.read_fwf(REF_URL + '/Reference.txt',
                  names=colname, colspecs=colwidth, header=None)
# CS3

numb = [1, 2, 3, 4, 5, 6, 12]

for i in range(len(numb)):
    if i == 0:
        df_sv = pd.read_csv(CSS3_URL + '/tabula-NEA Lightcurve Analysis at the Center for Solar System Studies_{}.csv'.format(numb[i]))
        df_CS3 = format_spin_vector(df_sv)
        df_CS3["Reference"] = ref["ID"][0][2:]

    else:
        df_sv = pd.read_csv(CSS3_URL + '/tabula-NEA Lightcurve Analysis at the Center for Solar System Studies_{}.csv'.format(numb[i]))
        sv_prova = format_spin_vector(df_sv)
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

for i in range(1, 5):
    if i == 1:
        df_sv = pd.read_csv(NEAPS_URL + '/tabula-Lowell Observatory Near-Earth Asteroid Photometric Survey (NEAPS) - {}.csv'.format(i))
        df_NEAPS = format_spin_vector(df_sv)

        df_NEAPS["LPAB"] = df_NEAPS["LPAB"].astype(str)
        df_NEAPS["BPAB"] = df_NEAPS["BPAB"].astype(str)

        for k in range(len(df_NEAPS)):
            if "." in df_NEAPS["LPAB"].iloc[k]:
                t = df_NEAPS["LPAB"].iloc[k].find(".")
                df_NEAPS["LPAB"].iloc[k] = df_NEAPS["LPAB"].iloc[k][:t]
            else:
                continue
        for k in range(len(df_NEAPS)):
            if "." in df_NEAPS["BPAB"].iloc[k]:
                t = df_NEAPS["BPAB"].iloc[k].find(".")
                df_NEAPS["BPAB"].iloc[k] = df_NEAPS["BPAB"].iloc[k][:t]
            else:
                continue

        for k in range(len(df_NEAPS)):
            if " " in df_NEAPS["LPAB"].iloc[k]:
                ws = df_NEAPS["LPAB"].iloc[k].find(" ")
                df_NEAPS["BPAB"].iloc[k] = df_NEAPS["LPAB"].iloc[k][ws+1:]
                df_NEAPS["LPAB"].iloc[k] = df_NEAPS["LPAB"].iloc[k][:ws]
            else:
                continue
        df_NEAPS["Reference"] = ref["ID"][6][2:]
    else:
        df_sv = pd.read_csv(NEAPS_URL + '/tabula-Lowell Observatory Near-Earth Asteroid Photometric Survey (NEAPS) - {}.csv'.format(i))
        sv = format_spin_vector(df_sv)

        sv["LPAB"] = sv["LPAB"].astype(str)
        sv["BPAB"] = sv["BPAB"].astype(str)

        for k in range(len(sv)):
            if "." in sv["LPAB"].iloc[k]:
                t = sv["LPAB"].iloc[k].find(".")
                sv["LPAB"].iloc[k] = sv["LPAB"].iloc[k][:t]
            else:
                continue
        for k in range(len(sv)):
            if "." in sv["BPAB"].iloc[k]:
                t = sv["BPAB"].iloc[k].find(".")
                sv["BPAB"].iloc[k] = sv["BPAB"].iloc[k][:t]
            else:
                continue

        for k in range(len(sv)):
            if " " in sv["LPAB"].iloc[k]:
                ws = sv["LPAB"].iloc[k].find(" ")
                sv["BPAB"].iloc[k] = sv["LPAB"].iloc[k][ws+1:]
                sv["LPAB"].iloc[k] = sv["LPAB"].iloc[k][:ws]
            else:
                continue
        if i == 2:
            sv["Reference"] = ref["ID"][6][2:]
        elif i == 3:
            sv["Reference"] = ref["ID"][7][2:]
        elif i == 4:
            sv["Reference"] = ref["ID"][7][2:]
        elif i == 5:
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

df_total["LPAB"] = df_total["LPAB"].astype(str)
df_total["BPAB"] = df_total["BPAB"].astype(str)

for i in range(len(df_total)):
    if "." in df_total["LPAB"].iloc[i]:
        t = df_total["LPAB"].iloc[i].find(".")
        df_total["LPAB"].iloc[i] = df_total["LPAB"].iloc[i][:t]
    else:
        continue

for i in range(len(df_total)):
    if "." in df_total["BPAB"].iloc[i]:
        t = df_total["BPAB"].iloc[i].find(".")
        df_total["BPAB"].iloc[i] = df_total["BPAB"].iloc[i][:t]
    else:
        continue

colspecs = [
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <5} ",
    "{: <5} ",
    "{: <4} "
    ]

write_fdf("./Output/Spin_vector.txt", df_total, colspecs)
