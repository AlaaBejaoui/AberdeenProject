from ..utilities.loadPickledData import loadPickledData

class Statistics:
    """
    This class generates descriptive statistics of a Pandas dataframe
    """

    def __init__(self, filepath):
        """
        The constructor loads the pickled dataframe

        :param filepath: Path to the pickeled dataframe
        :type filepath: String
        """
        
        self.filepath = filepath
        self.dataframe = loadPickledData(self.filepath)
    
    def getShape(self):
        """
        This function returns the shape of a given Pandas dataframe

        :return: Shape of a Pandas dataframe
        :rtype: Tuple
        """

        return self.dataframe.shape

    def getKeptColumns(self):
        """
        This function returns the remaining columns of a Pandas dataframe

        :return: Remaining columns of a Pandas dataframe
        :rtype: List
        """

        return list(self.dataframe.columns)

    def getNumKeptColumns(self):
        """
        This function returns the number of remaining columns of a Pandas dataframe

        :return: Number of remaining columns
        :rtype: Integer
        """

        return len(list(self.dataframe.columns))

    def getUniqueValues(self):
        """
        This function returns all unique values per column

        :return: Dictionary containing all unique values per column
        :rtype: Dictionary
        """

        uniqueValue_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                uniqueValue_dict[column] = self.dataframe[column].unique()
            except:
                print(f" Problem by the column: {column}")
        return uniqueValue_dict

    def getColumnsStatistics(self):
        """
        This function returns a Series containing counts of unique values per column

        :return: Dictionary containing all counts of unique values per column
        :rtype: Dictionary
        """

        statistics_dict = dict.fromkeys(self.dataframe.columns, None)
        for column in self.dataframe.columns:
            try:
                statistics_dict[column] = self.dataframe[column].value_counts(normalize=True,dropna=False)*100
            except:
                print(f" Problem by the column: {column}")
        return statistics_dict
