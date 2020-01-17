# -*- coding: utf-8 -*-
"""
Created on Fri Jan 17 12:21:44 2020

Tabulate occupational frequencies by region

@author: Celia
"""
import pandas as pd
import csv

path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/Occupation_Tabs/"

def make_code_dict():
    codes = pd.read_csv(path+"occupation_codes.csv")
    codes_dict = {}
    for index, row in codes.iterrows():
        occ_num = str(row['OCC'])
        codes_dict[occ_num] = 0
    
    codes_dict['997'] = 0    
    return codes_dict 

def make_region_dict():
    regions = pd.read_csv("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/regions.csv")
    regions_dict = {}
    for index, row in regions.iterrows():
        regions_dict[row['city']]=row['region']
    return regions_dict

def update_region_dict(row, region_dict):
    for occ in row.keys():
        print()
        print(occ)
        if(occ!='city'):
            region_dict[str(occ)] += int(row[occ])

#dictionaries for northeast, midwest/west, and southern cities
ne = make_code_dict()
mw_w = make_code_dict()
s = make_code_dict()

regions = make_region_dict()
in_file = path+"city_occ_tabs.csv"
with open(in_file, newline='\n') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if(regions[row['city']]=='NE'):
            print(row)
            update_region_dict(row, ne)           
        elif(regions[row['city']]=='MW-W'):
            update_region_dict(row, mw_w)
        elif(regions[row['city']]=='S'):
            update_region_dict(row, s)
        else:
            print(row)
            
ne_occs_df = pd.DataFrame(ne, index = ['NE'])
mw_occs_df = pd.DataFrame(mw_w, index = ['MW-W'])
s_occs_df = pd.DataFrame(s, index = ['S'])

ne_occs_df.to_csv(path+"NE_occ_tabs.csv")
mw_occs_df.to_csv(path+"MW_occ_tabs.csv")
s_occs_df.to_csv(path+"S_occ_tabs.csv")

