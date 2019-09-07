# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 15:27:58 2019

Create copies of dbf files as csv files 

@author: Celia
"""

import csv
from dbfpy import dbf
import os

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU"

for filename in directory:
    
    if filename.endswith('.dbf'):
        print ("Converting %s to csv" % filename)
        csv_fn = filename[:-4]+ ".csv"
        with open(csv_fn,'wb') as csvfile:
            in_db = dbf.Dbf(filename)
            out_csv = csv.writer(csvfile)
            names = []
            for field in in_db.header.fields:
                names.append(field.name)
            out_csv.writerow(names)
            for rec in in_db:
                out_csv.writerow(rec.fieldData)
            in_db.close()
            print ("Done...")
