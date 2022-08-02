# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 10:12:24 2022

@author: pio-r
"""

import pandas as pd
import re
import numpy as np
import os
from astroquery.jplsbdb import SBDB
from function.has_numbers import has_numbers
from function.is_nan import isNaN
from function.protolog import protolog
from function.start_space import start_space
from function.write_fdf import write_fdf
from function.are_there_NEO import are_there_NEO

EARN_URL = os.path.dirname('./Old_EARN/')
EARN_NEW_URL = os.path.dirname('./Output/')

COLWIDTH = [(0, 6), (7, 35), (36, 48), (53, 68), (69, 73), (74, 88), (89, 97), (98, 130)]

COLNAME = ["Number", "Name", "Prov.Desig", "Period(h)", "Quality", "Amp", "Var Max", "Ref"]

earn = pd.read_fwf(EARN_URL + '/rotation.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None, skiprows=1, nrows=1588,
                                  dtype='str', keep_default_na=False)

# Keep only the last reference that we can track

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

# Create a dataframe with our formatting

df_earn_old = pd.DataFrame(earn, columns=("Number", "Name", "Prov.Desig",
                                                  "Period(h)", "Lower P.", "Upper P.",
                                                  "Uncert. P.", "Approx P.",
                                                  "Quality", "Radar", "Multiple System",
                                                  "Amp", "Lower A.", "Upper A.",
                                                  "Uncert. A.", "Approx A.",
                                                  "Max Variation", "Ref"))
     
# Check for Radar measurements

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "R" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("R", "")
            df_earn_old["Radar"].iloc[i] = 'Y'
        else:
            df_earn_old["Radar"].iloc[i] = 'N'

# Take only the last value if available

i = 0 
while i < len(df_earn_old["Period(h)"]):
    if not isNaN(df_earn_old["Period(h)"].iloc[i]):
        if ";" in df_earn_old["Period(h)"].iloc[i]:
            string = df_earn_old["Period(h)"].iloc[i]
            result = re.split(";", string)
            df_earn_old["Period(h)"].iloc[i] = result[0]
        else:
            i += 1
            continue
    else:
        i += 1
        continue
    
# Check for B which means binary systems or multiple systems in general

i = 0
while i < len(df_earn_old["Period(h)"]):
    if not isNaN(df_earn_old["Period(h)"].iloc[i]):
        if "+" in df_earn_old["Period(h)"].iloc[i]:
            string = df_earn_old["Period(h)"].iloc[i]
            result = re.split("\+", string)    # it needs to include \ before +
            for j in range(len(result)):
                if j == 0:
                    df_earn_old["Period(h)"].iloc[i] = result[0]
                    df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("B", "")
                    df_earn_old["Multiple System"].iloc[i] = 'B0'
                else:
                    line = pd.DataFrame({"Number": df_earn_old["Number"].iloc[i],
                                         "Name": df_earn_old["Name"].iloc[i],
                                         "Prov.Desig": df_earn_old["Prov.Desig"].iloc[i],
                                         "Period(h)": result[j],
                                         "Lower P.": df_earn_old["Lower P."].iloc[i],
                                         "Upper P.": df_earn_old["Upper P."].iloc[i],
                                         "Uncert. P.": df_earn_old["Uncert. P."].iloc[i],
                                         "Approx P.": df_earn_old["Approx P."].iloc[i],
                                         "Quality": df_earn_old["Quality"].iloc[i].replace("B", ""),
                                         "Radar": df_earn_old["Radar"].iloc[i],
                                         "Multiple System": 'B{}'.format(j),
                                         "Amp": df_earn_old["Amp"].iloc[i],
                                         "Lower A.": df_earn_old["Lower A."].iloc[i],
                                         "Upper A.": df_earn_old["Upper A."].iloc[i],
                                         "Uncert. A.": df_earn_old["Uncert. A."].iloc[i],
                                         "Approx A.": df_earn_old["Approx A."].iloc[i],
                                         "Max Variation": df_earn_old["Max Variation"].iloc[i],
                                         "Ref": df_earn_old["Ref"].iloc[i]}, index=[i])
                    df_earn_old = pd.concat([df_earn_old.iloc[:i], line,
                                    df_earn_old.iloc[i:]]).reset_index(drop=True)
            i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue

     
# Check for global binary/multiple system measurements

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "B" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("B", "")
            df_earn_old["Multiple System"].iloc[i] = 'M' # indicates multiple systems in general
        else:
            continue
        
# Check for lower or upper limit on Period 

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Period(h)"].iloc[i]):
        if "<" in df_earn_old["Period(h)"].iloc[i]:
            start = df_earn_old["Period(h)"].iloc[i].find("<")
            df_earn_old["Upper P."].iloc[i] = df_earn_old["Period(h)"].iloc[i][start+1:]
            df_earn_old["Period(h)"].iloc[i] = np.nan
        elif ">" in df_earn_old["Period(h)"].iloc[i]:
            start = df_earn_old["Period(h)"].iloc[i].find(">")
            df_earn_old["Lower P."].iloc[i] = df_earn_old["Period(h)"].iloc[i][start+1:]
            df_earn_old["Period(h)"].iloc[i] = np.nan
        else:
            continue
    else:
        continue

# Check for lower or upper limit on Amp 

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Amp"].iloc[i]):
        if "<" in df_earn_old["Amp"].iloc[i]:
            start = df_earn_old["Amp"].iloc[i].find("<")
            df_earn_old["Upper A."].iloc[i] = df_earn_old["Amp"].iloc[i][start+1:]
            df_earn_old["Amp"].iloc[i] = np.nan
        elif ">" in df_earn_old["Amp"].iloc[i]:
            start = df_earn_old["Amp"].iloc[i].find(">")
            df_earn_old["Lower A."].iloc[i] = df_earn_old["Amp"].iloc[i][start+1:]
            df_earn_old["Amp"].iloc[i] = np.nan
        else:
            continue
    else:
        continue

# Check for in quality (a, T, L, ?, ~)
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "A" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("A", "")
            df_earn_old["Approx P."].iloc[i] = 'a'
        elif "D" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("D", "")
            df_earn_old["Approx P."].iloc[i] = 'a'
        else:
            continue
    else:
         continue
     
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "~" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("~", "")
            df_earn_old["Approx P."].iloc[i] = '~'
        else:
            continue

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Period(h)"].iloc[i]):
        if "~" in df_earn_old["Period(h)"].iloc[i]:
            df_earn_old["Period(h)"].iloc[i] = df_earn_old["Period(h)"].iloc[i].replace("~", "")
            df_earn_old["Approx P."].iloc[i] = '~'
        else:
            continue
        
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "?" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("?", "")
            df_earn_old["Approx P."].iloc[i] = '?'
        else:
            continue
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Period(h)"].iloc[i]):
        if "?" in df_earn_old["Period(h)"].iloc[i]:
            df_earn_old["Period(h)"].iloc[i] = df_earn_old["Period(h)"].iloc[i].replace("?", "")
            df_earn_old["Approx P."].iloc[i] = '?'
        else:
            continue


for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "L" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("L", "")
            df_earn_old["Approx P."].iloc[i] = 'L'
        else:
            continue

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Quality"].iloc[i]):
        if "T" in df_earn_old["Quality"].iloc[i]:
            df_earn_old["Quality"].iloc[i] = df_earn_old["Quality"].iloc[i].replace("T", "")
            df_earn_old["Approx P."].iloc[i] = 'T'
        else:
            continue
        
# Amp
# Take only the last value if available

i = 0 
while i < len(df_earn_old["Amp"]):
    if not isNaN(df_earn_old["Amp"].iloc[i]):
        if ";" in df_earn_old["Amp"].iloc[i]:
            string = df_earn_old["Amp"].iloc[i]
            result = re.split(";", string)
            df_earn_old["Amp"].iloc[i] = result[0]
            i += 1
        elif "," in df_earn_old["Amp"].iloc[i]:
            string = df_earn_old["Amp"].iloc[i]
            result = re.split(",", string)
            df_earn_old["Amp"].iloc[i] = result[0]
            i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue
    
for i in range(len(df_earn_old["Amp"])):
    if not isNaN(df_earn_old["Amp"].iloc[i]):
        if "-" in df_earn_old["Amp"].iloc[i]:
            string = df_earn_old["Amp"].iloc[i]
            result = re.split("-", string)
            df_earn_old["Lower A."].iloc[i] = result[0]
            df_earn_old["Upper A."].iloc[i] = result[1]
            df_earn_old["Amp"].iloc[i] = np.nan
        else:
            continue
    else:
        continue

for i in range(len(df_earn_old["Amp"])):
    if not isNaN(df_earn_old["Amp"].iloc[i]):
        if " " in df_earn_old["Amp"].iloc[i]:
            string = df_earn_old["Amp"].iloc[i]
            result = re.split(" ", string)
            df_earn_old["Lower A."].iloc[i] = result[0]
            df_earn_old["Upper A."].iloc[i] = result[1]
            df_earn_old["Amp"].iloc[i] = np.nan
        else:
            continue
    else:
        continue
    


for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Amp"].iloc[i]):
        if "~" in df_earn_old["Amp"].iloc[i]:
            df_earn_old["Amp"].iloc[i] = df_earn_old["Amp"].iloc[i].replace("~", "")
            df_earn_old["Approx A."].iloc[i] = '~'
        else:
            continue
        
# Uplaoding the new dataset

COLWIDTH = [(0, 7), (8, 36), (37, 49), (50, 60), (61, 71), (72, 82), (83, 93),
            (94, 99), (100, 102), (103, 108), (109, 112), (113, 118), (119, 124),
            (125, 130), (131, 138), (139, 144), (145, 153), (154, 170)]

COLNAME = ["Number", "Name", "Prov.Desig",
           "Period(h)", "Lower P.", "Upper P.",
           "Uncert. P.", "Approx P.",
           "Quality", "Radar", "Multiple System",
           "Amp", "Lower A.", "Upper A.",
           "Uncert. A.", "Approx A.",
           "Max Variation", "Ref"]

earn_new = pd.read_fwf(EARN_NEW_URL + '/rotation.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None,
                                  dtype='str', keep_default_na=False)


df_total = pd.concat([df_earn_old, earn_new]).reset_index(drop=True)
df_total.fillna('', inplace=True)

list_non_NEO, idx = are_there_NEO(df_total)

if len(list_non_NEO) != 0:
    df_total.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_total = df_total.sort_values("Prov.Desig").reset_index(drop=True)

for i in range(len(df_total)):
    if len(df_total.at[i, "Radar"]) == 0:
        df_total.at[i, "Radar"] = 'N'
    else:
        continue
    
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

write_fdf("./Output/rotation_ALL.txt", df_total, colspecs)