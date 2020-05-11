import os
import sys
print(sys.path.append(os.getcwd()))
from project.configFile import ConfigurationFile
from project.dataPipelines import full_pipeline
import project.dataCleaning
import pickle
import os
import pandas as pd
import numpy as np

data = pickle.load(open(os.path.join(data_picklefile_dir, data_picklefile), "rb"))

#apply pipeline transformation
data_preprocess = pd.DataFrame(full_pipeline.fit_transform(data))

column_names = np.concatenate((["SERVER_PLS"],
                               ["HARDWARE_BUDGET"],
                               ["REVEN_REVISED"],
                               ["TERMINAL_BUDGET"],
                               ["ENT_IT_BUDGET"])
                              , axis = 0)
data_preprocess.columns = column_names

from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)
clf = clf.fit(data_preprocess[["HARDWARE_BUDGET","REVEN_REVISED","TERMINAL_BUDGET","ENT_IT_BUDGET"]], data_preprocess[["SERVER_PLS"]])
y_pred = clf.predict(data_preprocess[["HARDWARE_BUDGET","REVEN_REVISED","TERMINAL_BUDGET","ENT_IT_BUDGET"]])
from sklearn import metrics 
print("Accuracy:",metrics.accuracy_score(data_preprocess[["SERVER_PLS"]], y_pred))

