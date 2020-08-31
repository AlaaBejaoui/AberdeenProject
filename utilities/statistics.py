import os
import sys
sys.path.append(os.getcwd())

import pickle
from utilities.loadPickledData import loadPickledData

class Statistics:
    def __init__(self, filepath):
        self.filepath = filepath
        self.dataframe = loadPickledData(self.filepath)
    
    def getShape(self):
        return self.dataframe.shape

    def getKeptColumns(self):
        return list(self.dataframe.columns)

    def getNumKeptColumns(self):
        return len(list(self.dataframe.columns))

    def getUniqueValues(self):
        uniqueValue_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                uniqueValue_dict[column] = self.dataframe[column].unique()
            except:
                print(f" problem by the column: {column}")
        return uniqueValue_dict

    def getColumnsStatistics(self):
        statistics_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                statistics_dict[column] = self.dataframe[column].value_counts(normalize=True,dropna=False)*100
            except:
                print(f" problem by the column: {column}")
        return statistics_dict
