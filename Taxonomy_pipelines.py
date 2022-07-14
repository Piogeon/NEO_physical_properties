# -*- coding: utf-8 -*-
"""
Created on Wed May  4 11:22:30 2022

@author: pio-r
"""

import pandas as pd
import numpy as np
import tabula
from function.format_clean_dataset import format_clean_dataset
from function.is_nan import isNaN
from function.protolog import protolog
from function.write_fdf import write_fdf
from function.are_there_NEO import are_there_NEO


# Change the current working directory
# os.chdir('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/
# Primary_Pipelines')


# LOADING URLS FOR DATASETS FOR TAXONOMY

MITH_URL = ('https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/1538-3881/163/4/165/revision1/ajac532ft7_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1656581807&Signature=jmNgrkXqaEwCqjomGDT7yIsf7l4%3D')

MANO_URL = ('https://cfn-live-content-bucket-iop-org.s3.amazonaws.com/journals/1538-3881/158/5/196/revision1/ajab43ddt5_mrt.txt?AWSAccessKeyId=AKIAYDKQL6LTV7YY2HIK&Expires=1656581845&Signature=m%2BHSDLz5ofURu7%2BS3%2B%2FP6oMKI54%3D')

SDSS_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/SDSS/'

SKYM_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/SkyMapper/'

SIMD_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/SiMDA/'

NEOR_URL = ('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/'
            'NEOROCKS/')

PRAV_URL = ('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/'
            'Binary_asteroid_parameters/')


# REFERENCE


colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

ref = pd.read_fwf('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/'
                  'Programs/Primary_Pipelines/Reference.txt', names=colname,
                  colspecs=colwidth, header=None)

# MITHNEOS

NAME = ["Number", "Name", "Prov.Desig", "Taxon"]
COLWIDTH = [(33, 39), (51, 64), (40, 50), (123, 129)]
# inserire controllo in caso queste colonne possono cambiare anche in futuro

df = pd.read_fwf(MITH_URL, skiprows=61, names=NAME, colspecs=COLWIDTH,
                 header=None)

protolog("inf", "MITH_URL read correctly")

df_MITH = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig", "Taxon",
                                    "Approx.Value", "Ref"))

protolog("inf", "MITH_URL added Approx.Value and Ref columns")

df_MITH = format_clean_dataset(df_MITH)

df_MITH["Ref"] = df_MITH["Ref"].replace(np.nan, ref["ID"][15][2:])

list_non_NEO, idx = are_there_NEO(df_MITH)

if len(list_non_NEO) != 0:
    df_MITH.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_MITH.reset_index(drop=True, inplace=True)

#  MANOS

NAME = ['Prov.Desig', 'Taxon']
COLWIDTH = [(0, 10), (81, 83)]

df = pd.read_fwf(MANO_URL, skiprows=37, names=NAME, colspecs=COLWIDTH,
                 header=None)

protolog("inf", "MANO_URL read correctly")

df_MANO = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
                                    "Taxon", "Approx.Value", "Ref"))

df_MANO = format_clean_dataset(df_MANO)

df_MANO["Ref"] = df_MANO["Ref"].replace(np.nan, ref["ID"][8][2:])

list_non_NEO, idx = are_there_NEO(df_MANO)

if len(list_non_NEO) != 0:
    df_MANO.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_MANO.reset_index(drop=True, inplace=True)

# SDSS

df = pd.read_csv(SDSS_URL + 'SDSS_data.csv')
df.rename(columns={'Name': 'Prov.Desig', 'grcomplex': 'Taxon'}, inplace=True)

df_SDSS = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
                                    "Taxon", "Approx.Value", "Ref"))

df_SDSS = format_clean_dataset(df_SDSS)

df_SDSS["Ref"] = df_SDSS["Ref"].replace(np.nan, ref["ID"][13][2:])

list_non_NEO, idx = are_there_NEO(df_SDSS)

if len(list_non_NEO) != 0:
    df_SDSS.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_SDSS.reset_index(drop=True, inplace=True)

# SKYMAPPER Dataset

df = pd.read_csv(SKYM_URL + 'SkyMapper_data.csv')
df.rename(columns={'Name': 'Prov.Desig', 'complex': 'Taxon'}, inplace=True)

df_SKYM = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
                                    "Taxon", "Approx.Value", "Ref"))

df_SKYM = format_clean_dataset(df_SKYM)

