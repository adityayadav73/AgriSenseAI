# 🌾 AgriSense AI

AgriSense AI is an agriculture prediction system that uses Machine Learning to provide crop recommendation, crop yield prediction, and agriculture yield & cost prediction.

## 🚀 Features

- 🌱 Crop Recommendation
- 🌾 Crop Yield Prediction
- 💰 Yield & Cost Prediction
- 🖥️ Streamlit Frontend
- ⚡ FastAPI Backend
- 🤖 Machine Learning Models
- ☁️ Render Deployment
## 🏗️ Project Architecture

User  
  │
  ▼
Streamlit Frontend  
  │
  ▼
FastAPI Backend  
  │
  ▼
Machine Learning Models  
  │
  ▼
Prediction  
  │
  ▼
Result  
## Prediction Modules
🌱 Crop Recommendation  
The crop recommendation model uses:  
Nitrogen (N)  
Phosphorus (P)  
Potassium (K)  
Temperature  
Humidity  
pH  
Rainfall  
🌾 Yield Prediction 
The yield prediction module uses agriculture-related features such as:  
Crop  
State  
Season  
Area  
Other model-specific features  
💰 Yield & Cost Prediction  
This module predicts agriculture yield and related cultivation cost using the features required by the trained model.  
## 🛠️ Technologies Used
Python  
Pandas  
NumPy  
Scikit-learn  
Joblib  
FastAPI  
Uvicorn  
Streamlit  
Render  
## Repository Structure
AgriSense-AI/
│
├── mains.py  
├── streamlit_app.py  
├── requirements.txt  
├── README.md  
│
├── 01_crop_model.joblib  
├── 01_crop_features.joblib  
├── 01_crop_encoder.joblib  
│
├── 02_yield_model.joblib  
├── 02_yield_features.joblib  
├── 02_le_crop.joblib  
├── 02_le_state.joblib  
├── 02_le_season.joblib  
│
└── 03_yield_cost_model.joblib  

