import os
import subprocess
import numpy as np
from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier
from utilities.loadConfigFile import loadConfigFile


class Model:
    """
    This class creates a model that predicts the value of a target variable by learning simple decision rules 
    inferred from the data features.
    """

    # Only Decision Tree and Logistic Regression are currently implemented!   
    implemented_algorithms = ("decisionTree", "logisticRegression")

    def __init__(self, dataframe, algorithm, **parameters):
        """Class constructor

        :param dataframe: Pandas Dataframe used to the model fitting
        :type dataframe: Pandas Dataframe
        :param algorithm: Algorithm used to fit the data
        :type algorithm: String
        """

        assert len(label := list(loadConfigFile().get("labels").keys())
                   ) == 1, "Only model fitting for one label is currently implemented!"
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
        """
        This function builds the model from the training set (self.X, self.y)
        """
        try:
            self.model.fit(self.X, self.y)
        except ValueError:
            print("labels type converted to int!")
            self.y = self.y.astype('int')
            self.model.fit(self.X, self.y)
        finally:
            print("Model fitting completed successfully!")

    def crossValidation(self, cv):
        """
        This function reports the performance measure by k-fold cross-validation.

        :param cv: Number of folds
        :type cv: int
        """
        
        crossValidationScores = self.crossValidationScores(cv)
        scoreMean = np.mean(crossValidationScores)
        scoreVariance = np.var(crossValidationScores)
        print(
            f"cross validation mean: {scoreMean},\ncross validation variance: {scoreVariance}")

    def crossValidationScores(self, cv):
        """
        This function evaluates a score by cross-validation

        :param cv: Number of folds
        :type cv: int
        :return: Cross validation scores
        :rtype: list
        """
        try:
            return cross_val_score(self.model, self.X, self.y, cv=cv)
        except:
            print("labels type converted to int!")
            self.y = self.y.astype('int')
            return cross_val_score(self.model, self.X, self.y, cv=cv)

    def decisionTreeToGraphiz(self, out_file, feature_names, class_names):
        """
        This function generates a GraphViz representation of the decision tree in DOT format

        :param out_file: Name of the output file
        :type out_file: String
        :param feature_names: Names of each of the features
        :type feature_names: List
        :param class_names: Name of the target class
        :type class_names: List
        """

        tree.export_graphviz(self.model,
                             out_file=os.path.join("results/", out_file),
                             feature_names=feature_names,
                             class_names=class_names,
                             filled=True)

    # TODO
    # still not working in both Windows and Linux! Must be fixed!
    def decisionTreeToText(self):
        """
        This function builds a text report showing the rules of the decision tree

        :return: Text summary of all the rules in the decision tree
        :rtype: String
        """
        rules = export_text(self.fit(), feature_names=self.X.columns)
        return rules

    # TODO
    # should be fixed in Windows! (its working in Linux!)
    def graphvizToPng(self, out_file):
        """
        Graphical rendering of the decision tree rules from the DOT file 

        :param out_file: Name of the output file
        :type out_file: String
        """
        outfile_path = os.path.join("results/", out_file)
        assert os.path.isfile(
            outfile_path), f"file {out_file!r} does not exist!"
        command = f"dot -Tpng {outfile_path} -o {outfile_path[:-4]}.png"
        subprocess.call(command, shell=True)

    def decisionTreeToPng(self, out_file, feature_names, class_names):
        """
        This function wraps up self.decisionTreeToGraphiz and self.graphvizToPng

        :param out_file: Name of the output file
        :type out_file: String
        :param feature_names: Names of each of the features
        :type feature_names: List
        :param class_names: Name of the target class
        :type class_names: List
        """
        self.decisionTreeToGraphiz(out_file, feature_names, class_names)
        self.graphvizToPng(out_file)

    def buildRules(self, out_file):
        """
        This function exports decision tree rules to an image that can be interpreted by the user 

        :param out_file: Name of the output file
        :type out_file: String
        """
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
