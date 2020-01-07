# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 21:39:24 2019

I want to create a file that has all of the blocks in the nation, weighted for the 
number of people on that block

Input file:
    CompositeCityBlocks.csv
Rows are all city blocks for all 39 cities,
with the total population of each block, and the population density of each block

Output file:
    CompositeCityBLWeight.csv
Has the same data as the input file, but each row is repeated the for each person on the block
For example, a row from the input file that has a total population of 5 people on the block
will be repeated 5 times in the output file.

The reason is so that we can ge the "weighted" or "experienced density" on the block level.

@author: Celia
"""
import csv

in_file = "C:/Users/Celia/Documents/SSHA-Gergo/CompositeCityBlocks.csv"
out_file = "C:/Users/Celia/Documents/SSHA-Gergo/CompositeCityBLWeight.csv"

first=1

sanity_checker_old_city = ""

with open(in_file, newline='\n') as in_f:
    reader = csv.DictReader(in_f)       
    for row in reader:
        block_population = int(row['population'])
        sanity_checker_new_city = row['city']  
        if(sanity_checker_old_city!=sanity_checker_new_city):
            print(sanity_checker_new_city)
            sanity_checker_old_city = sanity_checker_new_city
            
        while(block_population>0):
            with open(out_file, 'a+', newline='') as o:
                data_to_keep = {'index':row['index'], 'city':row['city'], 'pop':row['population'], 'acres':row['Acres'], 'popDense':row['PopDense']}
                w = csv.DictWriter(o, data_to_keep.keys())
                if (first==1):
                    w.writeheader()
                    first+=1
                w.writerow(data_to_keep)
                block_population-=1