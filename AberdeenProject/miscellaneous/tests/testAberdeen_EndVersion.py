import os
import sys
sys.path.append(os.getcwd())

import pickle
import pprint
import pandas as pd
import numpy as np

from core.dataframeCreator import DataframeCreator
from core.TransformationWrapper import *
from core.dataPipelines import FullPipeline, MissingValuesPipeline, PreprocessingPipeline
from utilities.statistics import Statistics
from sklearn.preprocessing import LabelEncoder
from scipy.stats import bernoulli
from core.modelFitting import Model


# file = "/home/linux/Desktop/AberdeenProject/pickledData/dataframe_all.pkl"
# file = "C:\\Users\\alaab\\OneDrive\\Desktop\\AberdeenProject\\pickledData\\dataframe_all.pkl"
# file = "/home/linux/Desktop/AberdeenProject/pickledData/dataframe_kept.pkl"
file = "C:\\Users\\alaab\\OneDrive\\Desktop\\AberdeenProject\\pickledData\\dataframe_kept.pkl"

# loading the data from the pickle file
data = pickle.load(open(file,'rb'))

fullPipeline = FullPipeline()
fullPipeline.initialize(data)

missingValuesPipeline = MissingValuesPipeline()
preprocessingPipeline = PreprocessingPipeline()

missingValuesPipeline.buildPipeline()
preprocessingPipeline.buildPipeline()

fullPipeline.addPipeline(missingValuesPipeline)
fullPipeline.addPipeline(preprocessingPipeline)

data = fullPipeline.fit_transform(data)

# testing the model with target classes as integer (0,1)
model = Model(data, "decisionTree", max_depth=2)
model.fit()
model.buildRules("aberdeen.dot")
