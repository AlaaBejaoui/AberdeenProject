import os
import sys
sys.path.append(os.getcwd())

import pickle
import pprint
import pandas as pd
import numpy as np
from scipy.stats import bernoulli
from core.modelFitting import Model
from sklearn import tree
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
missingValues_pipeline = MissingValuesPipeline()
missingValues_fullPipeline = missingValues_pipeline.buildFullPipeline()
data_after_pipeline = pd.DataFrame(missingValues_fullPipeline.fit_transform(data))
data_after_pipeline.columns = pipeline.recoverColumnsNames()

X = data_after_pipeline[["WIRELESS_USERS","LAPTOPS"]]
y = pd.Series(bernoulli.rvs(size=14956, p=0.5))

# testing the model with target classes as integer (0,1)
model_1 = Model(X, y, "decisionTree", max_depth=3)
model_1.fit()
model_1.buildRules("test_aberdeen.dot")
