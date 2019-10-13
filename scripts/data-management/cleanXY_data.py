# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 14:50:20 2019

Create point shapefile from XY points in csv files

Steps:
    Walk through directory of city files
    Make 

@author: Celia Arsen
"""
import arcpy
print('arcpy imported')
#MakeXYEventLayer(table, in_x_field, in_y_field, out_layer, {spatial_reference}, {in_z_field})