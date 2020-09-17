from utilities.statistics import Statistics
from utilities.loadPickledData import loadPickledData
from utilities.loadConfigFile import loadConfigFile
from itertools import chain
from itertools import count
from multiprocessing import Pool
import pandas as pd
import multiprocessing
import yaml

import os

class DataframeCreator:
    """
    This class contains all methods and attributes needed in order to create a single Pandas dataframe from features and labels
    chosen by the user.
    """

    def __init__(self):
        """
        The constructor of this class loads the needed variables from the configuration yaml file
        and creates an empty Pandas dataframe.
        """

        self.config = loadConfigFile()
        self.dataframe = pd.DataFrame()

    def readCsvFile(self, file):
        """
        A wrapper function to wrap the read_csv function from Pandas
        :param file: Path to the csv-file to be read
        :type file: String
        :return: The csv-file is returned as two-dimensional data structure with labeled axes.
        :rtype: Pandas dataframe
        """

        dataDir = self.config.get("dirConfig").get("dataDir")
        return pd.read_csv(os.path.join(dataDir, file), sep='\t')

    def createDataframe(self):
        """
        Every csv-file in the directory "data/" is read and transformed into a Pandas dataframe. After that, all the dataframes
        are concatenated vertically based on the variable "joinBasedOn" given by the user in the configuration yaml file.
        To avoid repeating this process everytime the code is run, the dataframe is pickeled and stored as a pickle file
        in the directory "pickeledData/".
        This function is parallelized over all available CPUs using the multiprocessing library.
        """

        csvFiles = [f for f in os.listdir(self.config.get("dirConfig").get("dataDir")) if not f.startswith('.')]

        with Pool(len(csvFiles)) as p:
            collectedData = p.map(self.readCsvFile, csvFiles)

        if len(collectedData) == 1:
            self.dataframe = collectedData
        else:
            self.dataframe = collectedData[0]
            try:
                joinBasedOn = self.config.get(
                    "dataframeConfig").get("joinBasedOn")
            except:
                for index in range(1, len(collectedData)):
                    self.dataframe = pd.concat(
                        [self.dataframe, collectedData[index]], axis=1)
            else:
                for index in range(1, len(collectedData)):
                    self.dataframe = self.dataframe.merge(
                        collectedData[index], how='outer', on=[joinBasedOn])

        # Remove duplicated columns
        self.dataframe = self.dataframe.loc[:,
                                            ~self.dataframe.columns.duplicated()]

        self.pickleDataframe(self.dataframe, self.config.get(
            "fileConfig").get("pickledData_all"))

    def pickleDataframe(self, dataframe, pickledDataFile):
        """
        This function saves a given Pandas dataframe as a pickle file
        :param dataframe: Pandas dataframe to be saved
        :type dataframe: Pandas dataframe
        :param pickledDataFile: Path to the desired location of the pickle file
        :type pickledDataFile: String
        """

        isempty = dataframe.empty
        assert not(
            isempty), "Dataframe is empty! You must call createDataframe()!"

        pklDir = self.config.get("dirConfig").get("pklDir")
        dataframe.to_pickle(os.path.join(
            pklDir, pickledDataFile))

    def threshholdFiltering(self):
        """
        This function filters the data based on the value of "threshold" given by the user in the configuration yaml file.
        The entire column will be ignored if the number of missing values exceeds the threshhold.
        The dataframe after applying the threshhold filtering will be pickled and stored in the directory "pickeledData/".
        """

        # Check if the pickle file exists
        pklDir = self.config.get("dirConfig").get("pklDir")
        pickledDataFile = self.config.get("fileConfig").get("pickledData_all")
        exist = os.path.exists(os.path.join(pklDir, pickledDataFile))
        assert exist, f"No dataframe found in {os.path.join(pklDir, pickledDataFile)}!"

        dataframe = loadPickledData(os.path.join(pklDir, pickledDataFile))

        columnsToKeep_list = []
        statistics = Statistics(os.path.join(
            pklDir, pickledDataFile)).getColumnsStatistics()
        threshold = float(self.config.get("missingConfig").get("threshold"))
        for column in chain(loadConfigFile().get("features").items(), loadConfigFile().get("labels").items()):
            column = column[0]
            # Check threshhold
            try:
                missingProp = float(
                    statistics[column].loc[statistics[column].index.isnull()])
            except:
                # No missing values found
                columnsToKeep_list.append(column)
            else:
                # Missing values found
                # If the missing values ratio is smaller than the defined threshhold, the column
                # will be kept, and dropped otherweise
                if missingProp < threshold:
                    columnsToKeep_list.append(column)

        self.pickleDataframe(dataframe[columnsToKeep_list], self.config.get(
            "fileConfig").get("pickledData_afterThFiltering"))