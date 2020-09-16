import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

import pickle
import pprint
import pandas as pd
import numpy as np
from core.dataframeCreator import DataframeCreator
from core.modelFitting import Model
from core.dataPipelines import FullPipeline, MissingValuesPipeline, PreprocessingPipeline
from utilities.statistics import Statistics
from utilities.loadConfigFile import loadConfigFile

def main():
    """
    This function defines the complete workflow, from dataframe generation to rules extraction from decision tree
    """

    ## Creating the dataframe from csv files
    data = DataframeCreator()
    data.createDataframe()
    data.threshholdFiltering()

    ## Loading the dataframe from the peviously saved pickle file
    pickleDir = loadConfigFile().get("dirConfig").get("pklDir")
    pickleFile = loadConfigFile().get("fileConfig").get("pickledData_afterThFiltering")
    filePath = os.path.join(pickleDir, pickleFile)
    data = pickle.load(open(filePath,'rb'))

    ## Initializing the full pipeline
    fullPipeline = FullPipeline()
    fullPipeline.initialize(data)

    ## Building the missing values and the preprocessing pipelines
    missingValuesPipeline = MissingValuesPipeline()
    preprocessingPipeline = PreprocessingPipeline()
    missingValuesPipeline.buildPipeline()
    preprocessingPipeline.buildPipeline()

    ## Adding the missing values and the preprocessing pipelines to the full pipeline
    fullPipeline.addPipeline(missingValuesPipeline)
    fullPipeline.addPipeline(preprocessingPipeline)

    ## Fitting the dataframe to the full pipeline
    data = fullPipeline.fit_transform(data)

    ## Fitting the model
    model = Model(data, "decisionTree", max_depth=2)
    model.fit()
    model.buildRules("aberdeenData.dot")

if __name__ == "__main__":
    main()