print("script started")
import arcpy

print("arcpy imported")

arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/TestData/TestData.gdb"
arcpy.env.overwriteOutput = 1
target_features = "AlbanyPD"
join_features = "Albany_IPUMS_proj"
out_features = "AlbanyOccs" 

#arcpy.SelectLayerByAttribute_management(join_features, "NEW_SELECTION", 
                                 #       '"OCC" = 29')
occ = 29
selection = arcpy.SelectLayerByAttribute_management(join_features, "NEW_SELECTION", 
                                        f'"OCC" = {occ}')
print(arcpy.GetCount_management(selection))
print("layer selected")

def set_merge_rules(fieldMappings):
    global join_features
    for field in arcpy.ListFields(join_features):
        #drop all other variables from join features if not required
        if(not(field.required)):
            #remove all other non-required fields in the joinFeatures table
            x = fieldMappings.findFieldMapIndex(field.name)
            fieldMappings.removeFieldMap(x)
            
    print("Merge rules set")
    return fieldMappings

def set_field_mappings():
    global target_features
    global join_features
    
    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable(target_features)
    fieldMappings.addTable(join_features)
    
    fieldMappings = set_merge_rules(fieldMappings)
    print("Field mappings set")
    return fieldMappings

arcpy.SpatialJoin_analysis(target_features, selection, out_features,
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", 
                               set_field_mappings(), "COMPLETELY_CONTAINS")

print("spatial join finished")