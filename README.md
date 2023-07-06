# mm_tesi

This is the repository for the Undergraduate Thesis of Giulio Frey.

## Aim of the project

We want to analyze how connected are different public housing with essential services around the city of Milan. 

## Contents

### code 

This folder contains all the code that is used in the project. The main task are the creation of the distance matrix using OSRM and subsequent analysis. 

* [analysis.ipynb](code/analysis.ipynb): performs the analysis
* [data_cleaning.ipynb](code/data_cleaning.ipynb): creates the datasets for essential services around the city. 
* [calculator.py](code/calculator.py): constructs the distance matrix using OSRM 
* [calculator_fixer.py](code/calculator_fixer.py): constructs the distance matrix using OSRM but only of one specific dataset. It was necessary as we faced geoencoding issues with one dataset.
* [merger.ipynb](code/merger.ipynb): merges the fixed dataset with all the others.
* [mm_geofactor.ipynb](code/mm_geofactor.ipynb): creates the social housing dataset. Converts the pdf provided by MM in a .csv file and the geoencodes the addresses 
* [tt_matrix.ipynb](code/tt_matrix.ipynb): experiments in calculating the time distance matrix between social housing and essential services using OSRM
* [visual.ipynb](code/visual.ipynb): creates visual to support the analysis

### outputs

This folder contains all the datasets created for the project

 * [calc_dataset.csv ](calc_dataset.csv )        
 * [calc_fixed_df.csv](calc_fixed_df.csv)  
 * [fixed_dataset.csv](fixed_dataset.csv)  
 * [mm_dataset.csv](mm_dataset.csv)  
 * [services_df.csv](services_df.csv)
 * [calc_dataset_backup.csv](calc_dataset_backup.csv)  
 * [distr_df.csv](distr_df.csv)       
 * [index_df.csv](index_df.csv)      
 * [row_file](row_file)


## Data sources

We use datasets provided by the portal [Open Data](https://dati.comune.milano.it/) of the Milan municipality in order to track essential services. 

A record of Social Housing in the city of Milan provides physical addresses. It can be found [here](https://casa.mmspa.eu/wps/portal/pon/case/home/patrimonio/alloggi/!ut/p/z1/04_Sj9CPykssy0xPLMnMz0vMAfIjo8zifQ0sjdwtTIx83f0NzQ0c_SzcDEKCfIz8_c30w1EVWHiYGRkEeod5-AUEBxkYOhvrRxGj3wAHcDQgTj8eBVH4jQ_Xj8JnhYW3OboCC3N3oM6w4GBD08BAAzc3YwwFmGFAyBUFuaGhEQaZnumOiooA8-SPZw!!/dz/d5/L2dBISEvZ0FBIS9nQSEh/)

