import pickle


def loadPickledData(filepath):
    """
    This function reads the pickled representation of an object from a file 

    :param filepath: Path to the pickled file
    :type filepath: String
    :return: The reconstituted dataframe
    :rtype: Pandas dataframe
    """

    with open(filepath, 'rb') as f:
        dataframe = pickle.load(f)
    return dataframe
