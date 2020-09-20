import os
import subprocess
import numpy as np
import pandas as pd
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import export_text
from sklearn.tree import DecisionTreeClassifier
from utilities.loadConfigFile import loadConfigFile


class Model:
    """
    This class extracts the most important features from a dataframe and then creates a model that predicts
    the value of a target variable by learning simple decision rules inferred from the data features.
    """

    # Only Decision Tree and Logistic Regression are currently implemented!
    implemented_algorithms = ("decisionTree", "logisticRegression")

    def __init__(self, dataframe, algorithm, **parameters):
        """
        Class constructor

        :param dataframe: Pandas dataframe used for the model fitting
        :type dataframe: Pandas dataframe
        :param algorithm: Algorithm used to fit the data
        :type algorithm: String
        """

        assert len(label := list(loadConfigFile().get("labels").keys())
                   ) == 1, "Only model fitting for one label is currently implemented!"
        labelName = label[0]

        self.X = dataframe.loc[:, dataframe.columns != labelName]
        self.y = dataframe[labelName]
        assert self.X.__class__.__name__ == "DataFrame", "Features matrix must be a Pandas dataframe!"
        assert self.y.__class__.__name__ == "Series", "Label must be a Pandas serie!"

        assert algorithm in self.__class__.implemented_algorithms, f"{algorithm} not yet implemented!"
        self.algorithm = algorithm

        if self.algorithm == "decisionTree":
            self.model = DecisionTreeClassifier(**parameters)
        elif self.algorithm == "logisticRegression":
            self.model = LogisticRegression(**parameters)

    def fit(self):
        """
        This function builds the model from the training set (self.X, self.y). If the chosen algorithm
        is Decision Tree, then the optimal depth from the function "bestModel" will be used
        """

        if self.algorithm == "decisionTree":
            print('Finding the optimal depth for the decision tree ...')
            optimal_depth = self.bestModel()["max_depth"]
            self.model.max_depth = optimal_depth

        try:
            self.model.fit(self.X, self.y)
        except ValueError:
            # Labels type converted to int
            self.y = self.y.astype('int')
            self.model.fit(self.X, self.y)
        finally:
            print("Model fitting completed successfully!")

    def keepBestFeatures(self):
        """
        This function extracts the best features from the user defined dataframe using Random Forest Classifier
        and writes the resulting features to a text file which will be stored in "results/"
        """

        randomForest = RandomForestClassifier(n_estimators=100)

        try:
            randomForest.fit(self.X, self.y)
        except ValueError:
            # Labels type converted to int
            self.y = self.y.astype('int')
            randomForest.fit(self.X, self.y)
        finally:
            print("Random Forest fitting completed successfully!")

        feature_imp = pd.Series(randomForest.feature_importances_, index=self.X.columns).sort_values(ascending=False)

        ratio = loadConfigFile().get("randomForest").get("ratio")
        
        feature_ratio = int(len(self.X.columns)*ratio)
        self.X = self.X[feature_imp[:feature_ratio].index]

        columnsFile = loadConfigFile().get("fileConfig").get("features_afterRFFiltering")
        
        with open(os.path.join("results/", columnsFile), "w") as f:
            for column in feature_imp[:feature_ratio].index:
                f.write(f"{column}\n")

    def bestModel(self):
        """
        This function finds the optimal depth for the decision tree model by function for fitting trees of
        various depths on the training data and choosing the optimal depth using cross-validation

        :return: Optimal decision tree depth
        :rtype: Integer
        """

        parameters = {'max_depth':range(2,10)}
        clf = GridSearchCV(DecisionTreeClassifier(), parameters, n_jobs=4)
        clf.fit(X=self.X, y=self.y)
        print(f"Best cross validation score: {np.round(clf.best_score_, 1)*100} %")
        print(f"Optimal decision tree depth: {clf.best_params_['max_depth']}")
        optimal_depth = clf.best_params_
        return optimal_depth

    def crossValidation(self, cv):
        """
        This function reports the performance measure by k-fold cross-validation

        :param cv: Number of folds
        :type cv: Integer
        """

        crossValidationScores = self.crossValidationScores(cv)
        scoreMean = np.mean(crossValidationScores)
        scoreVariance = np.var(crossValidationScores)
        print(
            f"Cross validation mean: {scoreMean},\nCross validation variance: {scoreVariance}")

    def crossValidationScores(self, cv):
        """
        This function evaluates a score by cross-validation

        :param cv: Number of folds
        :type cv: Integer
        :return: Cross validation scores
        :rtype: List
        """
        try:
            return cross_val_score(self.model, self.X, self.y, cv=cv)
        except:
            # Labels type converted to int
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
        try:
            subprocess.check_call(command, shell=True)
        except:
            print(f'Please run the following command in a Linux environment: \n {command}')
        else:
            print('Converting the dot file to png completed successfully!')

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
