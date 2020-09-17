import os
import sys
sys.path.append(os.getcwd())

import pickle
import pprint
import pandas as pd
import numpy as np

from core.dataframeCreator import DataframeCreator
from core.TransformationWrapper import *
from core.dataPipelines import EntirePipeline, MissingValuesPipeline, PreprocessingPipeline
from utilities.statistics import Statistics

# file = "/home/linux/Desktop/AberdeenProject/pickledData/dataframe_all.pkl"
# file = "C:\\Users\\alaab\\OneDrive\\Desktop\\AberdeenProject\\pickledData\\dataframe_all.pkl"
# file = "/home/linux/Desktop/AberdeenProject/pickledData/dataframe_kept.pkl"
file = "C:\\Users\\alaab\\OneDrive\\Desktop\\AberdeenProject\\pickledData\\dataframe_kept.pkl"

# loading the data from the pickle file
data = pickle.load(open(file,'rb'))

## initializing the full pipeline with the data
pipeline = EntirePipeline()
pipeline.initialize(data)

## missing values pipeline
# apply missing value pipeline 
missingValues_pipeline = MissingValuesPipeline()
missingValues_fullPipeline = missingValues_pipeline.buildFullPipeline()
# checking the output missing values pipeline applied to the data
print("data before passing through the missing values pipeline")
print(data)
data_after_pipeline_1 = pd.DataFrame(missingValues_fullPipeline.fit_transform(data))
print("data after passing through the missing values pipeline")
print(data_after_pipeline_1)
data_after_pipeline_1.columns = pipeline.recoverColumnsNames()
print("data after recovering the column names")
print(data_after_pipeline_1)

