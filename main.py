import io
import joblib
import pandas as pd 
from fastapi import FastAPI,HTTPException,UploadFile,File
from fastapi.responses import StreamingResponse
from pydantic import BaseModel,Field

app = FastAPI(title="AgriSense AI")
#01_crop_________MOdel_______
model_crop = joblib.load("01_crop_model.joblib")
features_crop = joblib.load("01_crop_features.joblib")
encoder_crop = joblib.load("01_crop_encoder.joblib")

#02____yield_____model_________
model_yield=joblib.load("02_yield_model.joblib")
features_yield = joblib.load("02_yield_features.joblib")
encoder_yield_crop = joblib.load("02_le_crop.joblib")
encoder_yield_state = joblib.load("02_le_state.joblib")
encoder_yield_season = joblib.load("02_le_season.joblib")
#03___yield______cost_____model____
model_yield_cost = joblib.load("03_yield_cost_model.joblib")
features_yield_cost =joblib.load("03_yield_cost_features.joblib")
encoder_yield_cost_crop = joblib.load("03_le_crop.joblib")
encoder_yield_cost_state =joblib.load("03_le_state.joblib")

#Input data
class CropInput(BaseModel):
    N: float
    P: float
    K:float
    temperature: float
    humidity:float
    ph: float
    rainfall:float

class YieldInput(BaseModel):
    Crop:str
    State:str
    Season:str
    Area: float

class CostInput(BaseModel):
    Crop:str
    State:str
    Yield: float

@app.get("/")
def home():
    return{
        "message":"AgriSense AI prediction api",
                "Status":"runnig",
                "endpoin":"send Post requst to /predict"
    }


@app.get("/helth1")
def health1():
    return{
        "status":"running",
        "model":"RandomForestClassifier",
        "features":features_crop,
        
    }

@app.get("/helth2")
def health2():
    return{
        "status":"running",
        "model":"RandomForestRegressor",
        "features":features_yield,
    }

@app.get("/helth3")
def health3():
    return{
        "status":"running",
        "model":"RandomForestRegressor",
        "features":features_yield_cost,
    }

@app.post("/predict1")
def predict_crop(Agri1:CropInput):
    try:
        input_data = pd.DataFrame([{
            "N":Agri1.N,
            "P":Agri1.P,
            "K":Agri1.K,
            "temperature":Agri1.temperature,
            "humidity":Agri1.humidity,
            "ph":Agri1.ph,
            "rainfall":Agri1.rainfall
        }])

        predicted_num = model_crop.predict(input_data)[0]
        crop_name = encoder_crop.inverse_transform([predicted_num])

        return{
            "predict_crop":f"Recommended crop is{crop_name} successfully"
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"prediction faild: {str(e)}"
        )

#Helper function
def get_encoded_val(encoder,user_input):
    clean_input =str(user_input).strip().lower()
    for original_label in encoder.classes_:
        if str(original_label).strip().lower() == clean_input:
            return encoder.transform([original_label])[0]
        
    raise ValueError(f"'{user_input}' not fond.Valid options:{list(encoder.classes_[:5])}")

@app.post("/predict2")
def predict_yield(Agri2:YieldInput):
    try:
        #string inputs label encode create
        crop_enc = get_encoded_val(encoder_yield_crop,Agri2.Crop)
        state_enc =get_encoded_val(encoder_yield_state,Agri2.State)
        season_enc =get_encoded_val(encoder_yield_season,Agri2.Season)

        input_data = pd.DataFrame([{
            "Crop":crop_enc,
            "State":state_enc,
            "Season":season_enc,
            "Area":Agri2.Area
        }])

        predicted = round(model_yield.predict(input_data)[0],2)
        

        return{
            "predict_yield":f"predict yield is {predicted} successfully"
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"prediction faild: {str(e)}"
        )

@app.post("/predict3")
def predict_cost(Agri3:CostInput):
    try:
        crop_enc = get_encoded_val(encoder_yield_cost_crop,Agri3.Crop)
        state_enc = get_encoded_val(encoder_yield_cost_state,Agri3.State)
        input_data = pd.DataFrame([{
            "Crop":crop_enc,
            "State":state_enc,
            "Yield":Agri3.Yield
        }])

        predicted = model_yield_cost.predict(input_data)[0]
        

        return{
            "predict_cost":f"predict{round(predicted)}invest cost is sussfully"
        }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"prediction faild: {str(e)}"
        )