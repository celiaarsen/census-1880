# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 09:43:17 2019

Walk through all people that are geocoded, and divide into shape files for each city

Steps:
    -make dictionary called 'citycodes' from csv with city codes and city names
    -make a dictionary 'outfile_dict' of city codes and output file names
    -Walk thru each line of John Logan data and look at city code
    -check and see if the city code already has a tuple in outfile_dict
        -If it does, write the line to the file in the tuple
        -If it does not,
            -Create a new tuple in the outfile_dict where the key is the city code 
            and the value is the value of the code in the citycodes dictionary
            -Write the line to that file

@author: Celia Arsen
"""

import csv

