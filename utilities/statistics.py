from utilities.loadPickledData import loadPickledData

class Statistics:
    """
    This class generates descriptive statistics of a dataframe
    """

    def __init__(self, filepath):
        """
        The constructor loads the pickled dataframe

        :param filepath: path of the pickeled dataframe
        :type filepath: String
        """
        
        self.filepath = filepath
        self.dataframe = loadPickledData(self.filepath)
    
    def getShape(self):
        """
        get the shape of a Pandas Dataframe

        :return: shape of a dataframe
        :rtype: tuple
        """

        return self.dataframe.shape

    def getKeptColumns(self):
        """
        get the kept columns of a Pandas Dataframe
        :return: Kept columns
        :rtype: List
        """

        return list(self.dataframe.columns)

    def getNumKeptColumns(self):
        """
        get the number kept columns of a Pandas Dataframe

        :return: Number of kept columns
        :rtype: int
        """

        return len(list(self.dataframe.columns))

    def getUniqueValues(self):
        """
        get unique values per columns

        :return: Dict containing the unique values per column
        :rtype: Dict
        """

        uniqueValue_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                uniqueValue_dict[column] = self.dataframe[column].unique()
            except:
                print(f" problem by the column: {column}")
        return uniqueValue_dict

    def getColumnsStatistics(self):
        """
        return a Series containing counts of unique values per columns

        :return: counts of unique values per columns
        :rtype: Dict
        """

        statistics_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                statistics_dict[column] = self.dataframe[column].value_counts(normalize=True,dropna=False)*100
            except:
                print(f" problem by the column: {column}")
        return statistics_dict
