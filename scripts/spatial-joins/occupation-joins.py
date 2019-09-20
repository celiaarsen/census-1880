# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:23:26 2019

@author: Celia Arsen

-Goal of this script will be to join the number of people from certain occupational 
categories to city blocks
-Inputs should be something like:
    AlbanyCE.shp (contains field occlabelB with occupations) and
    AlbanyET.shp (contains field popDense with population density)
-Eventually we want this to walk to through a directory and do it for every file in the directory
    
Pre-processing:
    1. May want to exclude beforehand certain people from AlbanyCE.shp
    
Steps:    
    1. Read in AlbanyET.shp as target features
    2. Read in AlbanyCE.shp
    3. Create a (temporary) copy of AlbanyCE.shp called AlbanyCE_occs.shp
    4. Create dummy variable categories in AlbanyCE_occs.shp for any occupations of interest
    5. Set AlbanyCE_occs.shp as join features
    3. Set destination for output files (will want to be set dynamically, eventually)
        -Something like AlbanyOcc.shp
    4. Create field mapping objects
    5. Set merge rules:
        -Sum all dummy variables from AlbanyCE_occs.shp
        -First for all variables of interest in AlbanyET.shp
        -Remove any other variables that are not necessary
    5. Perform spatial join
"""
print("script started")
import arcpy
print("arcpy imported")
directory = "C:/Users/Celia/Desktop/1880DataByCity - Copy/Albany"
targetFeatures = directory+"AlbanyET.shp"
individualPeople = directory+"AlbanyCE.shp"

