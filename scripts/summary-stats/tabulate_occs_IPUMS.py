# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:19:35 2019

Takes full count of IPUMS data from one city and calculates the number of women
and men in each occupation, the percent of workers in that occupation who are women,
and if the occupation is a "female" occupation, which means that women are 
overrepresented in that occupation. 

@author: Celia
"""
import csv
import pandas as pd

in_file = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/ManhattanIPUMS_fullCount.csv"
out_path = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/Thesis2020/"

occs = {}

with open(in_file, newline='\n') as f:
    reader = csv.DictReader(f)
    #print(row)
    for row in reader:
        try:
            #print('trying')
            #If the person is a woman
            if (int(row['SEX'])==2):
                #increase the women count for that occupation
                occs[row['OCC']]['women']+=1
            #If the person is a man
            elif (int(row['SEX'])==1):
                #increase the man count for that occupation
                occs[row['OCC']]['men']+=1
        #If that occupation hasn't been seen yet
        except:
            #add that occupation to the dictionary
            occs[row['OCC']] = {'women':0, 'men':0}
            if (int(row['SEX'])==2):
                #increase the women count for that occupation
                occs[row['OCC']]['women']+=1
            elif (int(row['SEX'])==1):
                #incrase the man count for that occupation
                occs[row['OCC']]['men']+=1
                
#make the dictionary into a pandas df
occs_df = pd.DataFrame(occs).transpose()
#make a column with total # of people in that occ
occs_df['total'] = occs_df['women']+occs_df['men']
#Make a column that is the percent women in that occupation
occs_df['percentW'] = occs_df['women']/occs_df['total']
#Make a variable that is the percent of the workforce that is female
ppl_in_workforce = 465960
women_in_workforce = 123698
percent_female_workforce = women_in_workforce/ppl_in_workforce
#Make a variable that indicates whether the profession is a female or male occuation
occs_df['femOcc'] = [1 if x >= percent_female_workforce else 0 for x in occs_df['percentW']]
#give index a name
occs_df.index.name = 'Occupation'
#write that file to csv
occs_df.to_csv(out_path+"ManhattanIPUMS_occ_tabs.csv")