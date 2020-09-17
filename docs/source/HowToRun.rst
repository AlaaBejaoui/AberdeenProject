How to run? 
============

Configuration file
^^^^^^^^^^^^^^^^^^^^

Files and directories 
++++++++++++++++++++++

First of all, we start by defining the working directory as well as all the other needed variables to run the code. 
The configuration file is a yaml file that is located in **AberdeenProject/** and can be found under the name **config.yml**. 

.. code-block:: RST

    dirConfig:
        workingDir: "C:\\Users\\alaab\\Desktop\\AberdeenProject"
        dataDir: "C:\\Users\\alaab\\Desktop\\AberdeenProject\\data"
        pklDir: "C:\\Users\\alaab\\Desktop\\AberdeenProject\\pickledData"
    
    fileConfig:
        pickledData_all: "dataframe_all.pkl"
        pickledData_afterThFiltering: "dataframe_kept.pkl"

    dataframeConfig:
        joinBasedOn: "SITEID"

    missingConfig:
        threshold: 70

The variables that should be defined in the configuration file are the following:

* **workingDir**
    which defines the path to the working directory
* **dataDir**
    which defines the path to the data directory where the csv-files are stored
* **pklDir** 
    which defines the path to the directory where the pickled dataframe will be stored
* **pickledData_all**
    which defines the name of the complete pickled dataframe 
* **pickledData_afterThFiltering**
    which defines the name of the pickled dataframe after the threshold filtering 
* **joinBasedOn**
    which defines the column name based on which the csv-files will concatenated in order to generate the full dataframe
* **threshold**
    which defines the percentage of missing values based on which the decision whether a column should be dropped will be made 

Features and labels
++++++++++++++++++++

The user should also define a single label that will be predicted using a set of features which also should be defined in the configuration file.
For each defined feature and label, the user should specify the imputation and the preprocessing strategies as well. The following
startegies are currently supported

* Imputation strategies: 

    * **"mean"**: The missing values will be replaced using the mean along each column. This strategy can only be used with numeric data
    * **"median"**: The missing values will be replaced using the median along each column. This strategy can only be used with numeric data
    * **"most_frequent"**: The missing values will be replaced using the most frequent value along each column. This strategy can be used with strings as well as numeric data
    * **"constant"**: The missing values will be replaced using a constant value along each column. This strategy can be used with strings as well as numeric data

* Preprocessing strategies: 

    * **"onehot"**: The features will be encoded using a one-hot encoding scheme, which creates a binary column for each category. This strategy can only be applied to categorical features 
    * **None**: No preprocessing strategy will be applied to the feature

.. code-block:: RST

    features:
        ENT_LAPTOP: 
            missing: "most_frequent"
            preprocessing: "onehot"
        ENT_SERVER: 
            missing: "most_frequent"
            preprocessing: "onehot"
        WIRELESS_USERS: 
            missing: "most_frequent" 
            preprocessing: None
        LAPTOPS: 
            missing: "most_frequent" 
            preprocessing: None
    labels:
        STORAGE_CAPACITY_EXPANSION_PLS:
            missing: "most_frequent" 
            preprocessing: None

Code workflow
^^^^^^^^^^^^^^^

All the steps described below can be found in the file **main.py** which represents the entry point to execute the code. 

The first step consists in creating a Pandas dataframe from the csv-files provided by the user in the **data/** directory. The columns where the percentage of misssing
values exceeds the user defined threshhold will then be dropped. Next the dataframe will be pickled and stored in the **pickledData/** directory.

>>> data = DataframeCreator()
>>> data.createDataframe()
>>> data.threshholdFiltering()

After that, the dataframe will be loaded from the previously saved pickle file

>>> pickleDir = loadConfigFile().get("dirConfig").get("pklDir")
>>> pickleFile = loadConfigFile().get("fileConfig").get("pickledData_kept")
>>> filePath = os.path.join(pickleDir, pickleFile)
>>> data = pickle.load(open(filePath,'rb'))

The next step consists in initializing the full pipeline. This step is important in order to first store the columns names and then recover them when needed. 

>>> fullPipeline = FullPipeline()
>>> fullPipeline.initialize(data)

Once the full pipeline is initialized, the missing values as well as preprocessing pipelines can be built

>>> missingValuesPipeline = MissingValuesPipeline()
>>> preprocessingPipeline = PreprocessingPipeline()
>>> missingValuesPipeline.buildPipeline()
>>> preprocessingPipeline.buildPipeline()

and added to the full pipeline.

>>> fullPipeline.addPipeline(missingValuesPipeline)
>>> fullPipeline.addPipeline(preprocessingPipeline)

The full pipeline is now ready and can be applied to the dataframe.

>>> data = fullPipeline.fit_transform(data)

The transformed dataframe can now be used to build the model. After fitting the model to the data, the rules are extracted and exported to an image which will be
stored in the **results/** directory.    

>>> model = Model(data, "decisionTree", max_depth=2)
>>> model.fit()
>>> model.buildRules("aberdeenData.dot")

Below is an example of the generated output image

.. image:: aberdeenData.png
   :width: 600
