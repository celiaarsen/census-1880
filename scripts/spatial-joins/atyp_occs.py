# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 10:11:58 2020

Count number of German working women in atypical occs
and number of Irish working women in atypical occs on the block level

@author: Celia Arsen
"""
import pandas as pd
import arcpy
print('arcpy imported')

occupations_df = pd.read_csv("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/ManhattanIPUMS_occ_tabs.csv")
occupations_df = occupations_df.set_index('Occupation')


arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/SSHA-Arsen/SSHA-Arsen.gdb"
in_table = "NYCManhattan_IPUMS_proj"



fem_occ_code = """
def fem_occ(resident_occ):
    if (int(occupations_df.loc[resident_occ,'femOcc'])==1):
        return 1
    else:
        return 0 """
        
atyp_occ_code = """
def atyp_occ(female, occ):
    if (female==1 and (int(occupations_df.loc[occ,'femOcc'])==1)):
        return 0
    elif(female==0 and (int(occupations_df.loc[occ,'femOcc'])==0)):
        return 0
    else:
        return 1
"""

atyp_german_occ = """
def atyp_germanFW(germanFW, atypOcc):
    if (germanFW==1 and atypOcc==1):
        return 1
    else:
        return 0
"""        

atyp_irish_occ = """
def atyp_irishFW(irishFW, atypOcc):
    if (irishFW==1 and atypOcc==1):
        return 1
    else:
        return 0
"""   

#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
#arcpy.AddField_management(in_table, 'femOcc', "SHORT")

#arcpy.AddField_management(in_table, 'atypOcc', "SHORT")

#arcpy.AddField_management(in_table, 'atyp_GFW', "SHORT")

#arcpy.AddField_management(in_table, 'atyp_IFW', "SHORT")

print("fields added")

#CalculateField(in_table, field, expression, {expression_type}, {code_block})
#calculate a dummy variable for the attribute femOcc
#arcpy.CalculateField_management(in_table, 'femOcc', "fem_occ(!OCC!)", "PYTHON3", fem_occ_code)

arcpy.CalculateField_management(in_table, 'atypOcc', "atyp_occ(!Female!, !OCC!)", "PYTHON3", atyp_occ_code)

arcpy.CalculateField_management(in_table, 
                                'atyp_GFW', "atyp_germanFW(!germanFW!, !atypOcc!)", 
                                "PYTHON3", atyp_german_occ)

arcpy.CalculateField_management(in_table, 
                                'atyp_IFW', "atyp_irishFW(!irishFW!, !atypOcc!)", 
                                "PYTHON3", atyp_irish_occ)

print("Calculations complete")
