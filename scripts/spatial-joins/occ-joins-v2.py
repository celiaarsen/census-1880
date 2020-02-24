# -*- coding: utf-8 -*-
"""
Created on Sun Feb 23, 2020

@author: Celia Arsen

README

Change lines 47 and 49 to the file path of your local geodatabase and working directory
NOTE: remove_extra_file() function does not currently work (probably due to a 
schema lock issue). This means that there will be one extra intermediate file in
the output for each city.

-Goal of this script will be to join the number of people from certain occupations 
to city blocks
-Inputs should be something like:
    Albany_IPUMS_proj (contains field OCC with occupations) and
    AlbanyPD (contains field popDense with population density)

Script logical steps:
    1. Create dictionary of occupations 
    2. Read in AlbanyPD as target features
    3. Read in Albany_IPUMS_proj as join features
    4. Set name and destination for output files 
        -Something like AlbanyOcc
    5. For each of the occupational categories in the occ dictionary:
        -select the rows in Albany_IPUMS_proj that have that occupation
        -create field mapping objects
        -Set merge rules:
            -Remove any variables that are not necessary in Albany_IPUMS_proj
            -Remove extra TARGET_FID fields from AlbanyPD
        -perform spatial join (the first time it should be to AlbanyPD, 
                               the subsequent times will be to AlbanyOCC or
                               AlbanyOcc_new, rotating everytime, so the target
                               features and output features are never the same)
        -Rename the Join_Count in the output file to the name of the occupation
    6. Remove intermediate file(s)
    
"""
print("script started")
import arcpy
import csv

print("arcpy imported")

#Set global variables
arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Occupations/Occupations.gdb"
arcpy.env.overwriteOutput = 1
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Occupations/"
target_features = "POPULATION DENSITY POLYGON FILE" 
join_features = "FULL COUNT MICRO DATA TO JOIN TO POLYGON FILE"
out_features = "OUTPUT FILE" 
#csv with occupational categories and their corresponding occupational codes
#from IPUMS, see: https://usa.ipums.org/usa/volii/occ1880.shtml#prof
occupations_path = directory+"occupation_codes.csv"  
city_list = directory+"city_list.csv"
occupations = {} #will be a dictionary of occupations and their codes

#Make a dictionary with occupational categories and their codes
def make_occ_dictionary():
    occupations = {}
    with open(occupations_path, newline='\n') as f:
        reader = csv.DictReader(f)
        #the following for loop makes 'occupations' a dictionary, 
        #where the keys are occupational categories 
        #and the values are a list of the corresponding occupational codes
        for row in reader:
            try:
                occupations[row["Category"]].append(row["OCC"])
            except:
                occupations[row["Category"]] = [row["OCC"]]
    print("Created occupation dictionary")
    return occupations

def set_file_paths(city):
    global target_features
    global join_features
    global out_features
    
    join_features = city+"_IPUMS_proj"
     
    #set target feature name. The first time it should be cityPD, afterwards
    #it should be the most recent target features
    if(city in out_features):
        target_features = out_features
    else:
        target_features = city+"PD"
    
    #set output feature name. We use 
    if(out_features==city+"Occs"):
        out_features = city+"Occs_new"
    elif(out_features==city+"Occs_new"):
        out_features = city+"Occs"
    else:
        out_features = city+"Occs"
    """   
    print('target features: ', target_features)
    print('join features: ', join_features)
    print('output block file: ', out_features)
    """
    
#Set merge rules for spatial join
#See https://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm
#for further documentation
def set_merge_rules(fieldMappings):
    global join_features
    global target_features
    for field in arcpy.ListFields(join_features):
        #drop all other variables from join features if not required
        if(not(field.required)):
            #remove all other non-required fields in the joinFeatures table
            x = fieldMappings.findFieldMapIndex(field.name)
            fieldMappings.removeFieldMap(x)
    #Remove unnecessary TARGET_FID fields       
    for field in arcpy.ListFields(target_features):
        if(not(field.required) and "TARGET" in field.name):
            x = fieldMappings.findFieldMapIndex(field.name)
            fieldMappings.removeFieldMap(x)
        elif(field.name in occupations.keys()):
            occsIndex = fieldMappings.findFieldMapIndex(field.name)
            occsFieldMap = fieldMappings.getFieldMap(occsIndex)
            occsFieldMap.mergeRule = "First"
            fieldMappings.replaceFieldMap(occsIndex, occsFieldMap)
    #print("Merge rules set")
    return fieldMappings
    
#Set field mappings 
#See https://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm
#for further documentation
def set_field_mappings():
    global target_features
    global join_features
    
    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable(target_features)
    fieldMappings.addTable(join_features)
    
    fieldMappings = set_merge_rules(fieldMappings)
    #print("Field mappings set")
    return fieldMappings

#SelectLayerByAttribute(in_layer_or_view, {selection_type}, {where_clause}, {invert_where_clause})
def select_occupations(occ_category):
    occ_codes = occupations[occ_category]
    where_clause = ""
    for code in occ_codes:
        where_clause += " OCC = " + code + " OR"
    
    where_clause = where_clause.rstrip("OR")

    #print(where_clause)

    selected_features = arcpy.SelectLayerByAttribute_management(join_features, selection_type="NEW_SELECTION", 
                                       where_clause=where_clause)

    return selected_features
    
#aggregate the individual data up to the block level
#see https://pro.arcgis.com/en/pro-app/tool-reference/analysis/spatial-join.htm
#for further documentation    
def spatial_join(selected_features):
    
    fieldMappings = set_field_mappings()
    arcpy.SpatialJoin_analysis(target_features, selected_features, out_features,
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", 
                               fieldMappings, "COMPLETELY_CONTAINS")
    #print("Spatial join finished!")
    
#AlterField(in_table, field, {new_field_name}, 
#{new_field_alias}, {field_type}, {field_length}, {field_is_nullable}, {clear_field_alias})    
def rename_field(occupation_name):
    try:
        arcpy.AlterField_management(out_features, 'Join_Count_1', occupation_name, 
                                occupation_name)
    except:
        arcpy.AlterField_management(out_features, 'Join_Count', occupation_name, 
                                occupation_name)

#This doesn't currently work, I think because of a schema lock issue, probably
#which means there will be an extra intermediate file for each one of the cities
def remove_extra_file(city_name):
    if(len(occupations.keys())%2==0):
        #we want to use CityOccs_new
        arcpy.Delete_management(city+"Occs")
    else:
        #we want to use CityOccs
        arcpy.Delete_management(city+"Occs_new")


############################################################################## 
    
if __name__ == '__main__':
    occupations = make_occ_dictionary()
    with open(city_list, newline='\n') as f:
        for city in f: 
            first_join = True
            print()
            print()
            print()
            print("*************************************")
            city_stripped = city.strip()
            print(city_stripped)
            try:
                for occupation in occupations:
                    print(occupation)
                    set_file_paths(city_stripped)
                    selected_features = select_occupations(occupation)
                    spatial_join(selected_features)
                    rename_field(occupation)
                #remove_extra_file(city) #This function doesn't currently work
            
            except:
                print()
                print("!!!!!!!!!!!!!!!!!!!!!!!")
                print("error processing ", city_stripped)
                print("Check results for this city")
                print("!!!!!!!!!!!!!!!!!!!!!!!")
            
                
                













