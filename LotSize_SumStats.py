# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 15:15:16 2019

@author: Celia
"""

import os
import pandas as pd

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET"

city_dict = dict()

for in_file in os.listdir(directory):
    city = pd.read_csv(in_file) 
    local_dict = dict()
    
    #only include blocks where the number of houses is greater than 0    
    local_dict['mean'] = (city['Acres']/city['Join_Count'][(city['Join_Count'] > 0)]).mean()
    local_dict['median'] = (city['Acres']/city['Join_Count'][(city['Join_Count'] > 0)]).median()
    local_dict['stanard_dev'] = (city['Acres']/city['Join_Count'][(city['Join_Count'] > 0)]).std()
    local_dict['min'] = (city['Acres']/city['Join_Count'][(city['Join_Count'] > 0)]).min()
    local_dict['max'] = (city['Acres']/city['Join_Count'][(city['Join_Count'] > 0)]).max()
    
    
    city_label = in_file.split("ET")[0]
    city_dict[city_label] = local_dict
    
city_df = pd.DataFrame(city_dict).transpose()