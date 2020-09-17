import os
import sys
sys.path.append(os.getcwd())

import pandas as pd
from scipy.stats import bernoulli
from core.modelFitting import Model
from sklearn import tree

# testing the code with boston dataset
from sklearn.datasets import load_boston

data = load_boston()
X = pd.DataFrame(data=data["data"], columns=data["feature_names"])
y = pd.Series(bernoulli.rvs(size=506, p=0.5))

# testing the model with target classes as integer (0,1)
model_1 = Model(X, y, "decisionTree")
print(model_1)
model_1.fit()
model_1.buildRules("classes_as_integer.dot")
# still not working!
# rules = model_1.decisionTreeToText()

# testing the model with target classes as strings (class_0,class_1)
y = pd.Series(bernoulli.rvs(size=506, p=0.5))
y[y == 0] = "class_0"
y[y == 1] = "class_1"
model_2 = Model(X, y, "decisionTree", criterion='entropy', splitter='best', max_depth=2)
model_2.crossValidation(20)
print(model_2)
model_2.fit()
model_2.buildRules("classes_as_string.dot")

# testing the cross validation
cv = 20
crossValidationScore = model_1.crossValidationScores(cv=cv)
assert len(crossValidationScore) == cv , "Dimension test failed!"
model_1.crossValidation(cv)


# logistic regression
model_3 = Model(X, y, "logisticRegression", max_iter=10000, penalty="l2")
model_3.crossValidation(cv=cv)
model_3.fit()
      