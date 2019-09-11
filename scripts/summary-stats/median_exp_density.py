# -*- coding: utf-8 -*-
"""
Created on Sat May  4 14:44:19 2019

Get the median "experienced density" for each city

@author: Celia
"""
import pandas as pd
import numpy as np
import os
import statistics as st

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/SampleCities")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/SampleCities"

exclude_vars = ['Join_Count','TARGET_FID', 'Shape_Leng', 'Acres', 'acres','PopDense', 'Shape_Area', 'city']
 
def group_gen1_gen2(city):
    gen1 = ['brit1Bn','canada1Bn','china1Bn','danish1Bn','french1Bn','german1Bn','irish1Bn','japan1Bn','norway1Bn','swede1Bn']
    city['gen1'] = city[gen1].sum(axis=1)   
    gen2 = ['brit2Bn','canada2Bn','china2Bn','danish2Bn','french2Bn','german2Bn','irish2Bn','japan2Bn','norway2Bn','swede2Bn']
    city['gen2'] = city[gen2].sum(axis=1)   
    return city

def calc_exp_median(city, var):
    #exp_densities will be a list of the densities each person actually lived at
    exp_densities = list()
    #on each block...
    for block in range(0,city[var].size,1):
        #add the population density to the list for each person that lived at that density       
        repeats = np.repeat(city['PopDense'][block], city[var][block])
        exp_densities.append(repeats)
        
    exp_densities = np.concatenate(exp_densities).ravel().tolist()
    median = st.median(exp_densities)
    return median

def main():
    mydict = dict()
    for in_file in os.listdir(directory):
        city = pd.read_csv(in_file) 
        city = group_gen1_gen2(city)
        headers = list(city)
        minidict = dict()
        #print(in_file)
        #for each varialbe (i.e. ethnicity)
        for var in headers:
            if(var not in exclude_vars):
                #print(var)
                pop_sum = city[var].sum()
                #if there are people of this ethnicity in the city, calculate the median exp density
                if(pop_sum>0):
                    median = calc_exp_median(city, var)
                #if there are not people of this ethnicity in the city, leave it as blank
                else:
                    median = ""
                #add the calculated median to a dictionary under the variable name
                minidict[var] = median           
       
        minidict['totalPop'] = city['population'].sum()
    
        city_label = in_file.split("ET")[0] 
        print(city_label)
        mydict[city_label] = minidict

    df = pd.DataFrame(mydict).transpose()
    return df
    
df = main()