df_SKYM["Ref"] = df_SKYM["Ref"].replace(np.nan, ref["ID"][16][2:])

list_non_NEO, idx = are_there_NEO(df_SKYM)

if len(list_non_NEO) != 0:
    df_SKYM.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_SKYM.reset_index(drop=True, inplace=True)


# SIMDA

# df = pd.read_csv(SIMD_URL + 'SiMDA_220510.csv')
# df.rename(columns={'NUM': 'Number', 'DESIGNATION': 'Prov.Desig',
#                    'T.D': 'Taxon'}, inplace=True)

# df.drop(df[(df['DYN'] != 'NEA') & (df['DYN'] != 'AMO') &
#            (df['DYN'] != 'APO')].index, inplace=True)

# df = df.reset_index(drop=True)

# df_SIMD = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
#                                     "Taxon", "Approx.Value", "Ref"))

# df_SIMD = format_clean_dataset(df_SIMD)

# df_SIMD["Ref"] = df_SIMD["Ref"].replace(np.nan, ref["ID"][4])
# df_SIMD["Taxon"] = df_SIMD["Taxon"].replace('-', '')

# list_non_NEO, idx = are_there_NEO(df_SIMD)


# if len(list_non_NEO) != 0:
#     df_SIMD.drop(idx, axis=0, inplace=True)
# else:
#     print('All the objects are NEOs')

# df_SIMD.reset_index(drop=True, inplace=True)

# NEOROCKS

dfs = tabula.read_pdf(NEOR_URL + 'Spectral properties of near-Earth objects'
                      ' with low-Jovian Tisserand invariant -'
                      ' Simon et al 2021 - 150 NEAs.pdf', pages='18-20')

df = dfs[0]
df.rename(columns={'Designation': 'Number', 'Tax.': 'Taxon'}, inplace=True)
df_NEOR = pd.DataFrame(df, columns=("Number", "Name", "Prov.Desig",
                                    "Taxon", "Approx.Value", "Ref"))

df_1 = dfs[1]
df_1.columns = df_1.iloc[0]
df_1 = df_1[1:]
df_1.rename(columns={'Designation': 'Number', 'Tax.': 'Taxon'}, inplace=True)
df_NEOR_1 = pd.DataFrame(df_1, columns=("Number", "Name", "Prov.Desig",
                                        "Taxon", "Approx.Value", "Ref"))

df_2 = dfs[2]
df_2.columns = df_2.iloc[0]
df_2 = df_2[1:]
df_2.rename(columns={'Designation': 'Number', 'Tax.': 'Taxon'}, inplace=True)
df_NEOR_2 = pd.DataFrame(df_2, columns=("Number", "Name", "Prov.Desig",
                                        "Taxon", "Approx.Value", "Ref"))

df_NEOR = pd.concat([df_NEOR, df_NEOR_1, df_NEOR_2]).reset_index(drop=True)

df_NEOR = format_clean_dataset(df_NEOR)

df_NEOR["Ref"] = df_NEOR["Ref"].replace(np.nan, ref["ID"][12][2:])

list_non_NEO, idx = are_there_NEO(df_NEOR)

if len(list_non_NEO) != 0:
    df_NEOR.drop(idx, axis=0, inplace=True)
else:
    print('All the objects are NEOs')

df_NEOR.reset_index(drop=True, inplace=True)

# MERGE DATASET

df_total = pd.concat([df_MITH, df_MANO, df_SDSS, df_SKYM,
                      df_NEOR]).reset_index(drop=True)
df_total = df_total.drop_duplicates().reset_index(drop=True)
for i in range(len(df_total["Number"])):
    if not isNaN(df_total["Number"].iloc[i]):
        df_total["Number"].iloc[i] = np.int(df_total["Number"].iloc[i])
    else:
        continue
df_total = df_total.sort_values("Number").reset_index(drop=True)
df_total.fillna('', inplace=True)
#df_total["Ref"] = df_total["Ref"].astype(int)


# WRITE THE FILE


colspecs = [
    "{: <7} ",                                                  # left, width=6
    "{: <28} ",
    "{: <12} ",
    "{: <4} ",
    "{: <4} ",
    "{: <2} ",
    ]

write_fdf("C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/Programs/Primary_Pipelines/Dataset/taxonomy.txt", df_total, colspecs)

protolog("inf", "Taxonomy database ready")