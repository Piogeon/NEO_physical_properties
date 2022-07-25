# -*- coding: utf-8 -*-
"""
Created on Tue May 24 11:07:39 2022

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
from function.write_fdf import write_fdf
from function.are_there_NEO import are_there_NEO

EARN_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/EARN/D5_EARN_data/D5_EARN_data/'
EARN_NEW_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/'

COLWIDTH = [(0, 6), (7, 35), (36, 48), (49, 58), (59, 74), (75, 84), (85, 100), (101, 110), (111, 126), (127, 136), (137, 160)]

COLNAME = ["Number", "Name", "Prov.Desig", "U-V", "Ref 1", "B-V", "Ref 2", "V-R", "Ref 3", "R-I", "Ref 4"]

earn = pd.read_fwf(EARN_URL + 'color.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None, skiprows=1, nrows=315)

df_1 = pd.DataFrame(earn, columns=["Number", "Name", "Prov.Desig", "U-V", "Value", "Ref 1"])
df_1["Value"] = df_1["U-V"]
df_1["U-V"] = 'U-V'

df_1.rename(columns={'U-V': 'Type', 'Ref 1': 'Ref'},
          inplace=True)

df_2 = pd.DataFrame(earn, columns=["Number", "Name", "Prov.Desig", "B-V", "Value", "Ref 2"])
df_2["Value"] = df_2["B-V"]
df_2["B-V"] = 'B-V'

df_2.rename(columns={'B-V': 'Type', 'Ref 2': 'Ref'},
          inplace=True)

df_3 = pd.DataFrame(earn, columns=["Number", "Name", "Prov.Desig", "V-R", "Value", "Ref 3"])
df_3["Value"] = df_3["V-R"]
df_3["V-R"] = 'V-R'

df_3.rename(columns={'V-R': 'Type', 'Ref 3': 'Ref'},
          inplace=True)

df_4 = pd.DataFrame(earn, columns=["Number", "Name", "Prov.Desig", "R-I", "Value", "Ref 4"])
df_4["Value"] = df_4["R-I"]
df_4["R-I"] = 'R-I'

df_4.rename(columns={'R-I': 'Type', 'Ref 4': 'Ref'},
          inplace=True)

df_earn_old = pd.concat([df_1, df_2, df_3, df_4]).reset_index(drop=True)

for i in range(len(df_earn_old)):
    if any(char.isdigit() for char in df_earn_old["Name"].iloc[i]):
        df_earn_old["Name"].iloc[i] = np.nan
    else:
        continue
    
i = 0
while i < len(df_earn_old["Ref"]):
    if not isNaN(df_earn_old["Ref"].iloc[i]):
        if "," in df_earn_old["Ref"].iloc[i]:
            string = df_earn_old["Ref"].iloc[i]
            result = re.split(",", string)
            df_earn_old["Ref"].iloc[i] = result[0]
            i += 1
        elif ";" in df_earn_old["Ref"].iloc[i]:
            string = df_earn_old["Ref"].iloc[i]
            result = re.split(";", string)
            df_earn_old["Ref"].iloc[i] = result[0]
            i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue
df_earn_old = pd.DataFrame(df_earn_old, columns=["Number", "Name", "Prov.Desig", "Type", "Value", "Lower", "Upper", "Uncert", "Ref"])
    
COLWIDTH = [(0, 7), (8, 36), (37, 49), (50, 53), (54, 61), (62, 69), (70, 77), (78, 85), (86, 89)]

COLNAME = ["Number", "Name", "Prov.Desig", "Type", "Value", "Lower", "Upper", "Uncert", "Ref"]

earn_new = pd.read_fwf(EARN_NEW_URL + 'color.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None)

df_total = pd.concat([df_earn_old, earn_new]).reset_index(drop=True)
df_total.fillna('', inplace=True)

list_non_NEO, idx = are_there_NEO(df_total)

if len(list_non_NEO) != 0:
    df_total.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_total.reset_index(drop=True, inplace=True)
df_total = df_total.sort_values("Name").reset_index(drop=True)

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


i = 0

while i < len(df_total):
    idx = df_total.loc[df_total["Prov.Desig"] == df_total["Prov.Desig"].iloc[i]].index
    df_test = df_total.loc[df_total["Prov.Desig"] == df_total["Prov.Desig"].iloc[i]]
    df_test = df_test.sort_values("Ref")
    df_test.set_index(idx, drop=True, append=False, inplace=True, verify_integrity=False)
    df_total.iloc[idx[0]:idx[-1]+1] = df_test
    i = idx[-1] + 1


colspecs = [
    "{: <7} ",
    "{: <28} ",
    "{: <12} ",
    "{: <3} ",
    "{: <7} ",
    "{: <7} ",
    "{: <7} ",
    "{: <7} ",
    "{: <3} "
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/Color_ALL.txt", df_total, colspecs)

protolog("inf", "Color database ready")

