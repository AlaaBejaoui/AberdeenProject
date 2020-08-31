import pickle

def loadPickledData(filepath):
    with open(filepath, 'rb') as f:
        dataframe = pickle.load(f)
    return dataframe