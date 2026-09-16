import joblib
import pandas as pd

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel


# ==========================================
# FASTAPI APP
# ==========================================

app = FastAPI(title="AgriSense AI")


# ==========================================
# 01 - CROP MODEL
# ==========================================

model_crop = joblib.load("01_crop_model.joblib")
features_crop = joblib.load("01_crop_features.joblib")
encoder_crop = joblib.load("01_crop_encoder.joblib")


# ==========================================
# 02 - YIELD MODEL
# ==========================================

model_yield = joblib.load("02_yield_model.joblib")
features_yield = joblib.load("02_yield_features.joblib")

encoder_yield_crop = joblib.load("02_le_crop.joblib")
encoder_yield_state = joblib.load("02_le_state.joblib")
encoder_yield_season = joblib.load("02_le_season.joblib")


# ==========================================
# 03 - YIELD COST MODEL
# ==========================================

model_yield_cost = joblib.load("03_yield_cost_model.joblib")
features_yield_cost = joblib.load("03_yield_cost_features.joblib")

encoder_yield_cost_crop = joblib.load("03_le_crop.joblib")
encoder_yield_cost_state = joblib.load("03_le_state.joblib")


# ==========================================
# MODEL OPTIONS - LOAD ONCE
# ==========================================

YIELD_OPTIONS = {
    "crops": encoder_yield_crop.classes_.tolist(),
    "states": encoder_yield_state.classes_.tolist(),
    "seasons": encoder_yield_season.classes_.tolist()
}


COST_OPTIONS = {
    "crops": encoder_yield_cost_crop.classes_.tolist(),
    "states": encoder_yield_cost_state.classes_.tolist()
}


# ==========================================
# INPUT DATA MODELS
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
# HOME
# ==========================================

@app.get("/")
def home():
    return {
        "message": "AgriSense AI Prediction API",
        "status": "running",
        "endpoint": "POST /predict1, /predict2, /predict3"
    }


# ==========================================
# HEALTH CHECK - CROP
# ==========================================

@app.get("/health1")
def health1():
    return {
        "status": "running",
        "model": "RandomForestClassifier",
        "features": features_crop
    }


# ==========================================
# HEALTH CHECK - YIELD
# ==========================================

@app.get("/health2")
def health2():
    return {
        "status": "running",
        "model": "RandomForestRegressor",
        "features": features_yield
    }


# ==========================================
# HEALTH CHECK - COST
# ==========================================

@app.get("/health3")
def health3():
    return {
        "status": "running",
        "model": "RandomForestRegressor",
        "features": features_yield_cost
    }


# ==========================================
# 01 - CROP SUGGESTION
# POST /predict1
# ==========================================

@app.post("/predict1", status_code=status.HTTP_200_OK)
def predict_crop(Agri1: CropInput):

    try:

        # --------------------------------------
        # Input validation
        # --------------------------------------

        if (
            Agri1.N < 0
            or Agri1.P < 0
            or Agri1.K < 0
            or Agri1.rainfall < 0
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="N, P, K and rainfall cannot be negative."
            )

        # --------------------------------------
        # Prepare input
        # --------------------------------------

        input_data = pd.DataFrame([{
            "N": Agri1.N,
            "P": Agri1.P,
            "K": Agri1.K,
            "temperature": Agri1.temperature,
            "humidity": Agri1.humidity,
            "ph": Agri1.ph,
            "rainfall": Agri1.rainfall
        }])[features_crop]

        # --------------------------------------
        # Prediction
        # --------------------------------------

        predicted_num = model_crop.predict(input_data)[0]

        crop_name = encoder_crop.inverse_transform(
            [predicted_num]
        )

        # --------------------------------------
        # Response
        # --------------------------------------

        return {
            "status": "success",
            "predicted_crop": str(crop_name[0])
        }

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Server side error during crop suggestion: {str(e)}"
        )


# ==========================================
# 02 - YIELD ESTIMATION
# POST /predict2
# ==========================================

@app.post("/predict2", status_code=status.HTTP_200_OK)
def predict_yield(data: YieldInput):

    try:

        # --------------------------------------
        # Area validation
        # --------------------------------------

        if data.Area <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Area must be greater than 0."
            )

        # --------------------------------------
        # Encode Crop, State and Season
        # --------------------------------------

        try:

            crop_enc = encoder_yield_crop.transform(
                [data.Crop]
            )[0]

            state_enc = encoder_yield_state.transform(
                [data.State]
            )[0]

            season_enc = encoder_yield_season.transform(
                [data.Season]
            )[0]

        except ValueError as ve:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unknown Crop, State, or Season: {str(ve)}"
            )

        # --------------------------------------
        # Prepare input
        # --------------------------------------

        input_data = pd.DataFrame([{
            "Crop": crop_enc,
            "State": state_enc,
            "Season": season_enc,
            "Area": data.Area
        }])[features_yield]

        # --------------------------------------
        # Prediction
        # --------------------------------------

        predicted_yield = model_yield.predict(
            input_data
        )[0]

        # --------------------------------------
        # Response
        # --------------------------------------

        return {
            "status": "success",
            "predicted_yield": float(predicted_yield)
        }

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal yield model error: {str(e)}"
        )


# ==========================================
# 03 - COST ESTIMATION
# POST /predict3
# ==========================================

@app.post("/predict3", status_code=status.HTTP_200_OK)
def predict_cost(data: CostInput):

    try:

        # --------------------------------------
        # Yield validation
        # --------------------------------------

        if data.Yield < 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Yield value cannot be negative."
            )

        # --------------------------------------
        # Encode Crop and State
        # --------------------------------------

        try:

            crop_enc = encoder_yield_cost_crop.transform(
                [data.Crop]
            )[0]

            state_enc = encoder_yield_cost_state.transform(
                [data.State]
            )[0]

        except ValueError as ve:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Provided Crop or State is not recognized: {str(ve)}"
            )

        # --------------------------------------
        # Prepare input
        # --------------------------------------

        input_data = pd.DataFrame([{
            "Crop": crop_enc,
            "State": state_enc,
            "Yield": data.Yield
        }])[features_yield_cost]

        # --------------------------------------
        # Prediction
        # --------------------------------------

        predicted_cost = model_yield_cost.predict(
            input_data
        )[0]

        # --------------------------------------
        # Response
        # --------------------------------------

        return {
            "status": "success",
            "predicted_cost": float(predicted_cost)
        }

    except HTTPException as http_ex:
        raise http_ex

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal cost processing error: {str(e)}"
        )


# ==========================================
# YIELD OPTIONS
# GET /yield-options
# ==========================================

@app.get("/yield-options")
def yield_options():

    return YIELD_OPTIONS


# ==========================================
# COST OPTIONS
# GET /cost-options
# ==========================================

@app.get("/cost-options")
def cost_options():

    return COST_OPTIONS