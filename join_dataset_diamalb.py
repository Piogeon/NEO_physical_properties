# -*- coding: utf-8 -*-
"""
Created on Wed May 25 10:06:51 2022

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

COLWIDTH = [(0, 6), (7, 35), (36, 48), (49, 58), (59, 88), (89, 103), (104, 140)]

COLNAME = ["Number", "Name", "Prov.Desig", "Albedo", "Ref 1", "Diameter", "Ref 2"]

earn = pd.read_fwf(EARN_URL + 'diameter.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None, skiprows=1, nrows=1745,
                                  dtype='str', keep_default_na=False)

i = 0
while i < len(earn["Ref 1"]):
    if not isNaN(earn["Ref 1"].iloc[i]):
        if "," in earn["Ref 1"].iloc[i]:
            string = earn["Ref 1"].iloc[i]
            result = re.split(",", string)
            earn["Ref 1"].iloc[i] = result[0]
            if ";" in earn["Ref 1"].iloc[i]:
                string = earn["Ref 1"].iloc[i]
                result = re.split(";", string)
                earn["Ref 1"].iloc[i] = result[0]
            else:
                i += 1
        elif ";" in earn["Ref 1"].iloc[i]:
            string = earn["Ref 1"].iloc[i]
            result = re.split(";", string)
            earn["Ref 1"].iloc[i] = result[0]
            if "," in earn["Ref 1"].iloc[i]:
                string = earn["Ref 1"].iloc[i]
                result = re.split(",", string)
                earn["Ref 1"].iloc[i] = result[0]
            else:
                i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue
    
i = 0
while i < len(earn["Ref 2"]):
    if not isNaN(earn["Ref 2"].iloc[i]):
        if "," in earn["Ref 2"].iloc[i]:
            string = earn["Ref 2"].iloc[i]
            result = re.split(",", string)
            earn["Ref 2"].iloc[i] = result[0]
            if ";" in earn["Ref 2"].iloc[i]:
                string = earn["Ref 2"].iloc[i]
                result = re.split(";", string)
                earn["Ref 2"].iloc[i] = result[0]
            else:
                i += 1
        elif ";" in earn["Ref 2"].iloc[i]:
            string = earn["Ref 2"].iloc[i]
            result = re.split(";", string)
            earn["Ref 2"].iloc[i] = result[0]
            if "," in earn["Ref 2"].iloc[i]:
                string = earn["Ref 2"].iloc[i]
                result = re.split(",", string)
                earn["Ref 2"].iloc[i] = result[0]
            else:
                i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue
    
    
for i in range(len(earn)):
    if not earn["Ref 1"].iloc[i] in earn["Ref 2"].iloc[i]:
        row = pd.DataFrame({"Number": earn["Number"].iloc[i],
                                         "Name": earn["Name"].iloc[i],
                                         "Prov.Desig": earn["Prov.Desig"].iloc[i],
                                         "Albedo": earn["Albedo"].iloc[i],
                                         "Ref 1": np.nan,
                                         "Diameter": np.nan,
                                         "Ref 2": earn["Ref 1"].iloc[i]}, index=[i])
        earn["Albedo"].iloc[i] = np.nan
        earn = pd.concat([earn, row]).reset_index(drop=True)
        
    

earn.drop("Ref 1", axis=1, inplace=True)

df_earn_old = pd.DataFrame(earn,columns=("Number", "Name", "Prov.Desig",
                                                  "Albedo", "Lower A.", "Upper A.",
                                                  "Uncert.A.", "Approx A.",
                                                  "Diameter", "Lower D.", "Upper D.",
                                                  "Uncert.D.", "Approx D.",
                                                  "X", "Y", "Z", "Radar",
                                                  "Multiple System", "Ref 2"))
df_earn_old.rename(columns={'Ref 2': 'Ref.'}, inplace=True)

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Albedo"].iloc[i]):
        if "R" in df_earn_old["Albedo"].iloc[i]:
            start = df_earn_old["Albedo"].iloc[i].find("R")
            df_earn_old["Albedo"].iloc[i] = df_earn_old["Albedo"].iloc[i][:start]
            df_earn_old["Radar"].iloc[i] = 'Y'
        else:
            print('No Radar measurements for {}'.format(df_earn_old["Prov.Desig"].iloc[i]))
        if any(k in df_earn_old["Albedo"].iloc[i] for k in ('d', 'm', 'mh', 'h', 'a', '~')):
            df_earn_old["Approx A."].iloc[i] = df_earn_old["Albedo"].iloc[i]
            df_earn_old["Albedo"].iloc[i] = np.nan
        else:
            print('No approx value for {}'.format(df_earn_old["Prov.Desig"].iloc[i]))
    else:
         continue   

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Approx A."].iloc[i]):
        if ";" in df_earn_old["Approx A."].iloc[i]:
            start = df_earn_old["Approx A."].iloc[i].find(";")
            if all(char.isdigit() for char in df_earn_old["Approx A."].iloc[i][start+1:]):
                df_earn_old["Albedo"].iloc[i] = df_earn_old["Approx A."].iloc[i][:start]
                df_earn_old["Approx A."].iloc[i] = df_earn_old["Approx A."].iloc[i][start+1:]
            else:
                df_earn_old["Albedo"].iloc[i] = df_earn_old["Approx A."].iloc[i][start+1:]
                df_earn_old["Approx A."].iloc[i] = df_earn_old["Approx A."].iloc[i][:start]
        if "~" in df_earn_old["Approx A."].iloc[i]:
            start = df_earn_old["Approx A."].iloc[i].find("~")
            df_earn_old["Albedo"].iloc[i] = df_earn_old["Approx A."].iloc[i][start+1:]
            df_earn_old["Approx A."].iloc[i] = "~"
        else:
            continue
    else:
        continue
    
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Diameter"].iloc[i]):
        if "R" in df_earn_old["Diameter"].iloc[i]:
            start = df_earn_old["Diameter"].iloc[i].find("R")
            df_earn_old["Diameter"].iloc[i] = df_earn_old["Diameter"].iloc[i][:start]
            df_earn_old["Radar"].iloc[i] = 'Y'
        else:
            print('No Radar measurements for {}'.format(df_earn_old["Prov.Desig"].iloc[i]))        
        
i = 0
while i < len(df_earn_old["Diameter"]):
    if not isNaN(df_earn_old["Diameter"].iloc[i]):
        if ";" in df_earn_old["Diameter"].iloc[i]:
            string = df_earn_old["Diameter"].iloc[i]
            result = re.split(";", string)
            for j in range(len(result)):
                if j == 0:
                    df_earn_old["Diameter"].iloc[i] = result[0]
                else:
                    line = pd.DataFrame({"Number": df_earn_old["Number"].iloc[i],
                                         "Name": df_earn_old["Name"].iloc[i],
                                         "Prov.Desig": df_earn_old["Prov.Desig"].iloc[i],
                                         "Albedo": df_earn_old["Albedo"].iloc[i],
                                         "Lower A.": df_earn_old["Lower A."].iloc[i],
                                         "Upper A.": df_earn_old["Upper A."].iloc[i],
                                         "Uncert.A.": df_earn_old["Uncert.A."].iloc[i],
                                         "Approx A.": df_earn_old["Approx A."].iloc[i],
                                         "Diameter": result[j],
                                         "Lower D.": df_earn_old["Lower D."].iloc[i],
                                         "Upper D.": df_earn_old["Upper D."].iloc[i],
                                         "Uncert.D.": df_earn_old["Uncert.D."].iloc[i],
                                         "Approx D.": df_earn_old["Approx D."].iloc[i],
                                         "X": df_earn_old["X"].iloc[i],
                                         "Y": df_earn_old["Y"].iloc[i],
                                         "Z": df_earn_old["Z"].iloc[i],
                                         "Radar": df_earn_old["Radar"].iloc[i],
                                         "Multiple System": df_earn_old["Multiple System"].iloc[i],
                                         "Ref.": df_earn_old["Ref."].iloc[i]}, index=[i])
                    df_earn_old = pd.concat([df_earn_old.iloc[:i], line,
                                    df_earn_old.iloc[i:]]).reset_index(drop=True)
            i += 1
        elif "+" in df_earn_old["Diameter"].iloc[i]:
            string = df_earn_old["Diameter"].iloc[i]
            result = re.split("\+", string)
            for j in range(len(result)):
                if j == 0:
                    df_earn_old["Diameter"].iloc[i] = result[0]
                    df_earn_old["Multiple System"].iloc[i] = 'B0'
                else:
                    line = pd.DataFrame({"Number": df_earn_old["Number"].iloc[i],
                                         "Name": df_earn_old["Name"].iloc[i],
                                         "Prov.Desig": df_earn_old["Prov.Desig"].iloc[i],
                                         "Albedo": df_earn_old["Albedo"].iloc[i],
                                         "Lower A.": df_earn_old["Lower A."].iloc[i],
                                         "Upper A.": df_earn_old["Upper A."].iloc[i],
                                         "Uncert.A.": df_earn_old["Uncert.A."].iloc[i],
                                         "Approx A.": df_earn_old["Approx A."].iloc[i],
                                         "Diameter": result[j],
                                         "Lower D.": df_earn_old["Lower D."].iloc[i],
                                         "Upper D.": df_earn_old["Upper D."].iloc[i],
                                         "Uncert.D.": df_earn_old["Uncert.D."].iloc[i],
                                         "Approx D.": df_earn_old["Approx D."].iloc[i],
                                         "X": df_earn_old["X"].iloc[i],
                                         "Y": df_earn_old["Y"].iloc[i],
                                         "Z": df_earn_old["Z"].iloc[i],
                                         "Radar": df_earn_old["Radar"].iloc[i],
                                         "Multiple System": 'B{}'.format(j),
                                         "Ref.": df_earn_old["Ref."].iloc[i]}, index=[i])
                    df_earn_old = pd.concat([df_earn_old.iloc[:i], line,
                                    df_earn_old.iloc[i:]]).reset_index(drop=True)
            i += 1
        else:
            i += 1
            continue
    else:
        i += 1
        continue

for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Diameter"].iloc[i]):
        if "<" in df_earn_old["Diameter"].iloc[i]:
            start = df_earn_old["Diameter"].iloc[i].find("<")
            df_earn_old["Upper D."].iloc[i] = df_earn_old["Diameter"].iloc[i][start+1:]
            df_earn_old["Diameter"].iloc[i] = np.nan
        elif ">" in df_earn_old["Diameter"].iloc[i]:
            start = df_earn_old["Diameter"].iloc[i].find(">")
            df_earn_old["Lower D."].iloc[i] = df_earn_old["Diameter"].iloc[i][start+1:]
            df_earn_old["Diameter"].iloc[i] = np.nan
        else:
            continue
    else:
        continue
    
for i in range(len(df_earn_old)):
    if not isNaN(df_earn_old["Diameter"].iloc[i]):
        if "x" in df_earn_old["Diameter"].iloc[i]:
            string = df_earn_old["Diameter"].iloc[i]
            result = re.split("x", string)
            if len(result)<3:
                df_earn_old["X"].iloc[i] = result[0]
                df_earn_old["Y"].iloc[i] = result[1]
                df_earn_old["Diameter"].iloc[i] = np.nan
            else:
                df_earn_old["X"].iloc[i] = result[0]
                df_earn_old["Y"].iloc[i] = result[1]
                df_earn_old["Z"].iloc[i] = result[2]
                df_earn_old["Diameter"].iloc[i] = np.nan
    else:
        continue
    
for i in range(len(df_earn_old)):
    if any(char.isdigit() for char in df_earn_old["Name"].iloc[i]):
        df_earn_old["Name"].iloc[i] = np.nan
    else:
        continue
    
COLWIDTH = [(0, 7), (8, 36), (37, 49), (50, 56), (57, 63), (64, 70), (71, 77),
            (78, 84), (85, 93), (94, 102), (103, 111), (112, 120), (121, 124),
            (125, 133), (134, 142), (143, 151), (152, 157), (158, 161), (162, 165)]

COLNAME = ["Number", "Name", "Prov.Desig", "Albedo", "Lower A.", "Upper A.",
           "Uncert.A.", "Approx A.", "Diameter", "Lower D.", "Upper D.",
           "Uncert.D.", "Approx D.", "X", "Y", "Z", "Radar", "Multiple System", "Ref."]

earn_new = pd.read_fwf(EARN_NEW_URL + 'Diameter_Albedo.txt',
                  names=COLNAME, colspecs=COLWIDTH, header=None,
                                  dtype='str', keep_default_na=False)


df_total = pd.concat([df_earn_old, earn_new]).reset_index(drop=True)
df_total.fillna('', inplace=True)

list_non_NEO, idx = are_there_NEO(df_total)

if len(list_non_NEO) != 0:
    df_total.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_total.reset_index(drop=True, inplace=True)
df_total = df_total.sort_values("Name").reset_index(drop=True)
df_total['Ref.']= df_total['Ref.'].astype(str)

for i in range(len(df_total)):
    if ";" in df_total["Ref."].iloc[i]:
        string = df_total["Ref."].iloc[i]
        result = re.split(";", string)
        df_total["Ref."].iloc[i] = result[0]
    elif "," in df_total["Ref."].iloc[i]:
        string = df_total["Ref."].iloc[i]
        result = re.split(",", string)
        df_total["Ref."].iloc[i] = result[0]
    else:
        continue
    
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

# for i in range(len(df_total)):
#     row = df_total.loc[df_total["Prov.Desig"] == df_total["Prov.Desig"].iloc[i]]
#     idx = row.index
#     row = row.sort_values("Ref.").reset_index(drop=True)
    
i = 0

while i < len(df_total):
    idx = df_total.loc[df_total["Prov.Desig"] == df_total["Prov.Desig"].iloc[i]].index
    df_test = df_total.loc[df_total["Prov.Desig"] == df_total["Prov.Desig"].iloc[i]]
    df_test = df_test.sort_values("Ref.")
    df_test.set_index(idx, drop=True, append=False, inplace=True, verify_integrity=False)
    df_total.iloc[idx[0]:idx[-1]+1] = df_test
    i = idx[-1] + 1


colspecs = [
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <6} ",
    "{: <6} ",
    "{: <6} ",
    "{: <6} ",
    "{: <6} ",
    "{: <8} ",
    "{: <8} ",
    "{: <8} ",
    "{: <8} ",
    "{: <3} ",
    "{: <8} ",
    "{: <8} ",
    "{: <8} ",
    "{: <5} ",
    "{: <3} ",
    "{: <2} ",
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/Diameter_Albedo_ALL.txt", df_total, colspecs)

protolog("inf", "Diam database ready")

        