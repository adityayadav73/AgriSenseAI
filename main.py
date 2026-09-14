import os
import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="AgriSense AI Prediction API",
    description="AI based agriculture prediction API",
    version="1.0.0"
)

# ==========================================
# FILE PATH CONFIGURATION
# ==========================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Crop Recommendation Model & Encoder Paths
CROP_MODEL_PATH = os.path.join(BASE_DIR, "01_crop_model.joblib")
CROP_ENCODER_PATH = os.path.join(BASE_DIR, "01_crop_encoder.joblib")

# Yield Prediction Model & Encoder Paths
YIELD_MODEL_PATH = os.path.join(BASE_DIR, "02_yield_model.joblib")
YIELD_LE_CROP_PATH = os.path.join(BASE_DIR, "02_le_crop.joblib")
YIELD_LE_STATE_PATH = os.path.join(BASE_DIR, "02_le_state.joblib")
YIELD_LE_SEASON_PATH = os.path.join(BASE_DIR, "02_le_season.joblib")

# Cost Prediction Model & Encoder Paths
COST_MODEL_PATH = os.path.join(BASE_DIR, "03_yield_cost_model.joblib")
COST_LE_CROP_PATH = os.path.join(BASE_DIR, "03_le_crop.joblib")
COST_LE_STATE_PATH = os.path.join(BASE_DIR, "03_le_state.joblib")

# ==========================================
# ARTIFACT LOADER
# ==========================================
def load_artifact(path: str):
    if not os.path.exists(path):
        print(f"Warning: File not found at {path}")
        return None
    try:
        artifact = joblib.load(path)
        print(f"Successfully loaded: {path}")
        return artifact
    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None

# Load Models
crop_model = load_artifact(CROP_MODEL_PATH)
yield_model = load_artifact(YIELD_MODEL_PATH)
cost_model = load_artifact(COST_MODEL_PATH)

# Load Encoders
crop_encoder = load_artifact(CROP_ENCODER_PATH)

yield_le_crop = load_artifact(YIELD_LE_CROP_PATH)
yield_le_state = load_artifact(YIELD_LE_STATE_PATH)
yield_le_season = load_artifact(YIELD_LE_SEASON_PATH)

cost_le_crop = load_artifact(COST_LE_CROP_PATH)
cost_le_state = load_artifact(COST_LE_STATE_PATH)

# ==========================================
# INPUT SCHEMAS
# ==========================================
class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float

class YieldInput(BaseModel):
    Crop: str
    State: str
    Season: str
    Area: float

class CostInput(BaseModel):
    Crop: str
    State: str
    Yield: float

# ==========================================
# API ENDPOINTS
# ==========================================
@app.get("/")
def home():
    return {
        "message": "AgriSense AI prediction api",
        "status": "running",
        "endpoint": "Send POST request to /predict1, /predict2 or /predict3"
    }

@app.post("/predict1")
def predict_crop(data: CropInput):
    if crop_model is None or crop_encoder is None:
        raise HTTPException(status_code=500, detail="Crop recommendation model or encoder is not loaded.")
    try:
        features = [[
            data.N,
            data.P,
            data.K,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]]
        encoded_pred = crop_model.predict(features)[0]
        crop_name = crop_encoder.inverse_transform([encoded_pred])[0]
        
        return {"predict_crop": f"Recommended crop is {crop_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Crop suggestion error: {str(e)}")

@app.post("/predict2")
def predict_yield(data: YieldInput):
    if yield_model is None or not all([yield_le_crop, yield_le_state, yield_le_season]):
        raise HTTPException(status_code=500, detail="Yield prediction model or required encoders are not loaded.")
    try:
        encoded_crop = yield_le_crop.transform([data.Crop])[0]
        encoded_state = yield_le_state.transform([data.State])[0]
        encoded_season = yield_le_season.transform([data.Season])[0]
        
        features = [[encoded_crop, encoded_state, encoded_season, data.Area]]
        predicted_yield = yield_model.predict(features)[0]
        
        return {"predicted_yield": float(predicted_yield)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Encoding error: Invalid string input provided ({str(e)})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Yield prediction error: {str(e)}")

@app.post("/predict3")
def predict_cost(data: CostInput):
    if cost_model is None or not all([cost_le_crop, cost_le_state]):
        raise HTTPException(status_code=500, detail="Cost prediction model or required encoders are not loaded.")
    try:
        encoded_crop = cost_le_crop.transform([data.Crop])[0]
        encoded_state = cost_le_state.transform([data.State])[0]
        
        features = [[encoded_crop, encoded_state, data.Yield]]
        predicted_cost = cost_model.predict(features)[0]
        
        return {"predicted_cost_A2FL": float(predicted_cost)}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Encoding error: Invalid string input provided ({str(e)})")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cost prediction error: {str(e)}")