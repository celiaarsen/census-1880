# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 09:43:17 2019

Walk through all people that are geocoded, and divide into shape files for each city

Steps:
    -make dictionary called 'citycodes' from csv with city codes and city names
    -make a dictionary 'outfile_dict' of city codes and output file names
    -Walk thru each line of John Logan data and look at city code
    -check and see if the city code already has a tuple in outfile_dict
        -If it does, write the line to the file in the tuple
        -If it does not,
            -Create a new tuple in the outfile_dict where the key is the city code 
            and the value is the value of the code in the citycodes dictionary
            -Write the line to that file

@author: Celia Arsen
"""

import csv

city_code_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/IPUMS_cityCodes.csv'
in_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCities_XY.csv'
out_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/'
bad_data = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/no_city_data.csv'

#create citycodes citionary
city_codes = {}
with open(city_code_path, newline='\n') as f:
    reader = csv.DictReader(f) 
    for row in reader:
        city_codes[row['city_code']] = row['city_name']
        
#Create outfile_dict of city codes and output file names
#city_code : fileName
outfile_dict = {}

with open(in_path, newline='\n') as f:
    reader = csv.DictReader(f) 
    for row in reader:
        try:
            file_name = outfile_dict[row['CITY']]
            with open(out_path+file_name, 'a+', newline='') as o:
                w = csv.DictWriter(o, row.keys())
                w.writerow(row)
        except KeyError:
            try:
                outfile_dict[row['CITY']] = city_codes[row['CITY']]+'_IPUMS.csv'
                file_name = outfile_dict[row['CITY']]
                with open(out_path+file_name, 'a+', newline='') as o:
                    w = csv.DictWriter(o, row.keys())
                    w.writeheader()
                    w.writerow(row)
            except KeyError:
                with open(bad_data, 'a+', newline='') as o:
                    w = csv.DictWriter(o, row.keys())
                    w.writerow(row)
                
                
            