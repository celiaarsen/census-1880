# census-1880

This repo contains scripts for manipulating and analyzing the 1880 U.S. Census for residents in 39 cities with geocoded addresses.

Data can be downloaded from https://s4.ad.brown.edu/Projects/UTP2/39cities.htm or https://usa.ipums.org/usa/data.shtml

These data and scripts are being used for two ongoing research projects:
1. Celia Arsen's senior thesis in economic history http://ssha2019.ssha.org/abstracts/100959
2. Co-authored work with Gergely Baics (Barnard) and Leah Meisterlin (Columbia) http://ssha2019.ssha.org/abstracts/100862

```
+-- scripts/

    +-- data-management/
        +-- cleanXY.py                      <-- create copy of data with only valid XY coordinates
        +-- combine_cities.py               <-- combine family units from all cities into 1 file
        +-- dbf_to_csv.py                   <-- make copies of all DBF files in directory as CSVs
        +-- fix_projections.py              <-- project shapefiles into appropriate StatePlane proj
        +-- fullCount_to_cityCsvs.py        <-- divide single file into files for all cities
        +-- merge_census.py                 <-- merging all 4 NYC-Manhattan Census files together and tabulate the number of men and women in each unique occupation
    
    +-- density_curves/
        +-- density_curves_all_cities.py    <-- percent of population living at each density level
        +-- weighted_blocks.py              <-- creates file w/ all U.S. city blocks, weighted for # of people on the block
        +-- weighted_ethnicity_blocks.py    <-- weights city blocks by # of people of each ethnicity
    
    +-- spatial_joins/
        +-- fem_male_occupations.py         <-- determine if residents are in male/female dominated occupations
        +-- join_ethnicity.py               <-- join and sum ethnic categories up to block level
        +-- join_irish_german.py            <-- calculate various dummy variables in NYC shapefile
        +-- occupation-joins.py             <-- join count of specific occupations to block level
        +-- spatial_join_irish_german.py    <-- join NYC residents up to block level with calculated variables 
        +-- XY_table_to_shp.py              <-- create point shapefiles from xy tables
        
    +-- summary_stats/
        +-- avg_densities.py                <-- create CSV w/ average density of blocks by city
        +-- avg_exp_ethnicity.py            <-- create CSV w/ average density of residents by city
        +-- BlockArea_SumStats.py           <-- create CSV w/ mean, median, sd, min, and max block size by city
        +-- BuildingPopulation_SumStats.py  <-- create CSV w/ mean, median, sd, min, and max for building population by city
        +-- ethnicity_sums.py               <-- create CSV w/ total ethnicity population for each city 
        +-- LotSize_SumStats.py             <-- create CSV w/ mean, median, sd, min, and max for lot size by city
        +-- median_exp_density.py           <-- calcuate the median "experienced density" for each city
        +-- tabulate_occ_IPUMS.py           <-- calculates # of women and men in each occupation in a city, % female workers in each occ, and which occs have overrepresentation of women

```