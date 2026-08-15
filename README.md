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

