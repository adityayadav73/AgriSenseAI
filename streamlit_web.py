import streamlit as st
import requests
import json
import os


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# API CONFIG
# =========================================================

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)




# =========================================================
# PAGE HEADER
# =========================================================

st.title("🌾 AgriSense AI")
st.subheader("Agriculture Prediction System")

st.markdown(
    """
    Crop recommendation, yield prediction aur agriculture cost
    prediction ek hi dashboard se karein.
    """
)

st.divider()


# =========================================================
# HELPER FUNCTION
# =========================================================

def call_api(endpoint, payload):

    try:

        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            # JSON response
            try:
                return response.json()

            except Exception:
                # Agar StreamingResponse/text response aaye
                return {
                    "message": response.text
                }

        else:

            try:
                error_data = response.json()
            except Exception:
                error_data = response.text

            st.error(
                f"API Error ({response.status_code}): "
                f"{error_data}"
            )

            return None

    except requests.exceptions.ConnectionError:

        st.error(
            "❌ FastAPI server connect nahi ho raha.\n\n"
            "Pehle FastAPI server run karein:\n"
            "`uvicorn mains:app --reload`"
        )

        return None

    except requests.exceptions.Timeout:

        st.error("⏳ API request timeout ho gayi.")

        return None

    except Exception as e:

        st.error(f"Error: {str(e)}")

        return None


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌾 AgriSense AI")

option = st.sidebar.radio(
    "Select Prediction",
    [
        "🌱 Crop Recommendation",
        "🌾 Yield Prediction",
        "💰 Yield & Cost Prediction"
    ]
)

st.sidebar.divider()

st.sidebar.info(
    "FastAPI Backend\n"
    "AgriSense AI Prediction API"
)


# =========================================================
# 1. CROP PREDICTION
# =========================================================

if option == "🌱 Crop Recommendation":

    st.header("🌱 Crop Recommendation")

    st.write(
        "Soil aur weather conditions ke basis par suitable crop predict karein."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=50.0
        )

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=50.0
        )

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=50.0
        )

    with col2:

        temperature = st.number_input(
            "Temperature (°C)",
            value=25.0
        )

        humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=60.0
        )

        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5
        )

    with col3:

        rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=100.0
        )

    st.divider()

    if st.button(
        "🌱 Predict Crop",
        type="primary",
        use_container_width=True
    ):

        payload = {
            "N": N,
            "P": P,
            "K": K,
            "temperature": temperature,
            "humidity": humidity,
            "ph": ph,
            "rainfall": rainfall
        }

        response = requests.post(
            f"{API_URL}/predict1",
            json=payload
        )
        if response.status_code == 200:
            result = response.json()
            st.success("🌾Crop Prediction Successful!")
            st.json(result)
        else:
            st.error(
                f"Error:{response.status_code}"
            )


# =========================================================
# 2. YIELD PREDICTION
# =========================================================

elif option == "🌾 Yield Prediction":

    st.header("🌾 Yield Prediction")

    st.write(
        "Crop, state, season aur area ke basis par expected yield predict karein."
    )

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            "Crop",
            placeholder="e.g. Rice"
        )

        state = st.text_input(
            "State",
            placeholder="e.g. Punjab"
        )

    with col2:

        season = st.text_input(
            "Season",
            placeholder="e.g. Kharif"
        )

        area = st.number_input(
            "Area",
            min_value=0.0,
            value=1.0
        )

    st.divider()

    if st.button(
        "🌾 Predict Yield",
        type="primary",
        use_container_width=True
    ):

        if not crop or not state or not season:

            st.warning(
                "Please Crop, State aur Season fill karein."
            )

        else:

            payload = {
                "Crop": crop,
                "State": state,
                "Season": season,
                "Area": area
            }
            response = requests.post(
                        f"{API_URL}/prediction2",
                        json=payload
                    )
            if response.status_code == 200:
                        result = response.json()
                        st.success("🌾Yield Prediction Successful!")
                        st.json(result)
            else:
                 st.error(
                        f"Error:{response.status_code}"
                    )

            


# =========================================================
# 3. YIELD + COST PREDICTION
# =========================================================

elif option == "💰 Yield & Cost Prediction":

    st.header("💰 Yield & Cost Prediction")

    st.write(
        "Crop, state aur yield ke basis par agriculture cost predict karein."
    )

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            "Crop",
            placeholder="e.g. Rice"
        )

        state = st.text_input(
            "State",
            placeholder="e.g. Punjab"
        )

    with col2:

        yield_value = st.number_input(
            "Yield",
            min_value=0.0,
            value=100.0
        )

    st.divider()

    if st.button(
        "💰 Predict Cost",
        type="primary",
        use_container_width=True
    ):

        if not crop or not state:

            st.warning(
                "Please Crop aur State fill karein."
            )

        else:

            payload = {
                "Crop": crop,
                "State": state,
                "Yield": yield_value
            }

            response = requests.post(
                        f"{API_URL}/predict3",
                        json=payload
                    )
            if response.status_code == 200:
                        result = response.json()
                        st.success("🌾Yield & Cost Prediction Successful!")
                        st.json(result)
            else:
                st.error(
                        f"Error:{response.status_code}"
                )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "© 2026 AgriSense AI | Agriculture Prediction System"
)