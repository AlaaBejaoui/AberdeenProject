import pickle


def pklToCsv(pathToPklFile, pathToCsvFile):
    """
    This function converts a pkl file into a csv file

    :param pathToPklFile: Path to the pkl file
    :param pathToCsvFile: Path to the csv file
    """
    data = pickle.load(open(pathToPklFile, 'rb'))

    data.to_csv(pathToCsvFile)

