# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 23:53:23 2019

Calculate a new column in IPUMS shapefile that says whether a woman is in a 
"female" or "male" occupation. Use the script tabulate_occs_IPUMS.py to determine
which occupations have an overrepresentation of women or men, for the city of interest.

@author: Celia
"""

import pandas as pd
import arcpy
print('arcpy imported')

occupations_df = pd.read_csv("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/ManhattanIPUMS_occ_tabs.csv")
occupations_df = occupations_df.set_index('Occupation')

arcpy.env.workspace = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/SSHA-Arsen/SSHA-Arsen.gdb"
in_table = "ManhattanWomen"



codeblock = """
def occ_dummy(resident_occ):
    if (int(occupations_df.loc[resident_occ,'femOcc'])==1):
        return 1
    else:
        return 0 """

#AddField(in_table, field_name, field_type, {field_precision}, {field_scale})
#arcpy.AddField_management(in_table, 'femOcc', "SHORT")

#CalculateField(in_table, field, expression, {expression_type}, {code_block})
#calculate a dummy variable for the attribute occs
arcpy.CalculateField_management(in_table, 'femOcc', "occ_dummy(!OCC!)", "PYTHON3", codeblock)