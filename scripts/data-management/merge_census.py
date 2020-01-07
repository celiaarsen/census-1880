# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 19:50:17 2019

@author: Celia Arsen

Script for merging all 4 NYC-Manhattan Census files together and 
tabulating the number of men and women in each unique occupation

"""

import pandas as pd

path = "C:/Users/Celia/OneDrive - barnard.edu/Documents/Senior Thesis/CensusData/"
out_path = "C:/Users/Celia/OneDrive - barnard.edu/Documents/Senior Thesis/"
a1 = "NYC-ManhattanCE1a.csv"
b1 = "NYC-ManhattanCE1b.csv"
a2 = "NYC-ManhattanCE2a.csv"
b2 = "NYC-ManhattanCE2b.csv"

#types = {'occlabelB': object, 'ipumsOcc': object}
a1_DF = pd.read_csv(path+a1)
b1_DF = pd.read_csv(path+b1)
a2_DF = pd.read_csv(path+a2)
b2_DF = pd.read_csv(path+b2)

#this first line will take a long time. That's okay. Be patient!
all_nyc = a1_DF.append(b2_DF, ignore_index=True)
all_nyc2 = all_nyc.append(a2_DF, ignore_index=True)
all_nyc3 = all_nyc2.append(b1_DF, ignore_index=True)

all_newyorkers = all_nyc3

occs = {}

#tabulate up the occupations
for index, row in all_newyorkers.iterrows():
    try:
        #If the person is a woman
        if (row['sexB']==2):
            #increase the women count for that occupation
            occs[row['occlabelB']]['women']+=1
        #If the person is a man
        elif (row['sexB']==1):
            #increase the man count for that occupation
            occs[row['occlabelB']]['men']+=1
    #If that occupation hasn't been seen yet
    except KeyError: 
        #add that occupation to the dictionary
        occs[row['occlabelB']] = {'women':0, 'men':0}
        if (row['sexB']==2):
            #increase the women count for that occupation
            occs[row['occlabelB']]['women']+=1
        elif (row['sexB']==1):
            #incrase the man count for that occupation
            occs[row['occlabelB']]['men']+=1

#make the dictionary into a pandas df
occs_df = pd.DataFrame(occs).transpose()
#make a column with total # of people in that occ
occs_df['total'] = occs_df['women']+occs_df['men']
#give index a name
occs_df.index.name = 'occlabelB'
#write that file to csv
occs_df.to_csv(out_path+"occ_tabulations.csv")

#create df that only has occupations that more than one person had
over1 = occs_df[occs_df['total'] > 1]
#write to file
occs_df.to_csv(out_path+"occ_tabs_over1total.csv")
#create df that only has occupations that had at least one woman
has_women = occs_df[occs_df['women'] > 0]
#write to file
has_women.to_csv(out_path+"occ_tabs_women.csv")
#create df of occupations that had at least one woman and more than 1 total
over1woman = over1[over1['women']>0]
#write to file
over1woman.to_csv(out_path+"occ_tabs_over1t_women.csv")


