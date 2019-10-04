# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:23:26 2019

@author: Celia Arsen

-Goal of this script will be to join the number of people from certain occupations 
to city blocks
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
    
    Lines that are commented out with three single quotes should be uncommented before execution
"""
print("script started")
import arcpy


arcpy.env.overwriteOutput = 1
print("arcpy imported")
directory = "C:/Users/Celia/Desktop/1880DataByCity-Copy/Albany/"
target_features = directory+"AlbanyET.shp"
join_features = 'RESET AFTER COPYING TARGET FEATURES'
individual_people = directory+"AlbanyCE.shp"
out_features = directory+"AlbanyOcc.shp"
print('target features: ', target_features)
print('full count census: ', individual_people)


#CopyFeatures(in_features, out_feature_class)
#arcpy.CopyFeatures_management(individual_people, directory+"AlbanyCE_occs.shp")
#make the copy of AlbanyCE the join features
join_features = directory+"AlbanyCE_occs.shp"
print("Copied CE file")
print('join features: ', join_features)
field_name = "occs"

codeblock = """
def occ_dummy(occupation):
    if (occupation=="LABORER"):
        return 1
    else:
        return 0 """

#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
'''arcpy.AddField_management(joinFeatures, field_name, "SHORT")'''
#CalculateField(in_table, field, expression, {expression_type}, {code_block})
#calculate a dummy variable for the attribute occs
'''arcpy.CalculateField_management(join_features, field_name, "occ_dummy(!occlabelB!)", "PYTHON3", codeblock)'''

#initialize a FieldMappings object with the target and join features
fieldMappings = arcpy.FieldMappings()
fieldMappings.addTable(target_features)
fieldMappings.addTable(join_features)

#Set merge rules
#Rule for occs should be "Sum", so we get the count of people with that occupation on the block
occsIndex = fieldMappings.findFieldMapIndex("occs")
occsFieldMap = fieldMappings.getFieldMap(occsIndex)
occsFieldMap.mergeRule = "Sum"
fieldMappings.replaceFieldMap(occsIndex, occsFieldMap)

#We don't need to join any of the other fields from the Census to the blocks, so remove those 
#fieldMaps from the fieldMappings
for field in arcpy.ListFields(join_features):
    if ((field.name != 'occs') and not(field.required)):
        #remove all other non-required fields in the joinFeatures table
        x = fieldMappings.findFieldMapIndex(field.name)
        fieldMappings.removeFieldMap(x)

#perform the spatial join
arcpy.SpatialJoin_analysis(target_features, join_features, out_features,"JOIN_ONE_TO_ONE", "KEEP_ALL", fieldMappings, "COMPLETELY_CONTAINS")

print('finished!')
    

