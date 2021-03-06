Code format
===========

Overview
-----------------

The implementation in this project adheres to a standard template. You can find below the folder structure of the Aberdeen
project

|   **AberdeenProject**
|   ├── **AberdeenProject**
|   │   ├── **core**
|   │   ├── **data**
|   │   ├── **pickeledData**
|   │   ├── **results**
|   │   ├── **utilities**
|   │   ├── **miscellaneous**
|   │   ├── *__init__.py*
|   │   ├── *config.yml*
|   │   └── *main.py*
|   ├── **docs**
|   ├── *environment.yml*
|   ├── *README.md*
|   ├── *readthedocs.yml*
|   └── *requirements.txt*
|

Folder structure
-----------------

In the folder structure above:

    * **AberdeenProject** is the actual Python package directory where all the Python source files reside

        * **core** is the directory which contains all the classes and functions that are called in the main file
        * **data** is the folder which contains all the csv files used to create the dataframe
        * **pickledData** is the directory which contains the pickeled dataframe that is created in order to avoid the time consuming process of reading and joining the csv files every time the code is executed
        * **results** is the folder which contains the text files where the automatically extracted features are listed as well as the output image generated from the dot file where the decision tree rules are graphically respresented
        * **utilities** is a directory which contains various utilities needed to run the code
        * **miscellenous** is a folder which contains some tests used to check the implementation in the early project phase
        * *__init__.py* is a file which is required by Python in oder to treat directories containing the file as packages
        * *config.yml* is the configuration file which contains all the variables that must be specified by the user in order to run the code
        * *main.py* is the main file which contains the core logic of the code

    * **docs** is the directory where the Sphinx documentation resides
    * *environment.yml* is the file which contains the conda environment that includes all the libraries, packages and dependencies needed to run the code
    * *README.md* is a text file that introduces and explains the project
    * *readthedocs.yml* is the configuration file required by Read the Docs which contains all the variables that must be specified by the user in order to build the documentation
    * *requirements.txt* is a file required by Read the Docs where the user needs to specify the dependencies required to build the documentation




 