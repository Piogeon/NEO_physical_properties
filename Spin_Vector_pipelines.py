# -*- coding: utf-8 -*-
"""
Created on Thu May 12 12:08:52 2022

@author: pio-r
"""

import pandas as pd
import sys
import numpy as np
import os
from bs4 import BeautifulSoup as bs
from lxml import etree
import xml.etree.ElementTree as ET
from function.is_nan import isNaN
from function.protolog import protolog
import tabula
from function.format_dataset_color import format_dataset_color
import re
from ESANEOCC import neocc
from tqdm import tqdm


# LOADING URLS FOR DATASETS FOR TAXONOMY
CSS3_URL = 'C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article/CS3/'

NEAPS_URL = ('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Books/Article'
             '/Lowell Observatory NEAPS/')

# REFERENCE

colwidth = [(0, 5), (6, 105)]

colname = ["ID", "Reference"]

ref = pd.read_fwf('C:/Users/pio-r/OneDrive/Desktop/ESA/Internship/Data/'
                  'Programs/Primary_Pipelines/Reference.txt',
                  names=colname, colspecs=colwidth, header=None)
# ESA

neo_num = neocc.query_list(list_name='nea_list')

#
with open(CSS3_URL + "NEA Lightcurve Analysis at the Center for Solar System Studies_5.html",
          'r', encoding='utf-8') as f:

    contents = f.read()

    root = ET.fromstring(contents)
    for child in root:
        print(child.tag, child.attrib)
    
    table = root.findall("./body/table[2]//td/p")

    value_tab = []
    for value in table:
        if not isinstance(value.text, type(None)):
            value_tab.append(value.text)
        else:
            value_tab.append("")
        

            
        
    for i in range(len(value_tab)):
        value_tab[i] = value_tab[i].replace("\t", "")
        value_tab[i] = value_tab[i].replace("\n", "")
    
    # For some pdf the columns Name and the Date are together so in the following part I'm splitting them 

    for i in range(len(value_tab)):
        if not isNaN(value_tab[i]):
            if " " in value_tab[i] and "/" in value_tab[i]:
                start = value_tab[i].find(" ")
                if all(char.isalpha() for char in value_tab[i][start:][1:3]):
                    start = start + value_tab[i][start+1:].find(" ") + 1
                else:
                    start = start
                if "/" in value_tab[i][start:].lstrip() and (all(char.isalpha() for char in value_tab[i][:4].lstrip()) or all(char.isdigit() for char in value_tab[i][:4])):
                    value_tab.insert(i+1, value_tab[i][start:].lstrip())
                    value_tab[i] = value_tab[i][:start]
                else:
                    continue
            else:
                continue
        else:
            continue
        
        
    c = input("What is the number of columns of the pdf file? ")
    col = value_tab[0:int(c)]
    value_tab = value_tab[int(c):]
    
    
    # Split the Name column in necessary
    
    for i in range(len(value_tab)):
        if not all(char.isalpha() for char in value_tab[i].replace(" ","")):
            if " " in value_tab[i]:
                ws = value_tab[i].find(" ")
                temp_char = value_tab[i][ws+1:]
                if any(char.isalpha() for char in temp_char):
                    if " " in temp_char:
                        ws_new = temp_char.find(" ")
                        new_value = temp_char[ws_new:]
                        new_value = new_value.lstrip()
                        value_tab.insert(i+1, new_value)
                        value_tab[i] = value_tab[i][:ws+1+ws_new]
                        print("Entered in if cond at i = {}".format(i))
                    else:
                        if not ("/" in temp_char or "?" in temp_char):
                            value_tab.insert(i+1, temp_char)
                            value_tab[i] = value_tab[i][:ws]
                            print("Entered in else cond at i = {}".format(i))
                        else:
                            continue
                else:
                    continue
            else:
                continue
        else:
            continue
    
    table = table[int(c):]
        
    def count_number(string):
        s = []
        for i in range(len(string)):
            if string[i].isalpha():
                s.append(string[i])
            else:
                continue
        return s
    
    # In the following code I am unifying the provisional designation, because in some parts it is splitted 
    
    for i in range(len(value_tab)):
        if i < len(value_tab)-4:
            if (all(char.isdigit() for char in value_tab[i]) and len(value_tab[i]) == 4) and ((len(value_tab[i+1]) == 2 and (all(char.isalpha() for char in value_tab[i+1])) or (len(count_number(value_tab[i+1])) == 2 and any(char.isdigit() for char in value_tab[i+1])))):
                print('Entered at {}'.format(i))
                new_value = value_tab[i] + " " + value_tab[i+1]
                value_tab.insert(i+2, new_value)
                value_tab = value_tab[:i] + value_tab[i+2:]
            else:
                continue
        else:
            break
    
    test_list = [value_tab[n:n+int(c)] for n in range(0, len(value_tab), int(c))]
    
    for i in range(len(value_tab)):
        if not isNaN(value_tab[i]):
            if value_tab[i][:4].isdigit() and len(count_number(value_tab[i][5:])) == 2:
                if not "/" in value_tab[i+1]:
                    try:
                        for j in range(len(table)):
                            if value_tab[i][5:] in table[j].text:
                                idx = j + 1
                                break
                            else:
                                continue
                        value_tab[i+1] = table[idx]._children[0].text
                        print('Entered try at {}'.format(i))
                    except:
                        print('Entered except at {}'.format(i))
                        value_tab.insert(i+1, " ")
        else:
            continue
        
    for i in range(len(value_tab)):
        if not isNaN(value_tab[i]):
            if i < len(value_tab)-4:
                if len(value_tab[i]) < 5 and "." in value_tab[i] and (value_tab[i+1][:4].isdigit() and len(count_number(value_tab[i+1][5:])) == 2):
                    value_tab.insert(i+1, " ")
                else:
                    continue
        else:
            continue
    #test = []
    for i in range(len(value_tab)):
        if not isNaN(value_tab[i]):
            if i < len(value_tab)-1:
                if "," in value_tab[i]:
                    if " " in value_tab[i+1]:
                        new_value = re.split(" ", value_tab[i+1])
                        #test.append(new_value)
                        value_tab.insert(i+2, new_value[1])
                        value_tab[i+1] = new_value[0]
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue
      
    # table = table[int(c):]
    for i in range(len(value_tab)):
        if not isNaN(value_tab[i]):
            if "P" == value_tab[i]:
                try:
                    for j in range(len(table)):
                        if value_tab[i] == ((table[j].text).replace("\t", "")).replace("\n", ""):
                            idx = j
                            break
                        else:
                            continue
                    value_tab[i] = table[idx]._children[0].text
                except:
                    continue
            else:
                continue    
        else:
            continue
    
    test_var = []
    
    for i in range(len(value_tab)):
        if i < len(value_tab)-4:
            if not isNaN(value_tab[i]):
                if value_tab[i+1][:4].isdigit() and len(count_number(value_tab[i+1][5:7])) == 2:
                    test_var = []
                    if i+10 < len(value_tab):
                        for j in range(i+1, i+10):
                            if not (value_tab[j+1][:4].isdigit() and len(count_number(value_tab[j+1][5:7])) == 2):
                                test_var.append(value_tab[j])
                            else:
                                break
                    else:
                        continue
                    if len(test_var) < 9:
                        for k in range(1, len(test_var)):
                            if not (value_tab[i+12][:4].isdigit() and len(count_number(value_tab[i+12][5:7])) == 2):
                                value_tab.insert((i+1)+k, " ")
                            else:
                                break
                    else:
                        continue
                else:
                    continue
            else:
                continue
        else:
            continue
        
    for i in range(10, len(value_tab)):
        if not isNaN(value_tab[i]):
            if 3 <= len(value_tab[i]) < 7 and all(char.isdigit() for char in value_tab[i]) and len(value_tab[i+1]) == 0:
                value_tab[i+1] = value_tab[i-10]
            else:
                continue
        else:
            continue
    
    
    
    for i in range(7, len(value_tab)):
        if i < len(value_tab)-10:
            if len(value_tab[i]) < 5 and len(value_tab[i-1]) < 5 and "." in value_tab[i] and "." in value_tab[i-1]:
                if len(value_tab[i+1]) == 0 and len(value_tab[i+2]) == 0 and len(value_tab[i+3]) == 0:
                    value_tab.pop((i+2))
                    print("Asteroid {}".format(i))
                else:
                    continue
            else:
                continue
        else:
            continue
    
    for i in range(7, len(value_tab)):
        if i < len(value_tab)-10:
            if (len(value_tab[i]) < 7 and all(char.isdigit() for char in value_tab[i]) and len(value_tab[i]) != 0) and (all(char.isdigit() for char in value_tab[i+1][:4]) and all(char.isalpha() for char in value_tab[i+1][5:7])) and len(value_tab[i+2]) == 0:
                    value_tab.pop((i+2))
                    print("Asteroid {}".format(i))
            else:
                continue
        else:
            continue
    
    p = [(7, 8), (8, 9)]
    
    if c == '10':
        p = p[0]
    elif c == '11':
        p = p[1]
    else:
        pass
    
    for i in range(7, len(value_tab)):
        if i < len(value_tab)-10:
            if len(value_tab[i]) < 9 and (any(char.isdigit() for char in value_tab[i]) and any(char.isalpha() for char in value_tab[i])) and len(value_tab[i-1]) == 0 and len(value_tab[i+1]) == 0:
                if not ((len(value_tab[i+p[1]]) < 5 and "." in value_tab[i+p[1]]) and (len(value_tab[i+p[0]]) < 5 and "." in value_tab[i+p[0]])):
                    value_tab.pop((i+1))
                    print("Asteroid {}".format(i))
                else:
                    continue
            else:
                continue
        else:
            continue
    
    for i in tqdm(range(len(value_tab))):
        if i < len(value_tab)-10:
            if not isNaN(value_tab[i]):
                if "Alternate" in value_tab[i] and len(value_tab[i-1]) == 0 and len(value_tab[i+1]) == 0:
                    while True:
                        value_tab.insert(i+1, "")
                        if "." in value_tab[i+8] and "." in value_tab[i+7] and "." in value_tab[i+6] and "." in value_tab[i+5]:
                            break
                        else:
                            value_tab.insert(i+1, "")
                            continue
                elif "(" in value_tab[i]:
                    while True:
                        value_tab.insert(i+1, "")
                        if "." in value_tab[i+8] and "." in value_tab[i+7] and "." in value_tab[i+6] and "." in value_tab[i+5]:
                            break
                        else:
                            value_tab.insert(i+1, "")
                            continue
                elif "Alternate" in value_tab[i+1] and "." in value_tab[i]:
                    while True:
                        value_tab.insert(i+1, "")
                        if "." in value_tab[i+10] and "." in value_tab[i+9] and "." in value_tab[i+8] and "." in value_tab[i+7]:
                            break
                        else:
                            continue
                else:
                    continue
            else:
                continue
        else:
            continue
                                                                 
   
    # if not (len(value_tab[-int(c)]) == 0 or all(char.isdigit() for char in value_tab[-int(c)])):
    #            value_tab.insert(-int(c)+1, " ")
    
    test_list = [value_tab[n:n+int(c)] for n in range(0, len(value_tab), int(c))]
    
    

i = [(4, 5), (5, 6)]
    
if c == '10':
    i = i[0]
elif c == '11':
    i = i[1]
else:
    pass    

number = [value_tab[i] for i in range(0, len(value_tab), int(c))]

name = [value_tab[i] for i in range(1, len(value_tab), int(c))]           
        
L = [value_tab[i] for i in range(i[0], len(value_tab), int(c))]

B = [value_tab[i] for i in range(i[1], len(value_tab), int(c))]

sv_df = pd.DataFrame(columns=["Number", "Name", "Prov.Desig", "L", "B", "Ref"])

sv_df["Number"] = number
sv_df["Name"] = name
sv_df["L"] = L
sv_df["B"] = B