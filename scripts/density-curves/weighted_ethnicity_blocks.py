# -*- coding: utf-8 -*-
"""
Created on Wed Nov 6 2019

Input file:
    NYCManhattanET_copy.csv and then PhiladelphiaET_copy.csv, NewOrleansET_copy.csv, 
    ChicagoET_copy.csv, SanFranciscoET_copy.csv
Rows are all the blocks in the city,
with the total population of each block, the population of each ethnicity on the block,
and the population density of each block

Output file:
    NYCManhattanBLWeight.csv and then the respective files for the other four input cities

Output file has the city blocks, but each block row is repeated for each person in each
group of interest livin on the block.
For example, if an input row has:
    popDense    totPop    nBw    fBn   bBn    irishBn    germanBn    frenchBn
    34.1234      10        4      6     1        2          4           0
    
The output for that row will be:
    popDense    totPop    nBw    fBn   bBn    irishBn    germanBn    frenchBn    indivET    
    34.1234      10        4      6     1        2          4           0          nBw
    34.1234      10        4      6     1        2          4           0          nBw
    34.1234      10        4      6     1        2          4           0          nBw
    34.1234      10        4      6     1        2          4           0          nBw
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          fBn
    34.1234      10        4      6     1        2          4           0          bBn
    34.1234      10        4      6     1        2          4           0        irishBn
    34.1234      10        4      6     1        2          4           0        irishBn
    34.1234      10        4      6     1        2          4           0        germanBn
    34.1234      10        4      6     1        2          4           0        germanBn
    34.1234      10        4      6     1        2          4           0        germanBn
    34.1234      10        4      6     1        2          4           0        germanBn
    
  
ethnic groups: 
    Native-born white, foreign-born, second-gen, black, irish, german, british, french (for NOLA), chines (for SF)

We do this to get the "weighted" or "experienced density" on the block level
for each ethnic group in the city.
However, this algorithm does not use space efficiently.
Finding another way to do this would be great, but this is what I have for now. 

@author: Celia Arsen
"""
import csv

in_file = "C:/Users/Celia/Documents/SSHA-Gergo/NYCManhattanET_copy.csv"
out_file = "C:/Users/Celia/Documents/SSHA-Gergo/NYCManhattanBLWeight.csv"

ethnicities = ["blkBn", "britBn","germanBn","irishBn","nwnpBn","fbBn","secGen"]

first=1
sanity_checker = 0

with open(in_file, newline='\n') as in_f:
    reader = csv.DictReader(in_f)       
    for row in reader:
        for ethnicity in ethnicities:
            ethnic_population = int(row[ethnicity])

            while(ethnic_population>0):
                with open(out_file, 'a+', newline='') as o:
                    data_to_keep = {'TARGET_FID':row['TARGET_FID'], 'ethnicPop':row[ethnicity],                                     
                                    'acres':row['Acres'], 'popDense':row['PopDense'], 'indivET':ethnicity}
                    w = csv.DictWriter(o, data_to_keep.keys())
                    if (first==1):
                        w.writeheader()
                        first+=1
                    w.writerow(data_to_keep)
                    ethnic_population-=1
        
        sanity_checker += 1
        if(sanity_checker%100==0):
            print('processed ', sanity_checker, ' rows')
            
            
            