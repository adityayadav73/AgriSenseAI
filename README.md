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

You can try the live application here:
## 🌐 Live Demo
You can try the live application here:  
👉 **[AgriSense AI Web App](https://agrisenseai-gps1.onrender.com/)**

