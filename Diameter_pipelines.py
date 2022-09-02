# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:16:05 2022

@author: pio-r
"""

import pandas as pd
import tabula
import os

from function.is_nan import isNaN
from function.protolog import protolog
from function.are_there_NEO import are_there_NEO
from function.neowise_clean_dataset import neowise_clean_dataset
from function.neorocks_diam import neorocks_diam
from function.write_fdf import write_fdf


# LOADING URLS FOR DATASETS FOR DIAMETER and ALBEDO
NEOW45_URL = ['https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t1_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662712922&Signature=1RCWqh6oQLg6%2FIQ2bX2LML%2FmCI0%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t2_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662712922&Signature=i7Kryosfp8SblEWKWBXjBXWOW7k%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t3_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662712922&Signature=anYp1NPsfVvStMBsxF8M4Qxoo8Y%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t4_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662712922&Signature=SkkaNkF0cxnKAHhBYw8YBx3xseY%3D']

NEOW67_URL = ['https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt1_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662713670&Signature=6V7U9P5nrWVOEW5xj7Cb14dIFSc%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt2_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662713670&Signature=O0SwXkeiLt4VeM%2Bo%2BDee0cZ%2BzxQ%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt3_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662713670&Signature=LMHY%2F6sccl9DlkHneV5Kv7Y7uCw%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt4_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1662713670&Signature=3dzQ4WacW5vSDlU8uS37fcfKfA0%3D']

NEOR_URL = os.path.dirname('./Data/NEOROCKS/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

# REF_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/')

ref = pd.read_fwf('./Reference.txt',
                  names=colname, colspecs=colwidth, header=None)

# NEOWISE 4-5 years

df_NEOW45 = neowise_clean_dataset(NEOW45_URL)
df_NEOW45[0]["Ref."] = ref["ID"][10][2:]


# NEOWISE 6-7 years
df_NEOW67 = pd.DataFrame()
idx67 = []
neo67 = []

df_NEOW67 = neowise_clean_dataset(NEOW67_URL)
df_NEOW67[0]["Ref."] = ref["ID"][11][2:]


df_NEOW = pd.concat([df_NEOW45[0], df_NEOW67[0]]).reset_index(drop=True)

# NEOROCKS

dfs = tabula.read_pdf(NEOR_URL + '/Spectral properties of near-Earth objects'
                      ' with low-Jovian Tisserand invariant -'
                      ' Simon et al 2021 - 150 NEAs.pdf', pages='18-20')


df = dfs[0]
df.rename(columns={'Designation': 'Number', 'pv': 'Albedo', 'D eq': 'Diam.'}, inplace=True)
df_NEOR = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
                                                  "Albedo", "Lower A.", "Upper A.",
                                                  "Uncert.A.", "Approx A.",
                                                  "Diam.", "Lower D.", "Upper D.",
                                                  "Uncert.D.", "Approx D.",
                                                  "X", "Y", "Z", "Radar",
                                                  "Multiple System", "Ref."))

df_1 = dfs[1]
df_1.columns = df_1.iloc[0]
df_1 = df_1[1:]
df_1.rename(columns={'Designation': 'Number', 'pv': 'Albedo', 'D(km)eq': 'Diam.'}, inplace=True)
df_NEOR_1 = pd.DataFrame(df_1, columns=("Number", "Name", "Prov.Desig",
                                                  "Albedo", "Lower A.", "Upper A.",
                                                  "Uncert.A.", "Approx A.",
                                                  "Diam.", "Lower D.", "Upper D.",
                                                  "Uncert.D.", "Approx D.",
                                                  "X", "Y", "Z", "Radar",
                                                  "Multiple System", "Ref."))

df_2 = dfs[2]
df_2.columns = df_2.iloc[0]
df_2 = df_2[1:]
df_2.rename(columns={'Designation': 'Number', 'pv': 'Albedo', 'D(km)eq': 'Diam.'}, inplace=True)
df_NEOR_2 = pd.DataFrame(df_2, columns=("Number", "Name", "Prov.Desig",
                                                  "Albedo", "Lower A.", "Upper A.",
                                                  "Uncert.A.", "Approx A.",
                                                  "Diam.", "Lower D.", "Upper D.",
                                                  "Uncert.D.", "Approx D.",
                                                  "X", "Y", "Z", "Radar",
                                                  "Multiple System", "Ref."))

df_NEOR = pd.concat([df_NEOR, df_NEOR_1, df_NEOR_2]).reset_index(drop=True)

df_NEOR = neorocks_diam(df_NEOR)

list_non_NEO, idx = are_there_NEO(df_NEOR)

df_NEOR["Ref."] = ref["ID"][12][2:]

idx = []

for i in range(len(df_NEOR)):
    if not isNaN(df_NEOR["Approx A."].iloc[i]):
        if "*" in df_NEOR["Approx A."].iloc[i]:
            idx.append(i)
        else:
            continue
    else:
        continue

df_NEOR.drop(idx, axis=0, inplace=True)

df_NEOR.reset_index(drop=True, inplace=True)

# MERGE DATASET

df_total = pd.concat([df_NEOW, df_NEOR]).reset_index(drop=True)
df_total = df_total.drop_duplicates().reset_index(drop=True)
df_total.fillna('', inplace=True)
df_total = df_total.sort_values("Prov.Desig").reset_index(drop=True)

for i in range(len(df_total)):
    if type(df_total["Upper A."].iloc[i]) == float:
        df_total["Upper A."].iloc[i] = round(df_total["Upper A."].iloc[i], 3)
    else:
        continue
for i in range(len(df_total)):
    if type(df_total["Lower A."].iloc[i]) == float:
       df_total["Lower A."].iloc[i] = round(df_total["Lower A."].iloc[i], 3)
    else:
        continue
for i in range(len(df_total)):
    if type(df_total["Albedo"].iloc[i]) == float:
        df_total["Albedo"].iloc[i] = round(df_total["Albedo"].iloc[i], 3)
    else:
        continue

idx = []

for i in range(len(df_total)):
    if all(char.isdigit() for char in df_total["Name"].iloc[i][1:]) and df_total["Name"].iloc[i].startswith("a"):
       idx.append(i)
    else:
        continue

for value in idx:
     df_total.drop(value, inplace=True)

df_total = df_total.sort_values("Prov.Desig").reset_index(drop=True)

df_total["Lower A."] = df_total["Lower A."].astype(str)
df_total["Upper A."] = df_total["Upper A."].astype(str)

for i in range(len(df_total)):
    if len(df_total["Lower A."].iloc[i]) != 0:
        df_total["Lower A."].iloc[i] = df_total["Lower A."].iloc[i] + '*'
    else:
        continue
    
for i in range(len(df_total)):
    if len(df_total["Upper A."].iloc[i]) != 0:
        df_total["Upper A."].iloc[i] = df_total["Upper A."].iloc[i] + '*'
    else:
        continue

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

write_fdf("./Output/Diameter_Albedo.txt", df_total, colspecs)

protolog("inf", "Diam database ready")
