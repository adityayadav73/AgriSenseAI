from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os


# =========================================================
# FASTAPI APP
# =========================================================

app = FastAPI(
    title="AgriSense AI Prediction API",
    description="AI based agriculture prediction API",
    version="1.0.0"
)


# =========================================================
# MODEL FILE PATHS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CROP_MODEL_PATH = os.path.join(BASE_DIR, "crop_model.pkl")
YIELD_MODEL_PATH = os.path.join(BASE_DIR, "yield_model.pkl")
COST_MODEL_PATH = os.path.join(BASE_DIR, "cost_model.pkl")


# =========================================================
# LOAD MODELS
# =========================================================

crop_model = None
yield_model = None
cost_model = None


def load_model(path):
    if not os.path.exists(path):
        print(f"Model file not found: {path}")
        return None

    try:
        model = joblib.load(path)
        print(f"Loaded model: {path}")
        return model

    except Exception as e:
        print(f"Error loading {path}: {e}")
        return None


crop_model = load_model(CROP_MODEL_PATH)
yield_model = load_model(YIELD_MODEL_PATH)
cost_model = load_model(COST_MODEL_PATH)


# =========================================================
# ROOT
# =========================================================

@app.get("/")
def home():
    return {
        "message": "AgriSense AI prediction api",
        "Status": "running",
        "endpoint": "Send POST request to /predict1, /predict2 or /predict3"
    }


# =========================================================
# CROP SUGGESTION INPUT
# =========================================================

class CropInput(BaseModel):
    N: float
    P: float
    K: float
    temperature: float
    humidity: float
    ph: float
    rainfall: float


# =========================================================
# PRODUCTION / YIELD INPUT
# =========================================================

class YieldInput(BaseModel):
    Crop: str
    State: str
    Season: str
    Area: float


# =========================================================
# COST INPUT
# =========================================================

class CostInput(BaseModel):
    Crop: str
    State: str
    Yield: float


# =========================================================
# PREDICT 1 - CROP SUGGESTION
# =========================================================

@app.post("/predict1")
def predict_crop(data: CropInput):

    if crop_model is None:
        raise HTTPException(
            status_code=500,
            detail="Crop model file is not loaded."
        )

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

        prediction = crop_model.predict(features)

        crop = prediction[0]

        return {
            "predict_crop": f"Recommended crop is {crop}"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Crop suggestion error: {str(e)}"
        )


# =========================================================
# PREDICT 2 - PRODUCTION ESTIMATION
# =========================================================

@app.post("/predict2")
def predict_yield(data: YieldInput):

    if yield_model is None:
        raise HTTPException(
            status_code=500,
            detail="Yield model file is not loaded."
        )

    try:

        features = [[
            data.Crop,
            data.State,
            data.Season,
            data.Area
        ]]

        prediction = yield_model.predict(features)

        result = float(prediction[0])

        return {
            "predict_yield": f"Predicted yield is {result} successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Production estimation error: {str(e)}"
        )


# =========================================================
# PREDICT 3 - COST ESTIMATION
# =========================================================

@app.post("/predict3")
def predict_cost(data: CostInput):

    if cost_model is None:
        raise HTTPException(
            status_code=500,
            detail="Cost model file is not loaded."
        )

    try:

        features = [[
            data.Crop,
            data.State,
            data.Yield
        ]]

        prediction = cost_model.predict(features)

        result = float(prediction[0])

        return {
            "predict_cost": f"Estimated cultivation cost is {result} successfully"
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"Cost estimation error: {str(e)}"
        )


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/health")
def health():

    return {
        "status": "ok",
        "crop_model_loaded": crop_model is not None,
        "yield_model_loaded": yield_model is not None,
        "cost_model_loaded": cost_model is not None
    }