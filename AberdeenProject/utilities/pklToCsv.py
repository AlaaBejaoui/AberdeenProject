import pickle


def pklToCsv(pathToPklFile, pathToCsvFile):
    """

    This function converts a pkl file into a csv file

    :param pathToPklFile: Path to the pkl file
    :type pathToPklFile: String
    :param pathToCsvFile: Path to the csv file
    :type pathToCsvFile: String
    """

    data = pickle.load(open(pathToPklFile, 'rb'))

    data.to_csv(pathToCsvFile)

