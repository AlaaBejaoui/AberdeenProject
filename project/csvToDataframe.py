from configFile import *
import os
import pandas as pd

def extractAllSITEID():
    """test
    
    :return: aaa
    :rtype: list
    """

    SITEID_set = set()
    for file in os.listdir(data_csv_dir):
        df = pd.read_csv(os.path.join(data_csv_dir, file), sep='\t')
        try:
            SITEID_set.update(set(df["SITEID"]))
        except:
            print(f"SITEID not found in {file}")
    return SITEID_set 


def extractAllFeatures():
    """test
    
    :return: aaa
    :rtype: list
    """

    COLUMNS_set = set()
    COLUMNS_dict = {}
    for file in os.listdir(data_csv_dir):
        df = pd.read_csv(os.path.join(data_csv_dir, file), sep='\t')
        try:
            df["SITEID"]
        except:
            print(f"SITEID not found in {file}. Columns are not going to be added!")
        else:
            COLUMNS_dict[file] = set(df.columns)
            COLUMNS_set.update(set(df.columns))
    return COLUMNS_set, COLUMNS_dict

#TODO: parall. with a decorator
def createDataFrame(SITEID_set, COLUMNS_set, COLUMNS_dict):
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

    index=0
    first = True
    for id in SITEID_set:
        SITEID_dict = dict.fromkeys(COLUMNS_set, float("nan"))     
        for _, (file, _)  in enumerate(COLUMNS_dict.items()):
            df = pd.read_csv(os.path.join(data_csv_dir, file), sep='\t')
            try:
                SITEID_dict.update((df.loc[df['SITEID'] == id].iloc[0]).to_dict()) #TODO: must be discussed!
            except:
                pass

        if first:
            data = pd.DataFrame.from_dict([SITEID_dict],orient='columns')
            first = False
        else:
            data = data.append(pd.DataFrame.from_dict([SITEID_dict],orient='columns'), ignore_index = True) 

        print(f"index: {index}")
        index+=1
    return data

def main():
    """main function
    """

    SITEID_set = extractAllSITEID()
    COLUMNS_set, COLUMNS_dict = extractAllFeatures()
    dataframe = createDataFrame(SITEID_set, COLUMNS_set, COLUMNS_dict)
    dataframe.to_pickle(os.path.join(data_picklefile_dir, data_picklefile)) 

if __name__ == "__main__":
    main()
