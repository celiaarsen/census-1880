# census-1880

This repo contains scripts for manipulating and analyzing the 1880 U.S. Census for residents in 39 cities with geocoded addresses.

Data can be downloaded from https://s4.ad.brown.edu/Projects/UTP2/39cities.htm or https://usa.ipums.org/usa/data.shtml

```
+-- scripts/
    +-- data-management/
        +-- cleanXY.py                <-- create copy of data with only valid XY coordinates
        +-- combine_cities.py         <-- combine family units from all cities into 1 file
        +-- dbf_to_csv.py             <-- make copies of all DBF files in directory as CSVs
        +-- fix_projections.py        <-- project shapefiles into appropriate StatePlane proj
        +-- fullCount_to_cityCsvs.py  <-- divide single file into files for all cities
        +-- merge_census.py           <-- merging all 4 NYC-Manhattan Census files together and tabulate the number of men and women in each unique occupation
    
    +-- density_curves/
        +-- density_curves_all_cities.py    <-- percent of population living at each density level
        +-- weighted_blocks.py
        +-- weighted_ethnicity_blocks.py

```
