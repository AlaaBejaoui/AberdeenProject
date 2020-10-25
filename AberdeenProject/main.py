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
    This function defines the complete workflow, from dataframe generation to features extraction up to
    rules extraction
    """

    # Creating the dataframe from csv files
    data = DataframeCreator()
    print("Converting the pkl files into csv files ...")
    data.convertPklToCsv()
    print("Creating the dataframe from csv files ...")
    data.createDataframe()
    print("Filtering the dataframe based on the threshold ...")
    data.threshholdFiltering()

    # Loading the dataframe from the previously saved pickle file
    pickleDir = loadConfigFile().get("dirConfig").get("pklDir")
    pickleFile = loadConfigFile().get("fileConfig").get("pickledData_afterThFiltering")
    filePath = os.path.join(pickleDir, pickleFile)
    print('Loading the dataframe from the pickle file ...')
    data = pickle.load(open(filePath, 'rb'))

    # Initializing the full pipeline
    print('Initializing the pipeline ...')
    fullPipeline = FullPipeline()
    fullPipeline.initialize(data)

    # Building the missing values and the preprocessing pipelines
    missingValuesPipeline = MissingValuesPipeline()
    preprocessingPipeline = PreprocessingPipeline()
    print('Building the missing values pipeline ...')
    missingValuesPipeline.buildPipeline()
    print('Building the preprocessing pipeline ...')
    preprocessingPipeline.buildPipeline()

    # Adding the missing values and the preprocessing pipelines to the full pipeline
    print('Adding the missing values pipeline to the full pipelines ...')
    fullPipeline.addPipeline(missingValuesPipeline)
    print('Adding the preprocessing pipeline to the full pipelines ...')
    fullPipeline.addPipeline(preprocessingPipeline)

    # Fitting the dataframe to the full pipeline
    print('Fitting the dataframe to the full pipeline ...')
    data = fullPipeline.fit_transform(data)

    # Fitting the model
    model = Model(data, "decisionTree")
    print('Extracting the most important features ...')
    model.keepBestFeatures()
    print('Fitting the model ...')
    model.fit()
    print('Building the rules ...')
    model.buildRules("decisionTree.dot")


if __name__ == "__main__":
    main()
