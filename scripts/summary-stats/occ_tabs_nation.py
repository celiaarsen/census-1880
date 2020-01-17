# -*- coding: utf-8 -*-
"""
Created on Friday January 12, 2020

Tabulate occupational frequencies in the country overall

Input:
    -Folder with the IPUMS data (individual level) for each city
        Called "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates"
Output:
    -Table of occupational frequencies in the country overall
    2. Table of occupational frequencies by region
    3. Table of occupational frequencies by city
    
@author: Celia Arsen
"""
import csv
import os
import pandas as pd

in_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates/"
out_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/Occupation_Tabs/"

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


                






