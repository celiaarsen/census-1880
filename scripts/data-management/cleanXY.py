# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 10:54:10 2019

Go through XY data and make copies that do not have any bad data

@author: Celia Arsen
"""

import csv
import os

in_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCitiesFullCount/'
out_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates/'
bad_data_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/bad_XY_data.csv'

os.chdir('C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCitiesFullCount/')

started_files = []

for city in os.listdir(in_path):
    with open(in_path+city, newline='\n') as f:
        reader = csv.DictReader(f) 
        for row in reader:
            if((row['XGPS']!='999' and row['XGPS']!='998' and row['YGPS']!='999' and row['YGPS']!='998') & (city in started_files)):
                with open(out_path+city, 'a+', newline='') as o:
                    w = csv.DictWriter(o, row.keys())
                    w.writerow(row)
            elif(row['XGPS']!='999' and row['XGPS']!='998' and row['YGPS']!='999' and row['YGPS']!='998'):
                with open(out_path+city, 'a+', newline='') as o:
                    started_files.append(city)
                    w = csv.DictWriter(o, row.keys())
                    w.writeheader()
                    w.writerow(row)
            else:
                with open(bad_data_path, 'a+', newline='') as o:
                    w = csv.DictWriter(o, row.keys())
                    w.writerow(row)
            