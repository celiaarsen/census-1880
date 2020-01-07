# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 13:19:36 2019

Create point shapefiles from XY coordinates of residents

Step:
    -import arcpy and print when done
    -walk through directory of XY tables. For each:
        -Create a shapefile from the XY table and put it in IPUMS_shp
        -find the spatial reference that the shp file should have from table of spatial references
        -Define the projection for the shp file we just made

@author: Celia Arsen
"""

import os
import arcpy
import pandas as pd
print('imported arcpy')

in_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/NoMissingCoordinates/'
out_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCitiesSHP/'
coordinate_systems = pd.read_csv('C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/city_projections.csv') 
coordinate_systems = coordinate_systems.set_index('city')

for city in os.listdir(in_path):
    try:
        name = city.rstrip('.csv')
        print('working on ', city)
        #XYTableToPoint(in_table, out_feature_class, x_field, y_field, {z_field}, {coordinate_system})
        arcpy.management.XYTableToPoint(in_path+city, out_path+name+'.shp', 'XGPS', 'YGPS')
        print('wrote XY table for ', city)
            
        #Get coordinate reference system for the city
        #I REALIZED THIS IS NOT THE RIGHT WAY TO GO ABOUT THIS
        #THE RIGHT THING TO DO WOULD BE TO USE THE DEFINEPROJECTION TOOL TO SET THE CRS AS 4236,
        #AND THEN USE THE PROJECT TOOL TO PROJECT TO THE STATEPLANE CRS
        city_system = coordinate_systems.loc[city.rstrip('_IPUMS.csv'), 'wkid']
        
        #DefineProjection(in_dataset, coor_system)
        arcpy.DefineProjection_management(out_path+name+'.shp', str(city_system))
        print('set coordinate reference system for ', city)
       
    except:
        print(city, 'encountered an error')
    
    


