# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 17:04:20 2019
inputs: csv files with each block and the sum of each ethnicity on the block
output: one csv fiel with 40 cities and the total number of people of each ethnicity

@author: Celia
"""

import os
import pandas as pd

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET"

exclude_vars = ['Join_Count','TARGET_FID', 'Shape_Leng', 'Acres', 'acres','PopDense', 'Shape_Area', 'city']

def gen1_sum(city):
    gen1 = ['brit1Bn','canada1Bn','china1Bn','danish1Bn','french1Bn','german1Bn','irish1Bn','japan1Bn','norway1Bn','swede1Bn']
    city['gen1'] = city[gen1].sum(axis=1)   
    gen1_sum = city['gen1'].sum()
    return gen1_sum

def gen2_sum(city):
    gen2 = ['brit2Bn','canada2Bn','china2Bn','danish2Bn','french2Bn','german2Bn','irish2Bn','japan2Bn','norway2Bn','swede2Bn']
    city['gen2'] = city[gen2].sum(axis=1)   
    gen2_sum = city['gen2'].sum()
    return gen2_sum

city_dict = dict()

for in_file in os.listdir(directory):
    city = pd.read_csv(in_file) 
    headers = list(city) 
    
    local_dict = dict()
    for var in headers:
        if(var not in exclude_vars):
            pop_sum = city[var].sum()
            local_dict[var] = pop_sum
    
    local_dict['gen1'] = gen1_sum(city)
    local_dict['gen2'] = gen2_sum(city)
    
    city_label = in_file.split("ET")[0]  
    city_dict[city_label] = local_dict
 
df = pd.DataFrame(city_dict).transpose() 