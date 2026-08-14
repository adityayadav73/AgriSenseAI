import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error,r2_score
import joblib

data =pd.read_csv("archive(42)/crop_yield.csv")

le_crop =LabelEncoder()
data['Crop'] =le_crop.fit_transform(data["Crop"])
le_state =LabelEncoder()
data['State'] =le_state.fit_transform(data["State"])
le_season =LabelEncoder()
data['Season'] =le_season.fit_transform(data["Season"])

features = ['Crop','State','Season','Area']

X = data[features]
y = data['Yield']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2,random_state=24)

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X_train,y_train)
y_pred =model.predict(X_test)

mee =mean_absolute_error(y_test,y_pred)
r2 = r2_score(y_test,y_pred)

joblib.dump(model,"02_yield_model.joblib")
joblib.dump(list(X.columns),"02_yield_features.joblib")
joblib.dump(le_crop,"02_le_crop.joblib")
joblib.dump(le_state,"02_le_state.joblib")
joblib.dump(le_season,"02_le_season.joblib")

