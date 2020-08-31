import os
import sys
sys.path.append(os.getcwd())

from core.dataframeCreator import DataframeCreator 

import pickle
import yaml
import pandas as pd
import numpy as np

data = DataframeCreator()
data.createDataframe()
data.applyMissingValuesStrategy()