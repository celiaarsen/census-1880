# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 21:37:14 2019

For my senior thesis. 

Purpose is to take full count of IPUMS points, and 

@author: Celia
"""
import arcpy

arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/SSHA-Arsen/SSHA-Arsen.gdb"
in_table = "NYCManhattan_IPUMS_proj"

irishCode = """
def irish(birthplace):
    if (birthplace==414):
        return 1
    else:
        return 0 """
               
irishFemCode = """
def irishFem(irish, female):
    if(irish==1 and female==1):
        return 1
    else:
        return 0
"""

irishMaleCode = """
def irishMale(irish, male):
    if(irish==1 and male==1):
        return 1
    else:
        return 0
"""

irishFemWorkCode = """
def irishFemWork(irishFem, occ):
    if(irishFem==1 and occ<300):
        return 1
    else:
        return 0
"""

irishMaleWorkCode = """
def irishMaleWork(irishMale, occ):
    if(irishMale==1 and occ<300):
        return 1
    else:
        return 0
"""


####################Do the same for Germans####################################
germanCode = """
def german(birthplace):
    if (birthplace==453):
        return 1
    else:
        return 0 """

germanFemCode = """
def germanFem(german, female):
    if(german==1 and female==1):
        return 1
    else:
        return 0
"""

germanMaleCode = """
def germanMale(german, male):
    if(german==1 and male==1):
        return 1
    else:
        return 0
"""

germanMaleWorkCode = """
def germanMaleWork(germanMale, occ):
    if(germanMale==1 and occ<300):
        return 1
    else:
        return 0
"""

germanFemWorkCode = """
def germanFemWork(germanFem, occ):
    if(germanFem==1 and occ<300):
        return 1
    else:
        return 0
"""

#########################For occupations#######################################

clerkCode = """
def storeClerk(occ):
    if(occ==65):
        return 1
    else:
        return 0
"""

tailorCode = """
def tailor(occ):
    if(occ==252):
        return 1
    else:
        return 0
"""

cigarMakerCode = """
def cigarMaker(occ):
    if(occ==163):
        return 1
    else:
        return 0
"""

##############################################################################
#Add and calculate fields

#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
#CalculateField(in_table, field, expression, {expression_type}, {code_block})

#irish
'''
arcpy.AddField_management(in_table, 'irish', "SHORT")
print("added irish")
arcpy.CalculateField_management(in_table, 'irish', "irish(!BPL!)", "PYTHON3", irishCode)
print("calculated irish")
'''
'''
#irish & female
arcpy.AddField_management(in_table, 'irishFem', "SHORT")
print("added irish female")
arcpy.CalculateField_management(in_table, 'irishFem', "irishFem(!irish!,!Female!)", "PYTHON3", irishFemCode)
print("calculated irish female")
'''
#irish & male
arcpy.AddField_management(in_table, 'irishMale', "SHORT")
print("added irish male")
arcpy.CalculateField_management(in_table, 'irishMale', "irishMale(!irish!,!Male!)", "PYTHON3", irishMaleCode)
print("calculated irish male")

#irish & female & working
arcpy.AddField_management(in_table, 'irishFW', "SHORT")
print("added irish female workers")
arcpy.CalculateField_management(in_table, 'irishFW', "irishFemWork(!irishFem!,!OCC!)", "PYTHON3", irishFemWorkCode)
print("calculated irish female workers")

#irish & male & working
arcpy.AddField_management(in_table, 'irishMW', "SHORT")
print("added irish male workers")
arcpy.CalculateField_management(in_table, 'irishMW', "irishMaleWork(!irishMale!,!OCC!)", "PYTHON3", irishMaleWorkCode)
print("calculated irish male workers")

###################Do the same for German######################################

arcpy.AddField_management(in_table, 'german', "SHORT")
print("added german")
arcpy.CalculateField_management(in_table, 'german', "german(!BPL!)", "PYTHON3", germanCode)
print("calculated german")

#german & female
arcpy.AddField_management(in_table, 'germanFem', "SHORT")
print("added german female")
arcpy.CalculateField_management(in_table, 'germanFem', "germanFem(!german!,!Female!)", "PYTHON3", germanFemCode)
print("calculated irish female")

#german & male
arcpy.AddField_management(in_table, 'germanMale', "SHORT")
print("added german male")
arcpy.CalculateField_management(in_table, 'germanMale', "germanMale(!german!,!Male!)", "PYTHON3", germanMaleCode)
print("calculated german male")

#german & female & working
arcpy.AddField_management(in_table, 'germanFW', "SHORT")
print("added german female workers")
arcpy.CalculateField_management(in_table, 'germanFW', "germanFemWork(!germanFem!,!OCC!)", "PYTHON3", germanFemWorkCode)
print("calculated german female workers")

#german & male & working
arcpy.AddField_management(in_table, 'germanMW', "SHORT")
print("added german male workers")
arcpy.CalculateField_management(in_table, 'germanMW', "germanMaleWork(!germanMale!,!OCC!)", "PYTHON3", germanMaleWorkCode)
print("calculated german male workers")

###########################Add and calculate fields for occupations############

#store clerks
arcpy.AddField_management(in_table, 'clerk', "SHORT")
print("added clerks")
arcpy.CalculateField_management(in_table, 'clerk', "storeClerk(!OCC!)", "PYTHON3", clerkCode)
print("calculated clerks")

arcpy.AddField_management(in_table, 'tailor', "SHORT")
print("added tailor")
arcpy.CalculateField_management(in_table, 'tailor', "tailor(!OCC!)", "PYTHON3", tailorCode)
print("calculated tailors")

arcpy.AddField_management(in_table, 'cigarMaker', "SHORT")
print("added cigar makers")
arcpy.CalculateField_management(in_table, 'cigarMaker', "cigarMaker(!OCC!)", "PYTHON3", cigarMakerCode)
print("calculated cigar makers")















        

