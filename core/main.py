import os
import sys
sys.path.append(os.getcwd())

import pickle
import pprint
import pandas as pd
import numpy as np

from core.dataframeCreator import DataframeCreator
from core.TransformationWrapper import *
from core.modelFitting import Model
from core.dataPipelines import FullPipeline, MissingValuesPipeline, PreprocessingPipeline
from utilities.statistics import Statistics
from utilities.loadConfigFile import loadConfigFile

## creating the dataframe from csv files
data = DataframeCreator()
data.createDataframe()
data.threshholdFiltering()


## loading the data to work with from the pickle file
pickleDir = loadConfigFile().get("dirConfig").get("pklDir")
pickleFile = loadConfigFile().get("fileConfig").get("pickledData_kept")
filePath = os.path.join(pickleDir, pickleFile)
data = pickle.load(open(filePath,'rb'))

## initializing the full pipeline
fullPipeline = FullPipeline()
fullPipeline.initialize(data)

## building the missing values and the preprocessing pipelines
missingValuesPipeline = MissingValuesPipeline()
preprocessingPipeline = PreprocessingPipeline()
missingValuesPipeline.buildPipeline()
preprocessingPipeline.buildPipeline()

## adding the missing values and the preprocessing pipelines to the full pipeline
fullPipeline.addPipeline(missingValuesPipeline)
fullPipeline.addPipeline(preprocessingPipeline)

## fitting the dataframe to the full pipeline
data = fullPipeline.fit_transform(data)

## fitting the model with the data
model = Model(data, "decisionTree", max_depth=2)
model.fit()
model.buildRules("aberdeenData.dot")












