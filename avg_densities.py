# -*- coding: utf-8 -*-
"""
Created on Sun Apr 21 19:00:48 2019

@author: Celia
"""
import pandas as pd
import os

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/CompositeCity/CompositeCity")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/CompositeCity/CompositeCity"

#city = pd.read_csv("NYCManhattanET_copy.csv")

mydict = dict()

for city in os.listdir(directory):
    in_file = pd.read_csv(city) 
    
    #get the total population of the city
    totalPop = in_file['population'].sum()
    #average block density
    avgBlockPD = in_file['PopDense'][(in_file['PopDense'] > 0)].mean()
    #average experienced density    
    avgExpPD = (in_file['population']*in_file['PopDense']).sum()/totalPop
    
    city_name = city.split("ET")[0]
    mydict[city_name] = {'totalPop': totalPop, 'avgBlockPD': avgBlockPD, 'avgExpPD': avgExpPD}
    
df = pd.DataFrame(mydict).transpose()
