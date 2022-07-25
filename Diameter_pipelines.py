# -*- coding: utf-8 -*-
"""
Created on Tue May 17 10:16:05 2022

@author: pio-r
"""

import pandas as pd
import tabula
import os
os.chdir('./new-earn')
from function.is_nan import isNaN
from function.protolog import protolog
from function.are_there_NEO import are_there_NEO
from function.neowise_clean_dataset import neowise_clean_dataset
from function.neorocks_diam import neorocks_diam
from function.write_fdf import write_fdf


# LOADING URLS FOR DATASETS FOR DIAMETER and ALBEDO
NEOW45_URL = ['https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t1_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657268583&Signature=1LmUgV%2FVXhlqWzp7G3Cdz1ObaO8%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t2_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657268583&Signature=ZbcQgLCVC9XXlZPkabDvzciq2fk%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t3_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657268583&Signature=ljFV6m8BXbrvpmZBiHWR8oKsY%2F4%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/1/1/5/revision1/psjab7820t4_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657268583&Signature=gWkhD%2F6zamu5qklbbENYO5ECEFo%3D']

NEOW67_URL = ['https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt1_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657267447&Signature=AUWHumHgvq8xzCnT%2BS6bCZrZs%2BU%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt2_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657267447&Signature=SdTren%2B%2BS%2FprTHnSskSXiZ2BBcE%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt3_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657267447&Signature=ygeoS3ZTvvJ%2FIhkYV8qfyGHrHP8%3D',
            'https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/2632-3338/2/4/162/revision1/psjac15fbt4_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1657267447&Signature=o7vtFE8LTeO%2FGtBP91CxDnRlnCA%3D']

NEOR_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/NEOROCKS/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

REF_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/')

ref = pd.read_fwf(REF_URL + '/Reference.txt',
                  names=colname, colspecs=colwidth, header=None)

# NEOWISE 4-5 years

df_NEOW45 = neowise_clean_dataset(NEOW45_URL)
df_NEOW45["Ref."] = ref["ID"][10][2:]


# NEOWISE 6-7 years
df_NEOW67 = pd.DataFrame()
idx67 = []
neo67 = []

df_NEOW67 = neowise_clean_dataset(NEOW67_URL)
df_NEOW67["Ref."] = ref["ID"][11][2:]


df_NEOW = pd.concat([df_NEOW45, df_NEOW67]).reset_index(drop=True)

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


# for i in range(len(df_total)):
#     df_total["Ref."].iloc[i] = int(df_total["Ref."].iloc[i])
# WRITE THE FILE


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

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/Diameter_Albedo.txt", df_total, colspecs)

protolog("inf", "Diam database ready")
