# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:23:26 2019

@author: Celia Arsen

-Goal of this script will be to join the number of people from certain occupational 
categories to city blocks
-Inputs should be something like:
    AlbanyCE.shp (contains field occlabelB with occupations) and
    AlbanyET.shp (cotains field popDense with population density)
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
directory = "C:/Users/Celia/Desktop/1880DataByCity-Copy/Albany/"
target_features = directory+"AlbanyET.shp"
print(target_features)
individual_people = directory+"AlbanyCE.shp"
print(individual_people)

#CopyFeatures(in_features, out_feature_class)
arcpy.CopyFeatures_management(individual_people, directory+"AlbanyCE_occs.shp")
joinFeatures = directory+"AlbanyCE_occs.shp"
print("Copied CE file")
field_name = "occs"

codeblock = """
def occ_dummy(occupation):
    if (occupation=="LABORER":
        return 1
    else:
        return NULL """

#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
arcpy.AddField(joinFeatures, field_name, "SHORT")
#CalculateField(in_table, field, expression, {expression_type}, {code_block})
arcpy.CalculateField(joinFeatures, field_name, "occ_dummy(!occs!", "PYTHON3", codeblock)

