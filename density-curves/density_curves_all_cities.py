# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 15:26:44 2019

@author: Celia Arsen

This script was written for analyzing population densities in 1880 U.S. cities
for Barnard History Professor Gergo Baics' research.
 
We start with a csv file, where each observation is a city block. Each observation 
has the population density of the block ( measured in people per acre). It also has 
the number of people from each ethnic category that live on the block. These files were 
created in ArcGIS with 1880 U.S. Census micro-data. 

Our goal is to see what portion of the population lived at different density levels,
and if this varies by ethnicity. For example, were German immigrants more likely
to be living on high-density blocks than than the native white population?

We divide the population density into density brackets. For Manhattan, we use 
0 to 1440, with 40 step intervals. Then we find what percent of an ethnic population 
is living within each density bracket.
"""
import os
import math
import pandas as pd
   
#set working directory
os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/AllCitiesET"
out_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Ethnicity/DensityCurves_20step/"

#Global static variables 
STEP = 20
#columns we do not need for the final output
EXTRA_COLS = ['Join_Count','TARGET_FID','Shape_Leng','Acres','PopDense','Shape_Area']

def divide_densities(in_file, max_density):
    #get the headers, the variable names from the file
    headers = list(in_file)

    #create density brackets for the data
    density_brackets = []
    for i in range(0, max_density + STEP, STEP):
        density_brackets.append(i)
        
    #dictionary to initialize the population brackets    
    mydict = dict()
       
    for header in headers:
        if header != 'city':
            current_list = list()
        for i in range(0-STEP,max_density,STEP): 
            the_sum = in_file[header][(in_file['PopDense'] >= i) & (in_file['PopDense'] <= i+STEP)].sum()
            current_list.append(the_sum)
                
        mydict[header] = current_list
    
    #done dividing the data. Make the dataframe        
    return pd.DataFrame(mydict, index = density_brackets)    
   

#clean up file and remove unnecessary fields
def clean_file(df):
    headers = list(df)
    drop_cols = list()
    for header in headers:
        if header in EXTRA_COLS:
            drop_cols.append(header)
            
    clean_df = df.drop(columns = drop_cols)
    return clean_df
    
#Find the percent of the population living at each density level
def make_percents(df):
    #get the headers, the variable names from the file
    headers = list(df)
    
    for header in headers:
        sum = df[header].sum()
        percent_label = header + '_P'
        df[percent_label] = (df[header] / sum) * 100
    return df

    
def main():   
    for city in os.listdir(directory):
        if city != 'CompositeCityET_copy.csv':
            in_file = pd.read_csv(city) 
            max_density = math.floor((in_file['PopDense']).max() + STEP)
        
            print(city)
            df = divide_densities(in_file, max_density)
            df = clean_file(df)
            df = make_percents(df)
        
            city_label = city.split("ET")[0]
        
            #write the dataframe to a csv file
            df.to_csv(out_path+city_label+'DC_'+str(STEP)+'step.csv')
        
main()              
                
                
                
                