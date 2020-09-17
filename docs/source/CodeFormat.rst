Code Format 
===========

The implementation in this project adheres to a standard template. It is split into: 

    * 3 files:
        
        * **main.py**
            which contains the core logic of the algorithm

        * **requirements.yml**
            which contains the conda environment that includes all the libraries, packages and dependencies needed to run the code
        
        * **config.yml**
            which contains all the variables that must be specified by the user

    * 6 directories:
        
        * **core/**
            which contains all the classes and functions that are called in the main file

        * **utilities/**
            which contains various utilities needed to run the code
        
        * **data/**
            which contains all the csv files used to create the dataframe
        
        * **pickledData/**
            which contains the pickeled dataframe that is created in order to avoid the time consuming process of reading and joining the csv files every time the code is executed
        
        * **results/**
            which contains the output image and dot file where the generated rules are graphically respresented

        * **miscellenous/**
            which contains some tests used to check the implementation in the early project phase
        
        


 