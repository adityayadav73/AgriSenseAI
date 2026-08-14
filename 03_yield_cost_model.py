import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,r2_score
import joblib
import numpy as np
from itertools import product

data =pd.read_csv("archive(43)/datafile (1).csv")

# Collect All UniQUe Crops and States

data.columns =data.columns.str.strip()
data.columns=['Crop','State','Cost_A2FL','Cost_C2','Cost_Prod','Yield']

#data.columns =data.columns.str.strip()


le_crop =LabelEncoder()
data['Crop'] =le_crop.fit_transform(data["Crop"])
le_state =LabelEncoder()
data['State'] =le_state.fit_transform(data["State"])


features = ['Crop','State','Yield']
X = data[features]
y= data['Cost_A2FL']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=24)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train,y_train)
y_pred =model.predict(X_test)

mae =mean_absolute_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)


joblib.dump(model,"03_yield_cost_model.joblib")
joblib.dump(list(X.columns),"03_yield_cost_features.joblib")
joblib.dump(le_crop,"03_le_crop.joblib")
joblib.dump(le_state,"03_le_state.joblib")
