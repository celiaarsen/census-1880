# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 22:30:18 2019

Redefine the projection for XY IPUMS data

@author: Celia Arsen
"""
import pandas as pd
import os
import arcpy
print('arcpy imported')

in_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/AllCitiesSHP/Unprojected/'
out_path = 'C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/IPUMS_shp_proj/'

coordinate_systems = pd.read_csv('C:/Users/Celia/Desktop/EthnicityUrbanHGIS/IPUMS_FullCount/city_projections.csv') 
coordinate_systems = coordinate_systems.set_index('city')

for filename in os.listdir(in_path):
    #I say dbf even though we want to look at the shp file bc there are two files
    #with the .shp extention for each shapefile
    #I already did NYC by hand, so it is excluded here
    if (filename.endswith('.dbf') and 'NewYork' not in filename):
        try:
            city = filename.rstrip('_IPUMS.dbf')
            print(city)
            #Define the projection of the file as WGS84 (EPSG: 4326) 
            arcpy.DefineProjection_management(in_path+city+'_IPUMS.shp', '4326')
            print('set coordinate reference system to 4326 for ', city)
        except:
            print('setting coordinate reference system 4326 for', filename, 'was unsuccessful')
        try:
            #Now, project it to the proper stateplane projection
            state_plane = arcpy.SpatialReference(coordinate_systems.loc[city, 'wkid'])
            transformation = 'WGS_1984_(ITRF00)_To_NAD_1983'
            #arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
            arcpy.Project_management(in_path+city+'_IPUMS.shp', out_path+city+'_IPUMS_proj.shp', state_plane, transform_method=transformation)
            print('created projected shp file for ', city)
        except:
            print('projecting ', filename, ' to stateplane failed')
    