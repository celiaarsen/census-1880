# -*- coding: utf-8 -*-
"""
Created on Sat May  4 14:44:19 2019

@author: Celia
"""
import pandas as pd
import os

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET"

exclude_vars = ['Join_Count','TARGET_FID', 'Shape_Leng', 'Acres', 'acres','PopDense', 'Shape_Area', 'city']
 
def gen1_avg(city):
    gen1 = ['brit1Bn','canada1Bn','china1Bn','danish1Bn','french1Bn','german1Bn','irish1Bn','japan1Bn','norway1Bn','swede1Bn']
    city['gen1'] = city[gen1].sum(axis=1)   
    gen1_sum = city['gen1'].sum()
    if(gen1_sum>0):
        gen1_avg = (city['gen1']*city['PopDense']).sum()/gen1_sum
    else:
        gen1_avg = ""
    return gen1_avg

def gen2_avg(city):
    gen2 = ['brit2Bn','canada2Bn','china2Bn','danish2Bn','french2Bn','german2Bn','irish2Bn','japan2Bn','norway2Bn','swede2Bn']
    city['gen2'] = city[gen2].sum(axis=1)   
    gen2_sum = city['gen2'].sum()
    if(gen2_sum>0):
        gen2_avg = (city['gen2']*city['PopDense']).sum()/gen2_sum
    else:
        gen2_avg = ""
    return gen2_avg
    

mydict = dict()
for in_file in os.listdir(directory):
    city = pd.read_csv(in_file) 
    headers = list(city)
    
    minidict = dict()
    #print(in_file)
    for var in headers:
        if(var not in exclude_vars):
            #print(var)
            pop_sum = city[var].sum()
            if(pop_sum>0):
                avg = (city[var]*city['PopDense']).sum()/pop_sum
            else:
                avg = ""
            minidict[var] = avg

            
    minidict['totalPop'] = city['population'].sum()
    minidict['gen1'] = gen1_avg(city)
    minidict['gen2'] = gen2_avg(city)
    
    
    city_label = in_file.split("ET")[0]  
    mydict[city_label] = minidict

df = pd.DataFrame(mydict).transpose() 
