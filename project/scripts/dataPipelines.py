from TransformationWrapper import * 
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, LabelEncoder


#custom transformation
def transformEducation(data):
    if (data == "Assoc-voc") or (data == "Assoc-acdm"):
        data = "Associate"
    elif (data == "11th") or (data == "10th") or (data == "7th-8th") or (data == "9th") \
    or (data == "12th") or (data == "5th-6th") or (data == "1st-4th") or (data == "Preschool"):
        data = "Without HS diploma"
    return data


#pipelines
pipeline_server_pls = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
])

pipeline_hardware_budget = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
])

pipeline_reven_revised = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
])

pipeline_terminal_budget = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
])

pipeline_ent_it_budget = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
    ("label", LabelEncoderP()),
])


pipeline_education = Pipeline([
    ("fillna", SimpleImputer(strategy = "most_frequent", missing_values = np.NaN)),
    ("transformEducation", TransformationWrapper(transformation = transformEducation)),
    ("encodeEducation", OneHotEncoder(categories = "auto", sparse = False)),
    ("scaler", StandardScaler())
])


full_pipeline = ColumnTransformer(
    [
    ("server_pls", pipeline_server_pls, ["SERVER_PLS"]),
    ("hardware_budget", pipeline_hardware_budget, ["HARDWARE_BUDGET"]),
    ("reven_revised", pipeline_reven_revised, ["REVEN_REVISED"]),
    ("terminal_budget", pipeline_terminal_budget, ["TERMINAL_BUDGET"]),
    ("ent_it_budget", pipeline_ent_it_budget, ["ENT_IT_BUDGET"]),
    ],remainder='passthrough', n_jobs=-1)