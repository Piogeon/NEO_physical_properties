# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:02:11 2022

@author: pio-r
"""


import pandas as pd
import numpy as np
import os

from function.is_nan import isNaN
from function.protolog import protolog
import tabula
from function.format_dataset_color import format_dataset_color
from function.write_fdf import write_fdf
from function.are_there_NEO import are_there_NEO


# LOADING URLS FOR DATASETS FOR TAXONOMY

SKYM_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/SkyMapper/')

PRAV_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/'
            'Article/Binary_asteroid_parameters/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

# REF_URL = os.path.dirname('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/')

ref = pd.read_fwf('./Reference.txt',
                  names=colname, colspecs=colwidth, header=None)

# SKYMAPPER

df = pd.read_csv(SKYM_URL + '/SkyMapper_data.csv')
df_SKYM = pd.DataFrame(columns=["Number", "Name", "Prov.Desig", "Type",
                                "Value", "Lower", "Upper", "Uncert.", "Ref"])
df_SKYM["Number"] = df['Number']
df_SKYM["Prov.Desig"] = df['Name']
df_SKYM = format_dataset_color(df_SKYM, df)
df_SKYM["Ref"] = df_SKYM["Ref"].replace(np.nan, ref["ID"][16][2:])

list_non_NEO, idx = are_there_NEO(df_SKYM)

if len(list_non_NEO) != 0:
    df_SKYM.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_SKYM.reset_index(drop=True, inplace=True)


# PRAVEC

dfs = tabula.read_pdf(PRAV_URL + '/Pravec_93_ast.pdf', pages='8-9',
                      pandas_options={'header': None})
df = dfs[0]
df.rename(columns={0: 'Name 1', 1: 'Name 2', 5: 'Value 1', 6: 'Value 2'},
          inplace=True)
df_1 = pd.DataFrame(df, columns=["Name 1", "Value 1"])
df_1 = df_1.rename(columns={'Name 1': 'Prov.Desig', 'Value 1': 'Value'})
df_2 = pd.DataFrame(df, columns=["Name 2", "Value 2"])
df_2 = df_2.rename(columns={'Name 2': 'Prov.Desig', 'Value 2': 'Value'})
df = pd.concat([df_1, df_2]).reset_index(drop=True)

df_PRAV = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig", "Type",
                                    "Value", "Lower", "Upper", "Uncert.", "Ref"))
df_PRAV["Value"] = df_PRAV["Value"].replace(np.nan, " ")
df_PRAV["Type"] = df_PRAV["Type"].replace(np.nan, "v-r")

df_PRAV = format_dataset_color(df_PRAV, df)
df_PRAV["Ref"] = df_PRAV["Ref"].replace(np.nan, ref["ID"][5][2:])

list_non_NEO, idx = are_there_NEO(df_PRAV)

if len(list_non_NEO) != 0:
    df_PRAV.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_PRAV.reset_index(drop=True, inplace=True)


# MERGE DATASET


df_total = pd.concat([df_SKYM, df_PRAV]).reset_index(drop=True)
df_total = df_total.drop_duplicates().reset_index(drop=True)
for i in range(len(df_total["Number"])):
    if not isNaN(df_total["Number"].iloc[i]):
        df_total["Number"].iloc[i] = np.int(df_total["Number"].iloc[i])
    else:
        continue
df_total = df_total.sort_values("Number").reset_index(drop=True)
df_total.fillna('', inplace=True)

for i in range(len(df_total["Value"])):
    df_total["Value"].iloc[i] = np.str(df_total["Value"].iloc[i])[:6]
# df_total["Ref"] = df_total["Ref"].astype(int)

# WRITE THE FILE

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

write_fdf("./Output/Color.txt", df_total, colspecs)

protolog("inf", "Color database ready")
