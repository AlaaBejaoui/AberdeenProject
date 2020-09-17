import os
import sys
sys.path.append(os.getcwd())

from core.dataframeCreator import DataframeCreator 

import pickle
import yaml
import pandas as pd
import numpy as np


with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

pklDir = cfg.get("dirConfig").get("pklDir")
dataFile = cfg.get("fileConfig").get("dataFile")


with open(os.path.join(pklDir,dataFile), 'rb') as f:
    data = pickle.load(f)

# Dimension test
dataframeCreator = DataframeCreator()
numRows = len(dataframeCreator.getAllSiteID())
numColumns = 0
for elem in dataframeCreator.getAllFeatures():
    numColumns += len(elem[1])

assert data.shape[0] == numRows and data.shape[1] == numColumns, "Dimension test failed!"

# 
print(data[data["SITEID"] == 208000878])