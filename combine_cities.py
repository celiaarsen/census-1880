"""
Combine all files in one directory into one file
@author: Celia
"""
import os
import pandas as pd

os.chdir("C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU")
directory = "C:/Users/Celia/Desktop/EthnicityUrbanHGIS/PopulationDensity/AllCitiesAU"

def combine_cities():
    df = pd.DataFrame()
    for city in os.listdir(directory):
        new_city = pd.read_csv(city)
        new_city['city'] = city.split("AU")[0]
        df = df.append(new_city, ignore_index = True, sort=False)
    return df


AllCitiesAU = combine_cities()





