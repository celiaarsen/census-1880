# -*- coding: utf-8 -*-
"""
Created on Sat Sep  7 16:23:26 2019

@author: Celia Arsen

-Goal of this script will be to join the number of people from certain occupations 
to city blocks
-Inputs should be something like:
    Albany_IPUMS.shp (contains field OCC with occupations) and
    AlbanyPD.shp (contains field popDense with population density)
-Eventually we want this to walk to through a directory and do it for every file in the directory

Steps:    
    1. Read in AlbanyPD.shp as target features
    2. Read in Albany_IPUMS.shp
    3. Create a copy of Albany_IPUMS.shp called AlbanyIPUMS_occs.shp
    4. Create dummy variable categories in AlbanyIPUMS_occs.shp for all occupations of interest
    5. Set AlbanyIPUMS_occs.shp as join features
    3. Set name and destination for output files 
        -Something like AlbanyOcc.shp
    4. Create field mapping objects
    5. Set merge rules:
        -Sum all dummy variables from AlbanyIPUMS_occs.shp
        -First for all variables of interest in AlbanyPD.shp
        -Remove any other variables that are not necessary
    5. Perform spatial join
    
"""
print("script started")
import arcpy
import csv

#Set global variables
arcpy.env.overwriteOutput = 1
print("arcpy imported")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/TestData/"
target_features = directory+"POPULATION DENSITY POLYGON FILE" 
individuals = directory+"FULL COUNT MICRO DATA FILE FROM IPUMS" 
join_features = "COPY OF FULL COUNT MICRO DATA TO JOIN TO POLYGON FILE"
out_features = directory+"OUTPUT FILE" 
occupations_path = directory+"occupations_sample.csv"
city_list = directory+"city_list.csv"

def set_file_paths(city):
    global directory
    global target_features
    global individuals
    global out_features

    target_features = directory+city+"PD.shp"
    individuals = directory+city+"_IPUMS_proj.shp"
    out_features = directory+city+"Occ.shp"
    
    print('target features: ', target_features)
    print('full count census: ', individuals)
    print('output file: ', out_features)

#Create a copy of full count features
def copy_features(city):
    #CopyFeatures(in_features, out_feature_class)
    arcpy.CopyFeatures_management(individuals, 
                                  directory+city+"_IPUMS_occs.shp")
    print("Copied full count data file")
    print()
    
#make the copy of individuals the join features
def set_join_features(city):
    global join_features
    join_features = directory+city+"_IPUMS_occs.shp"
    print('join features: ', join_features)
    print()
    
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
    
#Add a dummy field for each occupation    
#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
def add_dummy_fields():
    global join_features
    occupations = make_occ_dictionary()
    for occ in occupations:
        arcpy.AddField_management(join_features, occ, "SHORT")
    print("Added dummy fields")
    return occupations

#Make a codeblock that assigns rules for making dummy variables
def make_code_block(field_name, occupations):
    field = "'"+field_name+"'"

    codeblock = f"""
def calc_field(occ_code):
    occ = str(occ_code)
    if (occ in occupations[{field}]):
        return 1
    else:
        return 0 """
    return codeblock
    
#calculate the dummy variables for occupation fields      
def calculate_fields(occupation_categories):
    global join_features
    #for each of the dummy variables
    for field_name in occupation_categories:
        #set the rules
        codeblock = make_code_block(field_name, occupation_categories) 
        #calculate the field
        arcpy.CalculateField_management(join_features, field_name, 
                                        "calc_field(!OCC!)","PYTHON3",codeblock)
    print("Calculated fields")

#Set merge rules for spatial join
#See https://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm
#for further documentation
def set_merge_rules(fieldMappings, occupations):
    global join_features
    #set the merge rule to sum for all of the occupation dummy variables
    for field in arcpy.ListFields(join_features):
        if(field.name in occupations):
            occsIndex = fieldMappings.findFieldMapIndex(field.name)
            occsFieldMap = fieldMappings.getFieldMap(occsIndex)
            occsFieldMap.mergeRule = "Sum"
            fieldMappings.replaceFieldMap(occsIndex, occsFieldMap)
        #drop all other variables from join features if not required
        elif (not(field.required)):
            #remove all other non-required fields in the joinFeatures table
            x = fieldMappings.findFieldMapIndex(field.name)
            fieldMappings.removeFieldMap(x)
    print("Merge rules set")
    return fieldMappings
    
#Set field mappings 
#See https://pro.arcgis.com/en/pro-app/arcpy/classes/fieldmappings.htm
#for further documentation
def set_field_mappings(occupations):
    global target_features
    global join_features
    
    fieldMappings = arcpy.FieldMappings()
    fieldMappings.addTable(target_features)
    fieldMappings.addTable(join_features)
    
    fieldMappings = set_merge_rules(fieldMappings, occupations)
    print("Field mappings set")
    return fieldMappings

#aggregate the individual data up to the block level
#see https://pro.arcgis.com/en/pro-app/tool-reference/analysis/spatial-join.htm
#for further documentation    
def spatial_join(occupations):
    fieldMappings = set_field_mappings(occupations)
    arcpy.SpatialJoin_analysis(target_features, join_features, out_features,
                               "JOIN_ONE_TO_ONE", "KEEP_ALL", 
                               fieldMappings, "COMPLETELY_CONTAINS")
    print()
    print("Spatial join finished!")

############################################################################## 
    
if __name__ == '__main__':
    with open(city_list, newline='\n') as f:
        for city in f: 
            print()
            print()
            print()
            print("*************************************")
            city_stripped = city.strip()
            print(city_stripped)
            try:
                set_file_paths(city_stripped)
                copy_features(city_stripped)
                set_join_features(city_stripped)
                occupations = add_dummy_fields()
                calculate_fields(occupations)
                spatial_join(occupations)
            except:
                print()
                print("!!!!!!!!!!!!!!!!!!!!!!!")
                print("error processing ", city_stripped)
                print("Check results for this city")
                print("!!!!!!!!!!!!!!!!!!!!!!!")
                













