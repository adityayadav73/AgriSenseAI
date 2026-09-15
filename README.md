# 🌾 AgriSense AI

AgriSense AI is a Machine Learning based agriculture decision-support system designed to help farmers and users make better farming decisions.

The application provides:

- 🌱 Crop Suggestion
- 📊 Yield Estimation
- 💰 Cost Estimation
- 📈 Profit Estimation
- 🌦️ Weather-based inputs

The system uses a **Streamlit frontend**, **FastAPI backend**, and trained **Machine Learning models**.

---

## 🚀 Features

### 🌱 Crop Suggestion
Recommends a suitable crop based on:

- Nitrogen (N)
- Phosphorus (P)
- Potassium (K)
- Temperature
- Humidity
- pH
- Rainfall

Weather information can be provided through:

- 🌦️ Automatic Weather
- ✏️ Manual Weather Input

---

### 📊 Yield Estimation

Estimates agricultural production based on:

- Crop
- State
- Season
- Area

The available Crop, State, and Season options are automatically loaded from the trained model encoders.

---

### 💰 Cost Estimation

Estimates cultivation cost based on:

- Crop
- State
- Yield

The available Crop and State options are automatically loaded from the trained model encoders.

---

### 📈 Profit Estimation

Calculates estimated profit using:

- Estimated Yield
- Estimated Cost
- Expected Selling Price

The profit is calculated using the estimated agricultural production and cultivation cost.

---

## 🌦️ Weather Integration

AgriSense AI supports weather information for crop suggestions.

Users can either:

1. Enter a District and State to fetch weather information automatically.
2. Enter Temperature, Humidity, and Rainfall manually.

Weather data is used as an input for the Crop Suggestion module.

---

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
Crop / Yield / Cost Estimation  
  │
  ▼
Result  
## 🖥️ Application Pages
The Streamlit application contains the following pages:  
🏠 Home  
🌱 Crop Suggestion  
📊 Yield Estimation  
💰 Cost Estimation  
📈 Profit Estimation  
ℹ️ About  
The application also supports:  
🇬🇧 English  
🇮🇳 Hindi  
## 🛠️ Technologies Used
Python  
Pandas  
NumPy  
Scikit-learn  
Joblib  
FastAPI  
Uvicorn  
Streamlit  
Requests  
OpenWeather API  
Render  
## 📁 Repository Structure
AgriSense-AI/  
│  
├── main.py  
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
├── 03_yield_cost_model.joblib  
├── 03_yield_cost_features.joblib  
├── 03_le_crop.joblib  
└── 03_le_state.joblib  

You can try the live application here:
## 🌐 Live Demo
You can try the live application here:
# Streamlit Frontend
👉 **[AgriSense AI Web App](https://agrisenseai-gps1.onrender.com/)**
# FastAPI Backend
👉 **[AgriSense AI Web App API](https://agrisenseai-n621.onrender.com)**



