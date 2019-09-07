# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 17:38:15 2019

Get the mean, median, sd, min, and max for block size in each city

@author: Celia
"""

import os
import pandas as pd

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET"
#make a dictionary of dictionaries
#Each dictionary will be a city, containing the mean, median, std, min, and max
city_dict = dict()

for in_file in os.listdir(directory):
    city = pd.read_csv(in_file) 
    local_dict = dict()
    
    local_dict['mean'] = city['Acres'].mean()
    local_dict['median'] = city['Acres'].median()
    local_dict['stanard_dev'] = city['Acres'].std()
    local_dict['min'] = city['Acres'].min()
    local_dict['max'] = city['Acres'].max()
    
    city_label = in_file.split("ET")[0]
    city_dict[city_label] = local_dict
    
df = pd.DataFrame(city_dict).transpose()
