# -*- coding: utf-8 -*-
"""
Created on Sat Dec  8 17:18:09 2018
This script is designed to perform a spatial join between a polygon shapefile
(block level population density shapefile) and a point shapefile (AU).
All ethnic categories will be summed up to the block level.
Before running the program, make sure that the specified fields syntactically
specified in this program match those in the files you're using

Most importantly, note that the join features must not have any missing values,
and the population field in the join features class must be renamed 'population'
before running this program

@author: Celia Arsen, Gergo Baics, Barnard College
"""
print('program initiated')

#set appropriate input variables
#list of variables names to keep in the output file (ASCII encoding)
varName = 'varNames.txt' 
# polygon shape file to join to
targetFeatures = "D:/UrbanTransHistGIS/PopulationDensity/KansasCityPD/KansasCityPD/KansasCityPD.gdb/KansasCityPD"
#point features to join
#This should be a file that does not have any missing values (-999)
joinFeatures = "D:/UrbanTransHistGIS/PopulationDensity/KansasCityPD/KansasCityPD/KansasCityPD.gdb/KansasCityAU_posPop"
#name and location of output file
outFeatures = "D:/UrbanTransHistGIS/Ethnicity/KansasCityET/KansasCityET.shp"

#put info from the list of variables into a python list
vars_to_keep = list()
file = open(varName,'r')
lines = file.read().splitlines()
for line in lines:
    vars_to_keep.append(line)
print('instance variables set')

import arcpy
print('arcpy imported')

#initialize a FieldMappings object with the target and join features
fieldMappings = arcpy.FieldMappings()
fieldMappings.addTable(targetFeatures)
fieldMappings.addTable(joinFeatures)


#merge rule for population field should be 'first' 
#make sure to change the name of the 'poptotB' field to 'population' before 
#running this program
popIndex = fieldMappings.findFieldMapIndex("population")
popFieldMap = fieldMappings.getFieldMap(popIndex)
popFieldMap.mergeRule = "First"
fieldMappings.replaceFieldMap(popIndex, popFieldMap)

#merge rule for Acres field should be 'first' 
acreIndex = fieldMappings.findFieldMapIndex("Acres")
acreFieldMap = fieldMappings.getFieldMap(acreIndex)
acreFieldMap.mergeRule = "First"
fieldMappings.replaceFieldMap(acreIndex, acreFieldMap)

#merge rule for PopDense field should be 'first' 
densityIndex = fieldMappings.findFieldMapIndex("PopDense")
densityFieldMap = fieldMappings.getFieldMap(densityIndex)
densityFieldMap.mergeRule = "First"
fieldMappings.replaceFieldMap(densityIndex, densityFieldMap)

#get a list of the fields in the joinFeatures
for field in arcpy.ListFields(joinFeatures):
    #if the field in in the list of variables to keep
    if (field.name in vars_to_keep):
        #get the index where the map is in the the fieldMappings object
        fieldIndex = fieldMappings.findFieldMapIndex(field.name)
        #get the fieldmap that corresponds with this field
        fieldMap = fieldMappings.getFieldMap(fieldIndex)
        #change the mergeRule to Sum
        fieldMap.mergeRule = "Sum"
        #Replace the fieldMap with this new updated fieldMap
        fieldMappings.replaceFieldMap(fieldIndex, fieldMap)
    #remove all other non-required fields in the joinFeatures table
    #from the fieldMappings
    elif (not(field.required)):
        x = fieldMappings.findFieldMapIndex(field.name)
        fieldMappings.removeFieldMap(x)

#perform the spatial join
arcpy.SpatialJoin_analysis(targetFeatures, joinFeatures, outFeatures,"JOIN_ONE_TO_ONE", "KEEP_ALL", fieldMappings, "COMPLETELY_CONTAINS")

print('finished!')