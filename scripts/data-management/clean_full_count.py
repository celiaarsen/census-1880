# -*- coding: utf-8 -*-
"""
Celia Arsen - cla2143@barnard.edu

Script for extracting Census observations that have XY coordinates, as 
geo-coded by John Logan's team at Brown.

Data are downloaded from IPUMS. 

Steven Ruggles, Sarah Flood, Ronald Goeken, Josiah Grover, Erin Meyer, Jose Pacas and Matthew Sobek. 
IPUMS USA: Version 9.0 [dataset]. Minneapolis, MN: IPUMS, 2019.
https://doi.org/10.18128/D010.V9.0
"""
import csv
path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/IPUMS_FullCount1880.csv'
out_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCities_XY.csv'

first = 1 
sanity_checker = 0
total_input = 0
hundred_thousand = 100000
million = 1000000
    
with open(path, newline='\n') as f:
    reader = csv.DictReader(f)       
    for row in reader:
        total_input += 1
        if (total_input % million == 0):
            print(total_input/million, ' million residents processed from input')
        if(row["XGPS"]!="999"):
            sanity_checker += 1
            if (sanity_checker % hundred_thousand == 0):
                print(sanity_checker/hundred_thousand, ' hundred thousand residents added to output')
            #print(row)
            with open(out_path, 'a+', newline='') as o:
                w = csv.DictWriter(o, row.keys())
                if (first==1):
                    w.writeheader()
                    first+=1
                w.writerow(row)
   
print('Done')             