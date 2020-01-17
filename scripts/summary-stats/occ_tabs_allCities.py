# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 12:29:23 2019

Pre-processing:
    -Create a csv for each dbf file in the IPUMS (individual level data) for each city
    -Create a variable or dictionary, etc. that has the regions for each city
Input:
    -Folder with the IPUMS data (individual level) for each city
        Called "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates"
Output:
    1. Table of occupational frequencies in the country overall
    2. Table of occupational frequencies by region
    3. Table of occupational frequencies by city
    
@author: Celia Arsen
"""
import csv
import os
import pandas as pd
import numpy as np


in_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates/"
out_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/Occupation_Tabs/"

#create pandas df with all occupational codes and labels
codes = pd.read_csv("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/occupation_codes.csv")
#codes.index = codes['OCC']

#turn that df into a dictionary
codes_dict = {}
for index, row in codes.iterrows():
    codes_dict[row["OCC"]] = 0
    

###############################################################################
#Tabulate occupational frequencies in the contry overall#

occs = {}

for city in os.listdir(in_path):
    print(city)
    with open(in_path+city, newline='\n') as f:
        reader = csv.DictReader(f)
        #print(row)
        for row in reader:
            try:
                occs[row['OCC']]+=1
            #If that occupation hasn't been seen yet
            except:
                #add that occupation to the dictionary
                occs[row['OCC']] = 1
                
#make the dictionary into a pandas df
nation_occs_df = pd.DataFrame(occs, index = [0]).transpose()
#rename the column "count"
nation_occs_df = nation_occs_df.rename(columns={0:"count"})
#create a percentage column
nation_occs_df["percent"] = nation_occs_df["count"]/nation_occs_df["count"].sum()*100
#give index a name
nation_occs_df.index.name = 'OCC'
#write the dataframe to csv
nation_occs_df.to_csv(out_path+"nation_occ_tabs.csv")

################################################################################
#Tabulate occupational frequences by city#

city_occs = []

for city in os.listdir(in_path):
    city_name = city.rstrip("_IPUMS.csv")
    print(city_name)
    city_occs.append({city_name : })
    with open(in_path+city, newline='\n') as f:
        reader = csv.DictReader(f)
        #print(row)
        for row in reader:
            try:
                city_occs[city_name][row['OCC']]+=1
            #If that city hasn't been seen yet
            except:
                #add that city to the dictionary
                city_occs[city_name] = codes_dict
                city_occs[city_name][row['OCC']] = 1
                
city_occs = {}

city_name = "Nashville_IPUMS.csv".rstrip("_IPUMS.csv")
print(city_name)
with open(in_path+city, newline='\n') as f:
    reader = csv.DictReader(f)
    #print(row)
    for row in reader:
        try:
            city_occs[city_name][row['OCC']]+=1
        #If that occupation hasn't been seen yet
        except:
            #add that occupation to the dictionary
            city_occs[city_name] = codes_dict
            city_occs[city_name][row['OCC']] = 1

city_df = pd.DataFrame(city_occs)





