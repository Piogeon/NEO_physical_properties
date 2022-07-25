# -*- coding: utf-8 -*-
"""
Created on Mon May 23 14:44:29 2022

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

COLWIDTH = [(0, 7), (7, 36), (36, 51), (51, 60), (60, 65)]

COLNAME = ["Number", "Name", "Prov.Desig", "Taxon", "Ref"]

earn = pd.read_fwf(EARN_URL + 'taxonomy.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None, skiprows=1, nrows=829)

df_earn_old = pd.DataFrame(earn, columns=("Number", "Name", "Prov.Desig",
                                    "Taxon", "Approx.Value", "Ref"))

for i in range(len(df_earn_old["Taxon"])):
    if "comp" in df_earn_old["Taxon"].iloc[i]:
        df_earn_old["Taxon"].iloc[i] = df_earn_old["Taxon"].iloc[i].replace("comp", "")
        df_earn_old["Approx.Value"].iloc[i] = "Comp"
    elif "::" in df_earn_old["Taxon"].iloc[i]:
        df_earn_old["Taxon"].iloc[i] = df_earn_old["Taxon"].iloc[i].replace("::", "")
        df_earn_old["Approx.Value"].iloc[i] = "::"
    elif ":" in df_earn_old["Taxon"].iloc[i]:
        df_earn_old["Taxon"].iloc[i] = df_earn_old["Taxon"].iloc[i].replace(":", "")
        df_earn_old["Approx.Value"].iloc[i] = ":"
    elif "?" in df_earn_old["Taxon"].iloc[i]:
        df_earn_old["Taxon"].iloc[i] = df_earn_old["Taxon"].iloc[i].replace("?", "")
        df_earn_old["Approx.Value"].iloc[i] = "?"
    elif "-" in df_earn_old["Taxon"].iloc[i]:
        df_earn_old["Taxon"].iloc[i] = df_earn_old["Taxon"].iloc[i].replace("-", "")
        df_earn_old["Approx.Value"].iloc[i] = "-"
    else:
        continue
df_earn_old = df_earn_old.drop_duplicates().reset_index(drop=True)


i = 0
while i < len(df_earn_old["Taxon"]):
    if ";" in df_earn_old["Taxon"].iloc[i]:
        string = df_earn_old["Taxon"].iloc[i]
        result = re.split(";", string)
        for j in range(len(result)):
            if j == 0:
                df_earn_old["Taxon"].iloc[i] = result[0]
            else:
                line = pd.DataFrame({"Number": df_earn_old["Number"].iloc[i],
                                     "Name": df_earn_old["Name"].iloc[i],
                                     "Prov.Desig": df_earn_old["Prov.Desig"].iloc[i],
                                     "Taxon": result[j],
                                     "Approx.Value": df_earn_old["Approx.Value"].iloc[i],
                                     "Ref": df_earn_old["Ref"].iloc[i]}, index=[i])
                df_earn_old = pd.concat([df_earn_old.iloc[:i], line,
                                df_earn_old.iloc[i:]]).reset_index(drop=True)
        i += 1
    elif '/' in df_earn_old["Taxon"].iloc[i]:
        string = df_earn_old["Taxon"].iloc[i]
        result = re.split("/", string)
        for j in range(len(result)):
            if j == 0:
                df_earn_old["Taxon"].iloc[i] = result[0]
            else:
                line = pd.DataFrame({"Number": df_earn_old["Number"].iloc[i],
                                     "Name": df_earn_old["Name"].iloc[i],
                                     "Prov.Desig": df_earn_old["Prov.Desig"].iloc[i],
                                     "Taxon": result[j],
                                     "Approx.Value": df_earn_old["Approx.Value"].iloc[i],
                                     "Ref": df_earn_old["Ref"].iloc[i]}, index=[i])
                df_earn_old = pd.concat([df_earn_old.iloc[:i],
                                line, df_earn_old.iloc[i:]]).reset_index(drop=True)
        i += 1
    else:
        i += 1
        continue

for i in range(len(df_earn_old)):
    if any(char.isdigit() for char in df_earn_old["Name"].iloc[i]):
        df_earn_old["Name"].iloc[i] = np.nan
    else:
        continue
    
COLWIDTH = [(0, 7), (8, 36), (37, 49), (50, 54), (55, 59), (60, 63)]

COLNAME = ["Number", "Name", "Prov.Desig", "Taxon", "Approx.Value", "Ref"]

earn_new = pd.read_fwf(EARN_NEW_URL + 'taxonomy.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None)

df_total = pd.concat([df_earn_old, earn_new]).reset_index(drop=True)
df_total.fillna('', inplace=True)

list_non_NEO, idx = are_there_NEO(df_total)

if len(list_non_NEO) != 0:
    df_total.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_total.reset_index(drop=True, inplace=True)

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
#df_total = df_total.drop_duplicates(['Prov.Desig','Taxon','Approx.Value'], keep='last')

colspecs = [
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <4} ",
    "{: <4} ",
    "{: <2} ",
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/taxonomy_ALL.txt", df_total, colspecs)

protolog("inf", "Taxonomy database ready")
