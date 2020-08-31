import os
import sys
sys.path.append(os.getcwd())

from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier
from utilities.loadConfigFile import loadConfigFile
import numpy as np
import subprocess

class Model:

    implemented_algorithms = ("decisionTree", "logisticRegression")

    def __init__(self, dataframe, algorithm, **parameters):
        
        assert len(label := list(loadConfigFile().get("labels").keys())) == 1, "Only model fitting for one label is currently implemented!"
        labelName = label[0]
        
        self.X = dataframe.loc[:, dataframe.columns != labelName]
        self.y = dataframe[labelName]
        assert self.X.__class__.__name__ == "DataFrame", "features matrix must be a pandas dataframe!"
        assert self.y.__class__.__name__ == "Series", "label must be a pandas serie!"

        assert algorithm in self.__class__.implemented_algorithms, f"{algorithm} not yet implemented!"
        self.algorithm = algorithm

        if self.algorithm == "decisionTree":
            self.model = DecisionTreeClassifier(**parameters)
        elif self.algorithm == "logisticRegression":
            self.model = LogisticRegression(**parameters)

    def fit(self):
        try:
            self.model.fit(self.X, self.y)
        except ValueError:
            print("labels type converted to int!")
            self.y = self.y.astype('int')
            self.model.fit(self.X, self.y)
        finally:
            print("Model fitting completed successfully!")

    def crossValidation(self, cv):
        crossValidationScores = self.crossValidationScores(cv)
        scoreMean = np.mean(crossValidationScores)
        scoreVariance = np.var(crossValidationScores)
        print(
            f"cross validation mean: {scoreMean},\ncross validation variance: {scoreVariance}")

    def crossValidationScores(self, cv):
        try:
            return cross_val_score(self.model, self.X, self.y, cv=cv)
        except:
            print("labels type converted to int!")
            self.y = self.y.astype('int')
            return cross_val_score(self.model, self.X, self.y, cv=cv)
 

    def decisionTreeToGraphiz(self, out_file, feature_names, class_names):

        tree.export_graphviz(self.model,
                             out_file=os.path.join("results/", out_file),
                             feature_names=feature_names,
                             class_names=class_names,
                             filled=True)

    # TODO
    # still not working
    # must be checked!
    def decisionTreeToText(self):
        rules = export_text(self.fit(), feature_names=self.X.columns)
        return rules

    # TODO
    # should be fixed in windows! (its working in linux)
    def graphvizToPng(self, out_file):
        outfile_path = os.path.join("results/", out_file)
        assert os.path.isfile(outfile_path), f"file {out_file!r} does not exist!"
        command = f"dot -Tpng {outfile_path} -o {outfile_path[:-4]}.png"
        subprocess.call(command, shell=True)

    def decisionTreeToPng(self, out_file, feature_names, class_names):
        self.decisionTreeToGraphiz(out_file, feature_names, class_names)
        self.graphvizToPng(out_file)

    def buildRules(self, out_file):
        feature_names = self.X.columns
        class_names = [str(ele) for ele in sorted(self.y.unique())]
        self.decisionTreeToPng(out_file, feature_names, class_names)

    def __str__(self):
        summary = f""" 
        algorithm: {self.algorithm!r} \n
        features: {self.X.columns!r} \n 
        labels: {sorted(self.y.unique())!r} \n 
        """
        return summary
