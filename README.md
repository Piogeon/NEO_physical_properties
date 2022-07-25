# NEW EARN
This program is developed by Francesco Pio

Program to update NEOs' physical properties for ESA/NEOCC database.

Libraries needed:
    1) Pandas 1.1.3
    2) Tabula 2.3.0
    3) Numpy 1.19.2
    4) Regex 2020.10.15
    5) ElementTree 1.3.0

In the following text you can find the explanation of each file inside the NEW EARN 
project about the input it takes, the data management and the output it produces.

The NEW EARN project is structured in 2 script per physical properties:
    1) The first script is the file that regroups all the sources that we are using for a
    particular property, including the reference file, and after calling the second script for
    each source it merges everything into a single dataset,
    2) The second script is the data manipulation code so that we can actually change the formatting
    style and produce the final output following the new ICD guidelines.

The INPUTS of the scripts are datasets given in the following extensions:
    1) csv
    2) html
    3) fixed column tables
    4) pdf

The OUTPUT of the script is a dataset in the fixed column table format compatible with
the new ICD produced.

The directory "function" is filled with minor functions created by me both to double-check
the values of the data, validate them and also to write the final output of each physical properties.

The most important functions here are:
    1) are_there_NEO.py
    2) write_fdf.py
    
The first one is used to double check every sources if there are non-NEO asteroids
and delete them. It takes as INPUT the already processed dataframe and returns a list
of the names of the non-NEOs and a list of the indexed of the non-NEOs

The second one is used to write the final dataframe into a fixed column table file in
txt extension given a specified column specs that follows the ICD previously written.
It takes as INPUTs: the file path to save the file, the dataframe to write and the colum specs.
It returns a txt file in fixed column format saved in the path specified in the input.
