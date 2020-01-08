# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 17:14:33 2019

Get the mean, median, sd, min, and max for building population in each city


@author: Celia
"""

import os
import pandas as pd

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU"

city_dict = dict()

for in_file in os.listdir(directory):
    city = pd.read_csv(in_file) 
    local_dict = dict()
    
    local_dict['mean'] = city['poptotB'].mean()
    local_dict['median'] = city['poptotB'].median()
    local_dict['stanard_dev'] = city['poptotB'].std()
    local_dict['min'] = city['poptotB'].min()
    local_dict['max'] = city['poptotB'].max()
    
    city_label = in_file.split("AU")[0]
    city_dict[city_label] = local_dict
    
df = pd.DataFrame(city_dict).transpose()