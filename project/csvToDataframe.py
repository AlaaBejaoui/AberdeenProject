import pandas as pd
from itertools import count
import yaml
import os
import sys
print(sys.path.append(os.getcwd()))


class DataframeCreator:

    def __init__(self):

        self.__loadConfigFile()
        self.data = pd.DataFrame()

    def __loadConfigFile(self):
        """ttt
        """
        with open("utilities/config.yml", "r") as ymlfile:
            cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

        self.workingDir = cfg.get("dirConfig").get("workingDir")
        self.dataDir = cfg.get("dirConfig").get("dataDir")

        self.dataFile = cfg.get("fileConfig").get("dataFile")
        self.manualDecisionFile = cfg.get(
            "fileConfig").get("manualDecisionFile")

        self.threshold = cfg.get("simConfig").get("threshold")

    def __readCsvFile(self, file):
        """ttt

        :param file: [description]
        :type file: [type]
        :return: [description]
        :rtype: [type]
        """
        return pd.read_csv(os.path.join(self.dataDir, file), sep='\t')

    @property
    def allSiteID(self):
        """rrr

        :return: [description]
        :rtype: [type]
        """

        SiteID_set = set()
        for file in os.listdir(self.dataDir):
            df = self.__readCsvFile(file)
            try:
                SiteID_set.update(set(df["SITEID"]))
            except:
                print(f"SITEID column not found in {file}")
        return SiteID_set

    @property
    def allFeatures(self):
        """test

        :return: aaa
        :rtype: list
        """

        features_set = set()

        for file in os.listdir(self.dataDir):
            df = self.__readCsvFile(file)
            try:
                df["SITEID"]
            except:
                print(
                    f"SITEID not found in {file}. Columns are not going to be added!")
            else:
                features_set.update(set(df.columns))
        return features_set

    def createDataframe(self):
        """tttt

        :param SITEID_set: qqq
        :type SITEID_set: list
        :param COLUMNS_set: aaaa
        :type COLUMNS_set: list
        :param COLUMNS_dict: aaaa
        :type COLUMNS_dict: list
        :return: aaaa
        :rtype: list
        """

        index = count(start=0, step=1)
        first = True

        print(f"[+] getting all siteIDs from the CSV files in {self.dataDir}")
        allSiteID = self.allSiteID
        print(f"[+] collecting siteIDs done!")

        print(f"[+] getting all features from the CSV files in {self.dataDir}")
        allFeatures = self.allFeatures
        print(f"[+] collecting features done!")

        for id in allSiteID:
            SiteID_dict = dict.fromkeys(allFeatures, float("nan"))
            for file in os.listdir(self.dataDir):
                df = self.__readCsvFile(file)
                try:
                    # TODO: must be discussed!
                    SiteID_dict.update(
                        (df.loc[df['SITEID'] == id].iloc[0]).to_dict())
                except:
                    pass

            if first:
                self.data = pd.DataFrame.from_dict(
                    [SiteID_dict], orient='columns')
                first = False
            else:
                self.data = self.data.append(pd.DataFrame.from_dict(
                    [SiteID_dict], orient='columns'), ignore_index=True)

            print(f"index: {next(index)}")

    def pickle(self):
        """ttt
        """
        isempty = self.data.empty
        assert not(
            isempty), "dataframe is empty! You must call the method createDataframe()!"

        self.data.to_pickle(os.path.join(
            self.dataDir, self.dataFile))


# test = DataframeCreator()
# test.createDataframe()
# test.pickle()

# import pickle
# pickle_in = open("data/test_data.pkl","rb")
# data = pickle.load(pickle_in)
# print(data)
