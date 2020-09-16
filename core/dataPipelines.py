import numpy as np
import pandas as pd
from numpy import arange
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder
from utilities.loadConfigFile import loadConfigFile
from itertools import chain

class FullPipeline:
    """
    This class chains multiple pipelines (the missing values pipeline, the preprocessing pipeline, ...) 
    into one single pipeline.  
    """
    
    pipelines = [] 

    columns = None
        
    @classmethod
    def initialize(cls, data):
        """
        This function initializes the full pipeline with the Pandas dataframe. 
        The column names will be stored as a class attribute and then recovered when needed.

        :param data: Pandas dataframe needed for the initialization
        :type data: Pandas Dataframe
        """
        cls.columns = data.columns

    @classmethod
    def _recoverColumnsNames(cls):
        """
        This function returns the column names of the Pandas dataframe

        :return: Column names of the Pandas dataframe
        :rtype: List
        """
        return cls.columns

    def addPipeline(self, pipeline):
        """
        This function adds a given pipeline to the full pipeline

        :param pipeline: Data pipeline to be added the full pipeline
        :type pipeline: Pipeline
        """
        self.__class__.pipelines.append(pipeline)

    def fit_transform(self, data):
        """
        This function feeds the data to the full pipeline

        :param data: Pandas dataframe to be transformed
        :type data: Pandas dataframe
        :return: Transformed Pandas dataframe
        :rtype: Pandas dataframe
        """
        
        for pipeline in self.__class__.pipelines:
            if isinstance(pipeline, PreprocessingPipeline):
                data = pipeline.fit_transform(data)
            else:
                data = pd.DataFrame(pipeline.fit_transform(data))
                data.columns = self.__class__._recoverColumnsNames()

        return data

class MissingValuesPipeline:
    """
    This class provides a pipeline for completing missing values.
    """

    allowed_strategies = ("mean", "median", "most_frequent", "constant")

    pipelines = {}

    def __init__(self):
        """
        Check whether the full pipeline is initialized with the dataframe.
        """
        assert not(FullPipeline.columns.empty), "You have to initialize the entire pipeline with the data in order to keep the columns names!" 

    def addSimpleImputerPipeline(self, column, strategy="most_frequent"):
        """
        This function provides basic strategies for imputing missing values that can be imputed with a provided constant value, or using 
        the statistics (mean, median or most frequent) of a column in which the missing values are located.

        :param column: Column of the Pandas dataframe
        :type column: String
        :param strategy: Strategy of the imputation, defaults to "most_frequent"
        :type strategy: String, optional
        """
        assert strategy in self.__class__.allowed_strategies, f"{strategy}: Unknown imputation strategy!"

        self.__class__.pipelines[column] = Pipeline(
            [("fillna", SimpleImputer(strategy=strategy, missing_values=np.NaN)), ])

    def buildPipeline(self):
        """
        This function builds the missing values pipeline and prepares it to be fed with the Pandas dataframe.
        """
        
        for featureOrLabel, strategy in chain(loadConfigFile().get("features").items(), loadConfigFile().get("labels").items()):
            self.addSimpleImputerPipeline(featureOrLabel, strategy.get("missing"))

    def fit_transform(self, dataframe, remainder="passthrough", parallelize=True):
        """
        Fit to data, then transform it

        :param dataframe: Pandas dataframe to be passed through the missing values pipeline
        :type dataframe: Pandas dataframe
        :param remainder: By specifying remainder='passthrough', all remaining columns that were not specified in transformers will be automatically passed through. Otherweise, non-specified columns are dropped, defaults to "passthrough"
        :type remainder: String, optional
        :param parallelize: Parallelize the job using all processors, defaults to True
        :type parallelize: Boolean, optional
        :return: Pandas dataframe without missing values
        :rtype: Pandas dataframe
        """

        if parallelize:
            n_jobs = -1

        columnTransformer = ColumnTransformer(
            [
                (column, pipeline, [column]) for (column, pipeline) in self.__class__.pipelines.items()
            ], remainder=remainder, n_jobs=n_jobs)

        transformedData = columnTransformer.fit_transform(dataframe)

        return transformedData 

        
class PreprocessingPipeline:
    """
    This class provides a pipeline for data preprocessing like one-hot encoding.
    """

    allowed_strategies = ("onehot", "None")

    pipelines = {}

    def __init__(self):
        """
        Check whether the full pipeline is initialized with the dataframe.
        """
        assert not(FullPipeline.columns.empty), "You have to initialize the entire pipeline with the data in order to keep the columns names!" 

    def addOnehotEncoderPipeline(self, column, strategy=None):
        """
        Encode categorical feature as a one-hot numeric array

        :param column: Column of the Pandas dataframe
        :type column: String
        :param strategy: Preprocessing strategy, defaults to None
        :type strategy: String or None, optional
        """
        assert strategy in self.__class__.allowed_strategies, f"{strategy}: Unknown strategy!"

        if strategy != "None":
            self.__class__.pipelines[column] = lambda dataframe: pd.get_dummies(dataframe[column], prefix=column)
        else:
            self.__class__.pipelines[column] = None

    def buildPipeline(self):
        """
        This function builds the preprocessing pipeline and prepares it to be fed with the Pandas dataframe.
        """
        for featureOrLabel, strategy in chain(loadConfigFile().get("features").items(), loadConfigFile().get("labels").items()):
            self.addOnehotEncoderPipeline(featureOrLabel, strategy.get("preprocessing"))

    def fit_transform(self, dataframe):
        """
        Fit to data, then transform it

        :param dataframe: Pandas dataframe to be passed through the preprocessing pipeline
        :type dataframe: Pandas dataframe
        :return: Transformed Pandas dataframe 
        :rtype: Pandas dataframe
        """
        assert dataframe.__class__.__name__ == "DataFrame", "Only working with pandas dataframe!"
        
        onehot_dataframe = pd.DataFrame()
        for column, pipeline in self.__class__.pipelines.items(): 
            if pipeline != None:
                onehot_dataframe = pd.concat([onehot_dataframe, pipeline(dataframe)], axis=1)
            else:
                onehot_dataframe = pd.concat([onehot_dataframe, dataframe[column]], axis=1)
        return onehot_dataframe



