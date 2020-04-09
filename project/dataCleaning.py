from configFile import *
import pickle
import os
import math

data = pickle.load(open(os.path.join(data_picklefile_dir, data_picklefile), "rb"))

def saveData(dataToSave, fileName):
    """testtt
    
    :param dataToSave: data
    :type dataToSave: float
    :param fileName: tttt
    :type fileName: float
    """
    dataToSave.to_pickle(os.path.join(data_picklefile_dir, fileName))


def getKeptColumns():
    """zzz
    
    :return: qqqq
    :rtype: list
    """
    keptColumns = set(dataAfterDeletingColumns().columns)
    removedColumns = set(data.columns).difference(set(dataAfterDeletingColumns().columns))
    numKeptColumns = len(keptColumns)
    numRemovedColumns = len(removedColumns)
    return keptColumns, numKeptColumns, removedColumns, numRemovedColumns


def dataAfterDeletingColumns():
    """qoqqq
    
    :return: klkl
    :rtype: list
    """
    columnsToDrop_list = []
    for column, dropDecision in takeDecision().items():
        if dropDecision==True:
            columnsToDrop_list.append(column)
    return data.drop(columnsToDrop_list, axis=1)


def takeDecision():
    """llll
    
    :return: tttt
    :rtype: list
    """
    decision_dict = {}
    decisionForNaN_dict = takeDecisionForNaN()
    decisionManually_dict = pickle.load(open(os.path.join(data_picklefile_dir, manualDecisionFile), "rb"))
    for (column_nan,nanDropDecision), (column_manual,manualDropDecision) in zip(decisionForNaN_dict.items(), decisionManually_dict.items()):
        decision_dict[column_nan] = nanDropDecision or manualDropDecision
    return decision_dict


def getUniqueValuePerColumn():
    """aaaa
    
    :return: qqqq
    :rtype: list
    """
    uniqueValue_dict = dict.fromkeys(data.columns, None) 
    for column in data.columns:
        uniqueValue_dict[column] = data[column].unique()
    return uniqueValue_dict


def getColumnsStatistics():
    """qqqq
    
    :return: iiii
    :rtype: list
    """
    statistics_dict = dict.fromkeys(data.columns, None) 
    for column in data.columns:
        statistics_dict[column] = data[column].value_counts(normalize=True,dropna=False)*100
    return statistics_dict


def takeDecisionManually():
    """manual
    """
    try:
        decisionManually_dict = pickle.load(open(os.path.join(data_picklefile_dir, manualDecisionFile), "rb"))
        print("\n")
        print("[*] file already exists!")
        print("[*] you can modify the prvious decisions using the function (changeManualDecision)!")
        print("[*] Would you like to repeat the procedure for all the columns in the database?")
        decision = input("[*] press y (for yes) or n (for no) : ")
        print("\n")
        if decision == "n":
            return
        elif decision == "y":
            pass
    except:
        pass
    decisionManually_dict = dict.fromkeys(data.columns, False)
    print("\n")
    print("[*] manual selection of the columns to be removed")
    print("[*] if you would like to remove a column, press (t), (T), (true) or (True), else press enter")
    print("[*] Decisions will be saved in pickle file that can be found in ", os.path.join(data_picklefile_dir, manualDecisionFile))
    print("[*] Decisions could be modified using the function (changeManualDecision)") #TODO:name of the function
    print("\n")

    print("\n")
    print("[*] Would you like to keep all columns?") 
    keepAllColumnsDecision = input(f"yes (y) or no (n) : ")
    print("\n")
    if keepAllColumnsDecision == "y":
        pickle.dump(decisionManually_dict, open(os.path.join(data_picklefile_dir, manualDecisionFile), "wb"))
        return
    elif keepAllColumnsDecision == "n":
        for column, _ in decisionManually_dict.items():
            decision = input(f"remove {column} : ")
            if decision in ("t", "T", "true", "True"):
                decisionManually_dict[column] = True 
        pickle.dump(decisionManually_dict, open(os.path.join(data_picklefile_dir, manualDecisionFile), "wb"))


def changeManualDecision():
    """test
    """
    try:
        decisionManually_dict = pickle.load(open(os.path.join(data_picklefile_dir, manualDecisionFile), "rb"))
        print("\n")
        print("[*] manual changing of the previous decisions")
        print("[*] give the name of the column to be removed")
        print("[*] After you have finshed, write (end)")  
        print("\n")
        while True:
            column = input(f"column to be removed : ")
            if column == "end":
                break
            else:
                if column in decisionManually_dict.keys():
                    decisionManually_dict[column] = True
                else:
                    print("column does not exist, try again!")
        pickle.dump(decisionManually_dict, open(os.path.join(data_picklefile_dir, manualDecisionFile), "wb"))
    except:
        print("\n")
        print("file does not exist!")
        print("call the function (takeDecisionManually) to create it!")
        print("\n")


def takeDecisionForNaN():
    """qqq
    
    :return: qqq
    :rtype: list
    """
    statistics_dict = getColumnsStatistics()
    decisionForNaN_dict = dict.fromkeys(statistics_dict.keys(), False)
    for column, columnStat in statistics_dict.items():
        for index, value in columnStat.items():
            try:
                if math.isnan(index):
                    if value >= nan_threshold:
                        decisionForNaN_dict[column] = True
                    break #only checking for nan. Quit the for loop after finding the nan 
            except:
                pass      
    return decisionForNaN_dict

def main():
    """uuu
    """
    while True:
        print("\n")
        print("[1] get unique value of a column")
        print("[2] get column statistics")
        print("[3] remove some columns manually") #TODO: not precise
        print("[4] remove one columns manually") #TODO: not precise
        print("[5] list all columns that are kept")
        print("[6] save the data")
        print("[end] close")
        print("\n")

        action = input("choose the action to do : ")

        if action == "1":
            column = input("column's name : ")
            print(getUniqueValuePerColumn()[column])
        if action == "2":
            column = input("column's name : ")
            print(getColumnsStatistics()[column])
        if action == "3":
            takeDecisionManually()
        if action == "4":
            changeManualDecision()
        if action == "5":
            keptColumns, numKeptColumns, removedColumns, numRemovedColumns = getKeptColumns()
            print("\n")
            print("columns kept are : \n")
            print(keptColumns)
            print("\n")
            print("columns removed are : \n")
            print(removedColumns)
            print("\n")
            print(f"number of columns kept : {numKeptColumns}")
            print(f"number of columns removed : {numRemovedColumns}")
            print("\n")
        if action == "6":
            fileName = input("file name : ")
            saveData(dataAfterDeletingColumns(), fileName)
        if action == "end":
            break

if __name__ == "__main__":
    main()
      

