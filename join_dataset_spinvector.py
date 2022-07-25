# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 14:11:30 2022

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

COLWIDTH = [(0, 6), (7, 35), (36, 48), (49, 63), (64, 79)]

COLNAME = ["Number", "Name", "Prov.Desig", "Spin Vector", "Ref"]

earn = pd.read_fwf(EARN_URL + 'spinvector.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None, skiprows=1, nrows=42,
                                  dtype='str', keep_default_na=False)

i = 0
while i < len(earn["Ref"]):
    if not isNaN(earn["Ref"].iloc[i]):
        if "," in earn["Ref"].iloc[i]:
            string = earn["Ref"].iloc[i]
            result = re.split(",", string)
            earn["Ref"].iloc[i] = result[0]
            if ";" in earn["Ref"].iloc[i]:
                string = earn["Ref"].iloc[i]
                result = re.split(";", string)
                earn["Ref"].iloc[i] = result[0]
            else:
                i += 1
        elif ";" in earn["Ref"].iloc[i]:
            string = earn["Ref"].iloc[i]
            result = re.split(";", string)
            earn["Ref"].iloc[i] = result[0]
            if "," in earn["Ref"].iloc[i]:
                string = earn["Ref"].iloc[i]
                result = re.split(",", string)
                earn["Ref"].iloc[i] = result[0]
            else:
                i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue
    
earn.insert(4,"BPAB", "")
earn.rename(columns = {'Spin Vector': 'LPAB'}, inplace = True)

for i in range(len(earn)):
    string = earn["LPAB"].iloc[i]
    result = re.split(",", string)
    eq_0 = result[0].find("=")
    earn["LPAB"].iloc[i] = result[0][eq_0+1:]
    eq_1  = result[1].find("=")
    earn["BPAB"].iloc[i] = result[1][eq_1+1:]

for i in range(len(earn)):
    if all(char.isdigit() for char in earn["Name"].iloc[i][:4]):
        earn["Name"].iloc[i] = ""
    else:
        continue
    
COLWIDTH = [(0, 7), (8, 36), (37, 49), (50, 55), (56, 61), (62, 66)]

COLNAME = ["Number", "Name", "Prov.Desig", "LPAB", "BPAB", "Ref"]

earn_new = pd.read_fwf(EARN_NEW_URL + 'spin_vector.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None,
                                  dtype='str', keep_default_na=False)

df_total = pd.concat([earn, earn_new]).reset_index(drop=True)
df_total.fillna('', inplace=True)


list_non_NEO, idx = are_there_NEO(df_total)

if len(list_non_NEO) != 0:
    df_total.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')
    
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
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <5} ",
    "{: <5} ",
    "{: <4} "
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/spin_vector_ALL.txt", df_total, colspecs)

