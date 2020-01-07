# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 01:05:09 2019

@author: Celia
"""
import arcpy
print("arcpy imported")
arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/SSHA-Arsen/SSHA-Arsen.gdb"

target_features = "NYCManhattanBL_proj"
join_features = "NYCManhattan_IPUMS_proj"
out_features = "NYC_irish_german_gender"

#initialize a FieldMappings object with the target and join features
fieldMappings = arcpy.FieldMappings()
fieldMappings.addTable(target_features)
fieldMappings.addTable(join_features)
print("field mappings set")

fields_to_keep = ["irish","irishFem","irishMale","irishFW","irishMW","german",
                  "germanFem","germanMale","germanFW","germanMW","clerk","tailor","cigarMaker"]
#Set merge rules
#Rule for all fields should be "Sum", so we get the count of people with that trait on the block
for attribute in fields_to_keep:
    fieldIndex = fieldMappings.findFieldMapIndex(attribute)
    fieldMap = fieldMappings.getFieldMap(fieldIndex)
    fieldMap.mergeRule = "Sum"
    fieldMappings.replaceFieldMap(fieldIndex, fieldMap)

print("field maps set")

#We don't need to join any of the other fields from the Census to the blocks, so remove those 
#fieldMaps from the fieldMappings
for field in arcpy.ListFields(join_features):
    if ((field.name not in fields_to_keep) and not(field.required)):
        #remove all other non-required fields in the joinFeatures table
        x = fieldMappings.findFieldMapIndex(field.name)
        fieldMappings.removeFieldMap(x)

#perform the spatial join
arcpy.SpatialJoin_analysis(target_features, join_features, out_features,"JOIN_ONE_TO_ONE", "KEEP_ALL", fieldMappings, "COMPLETELY_CONTAINS")

print('finished!')