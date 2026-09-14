import os
import re
import requests
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CONFIG
# =========================================================

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-n621.onrender.com"
).rstrip("/")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "").strip()


# =========================================================
# SESSION STATE
# =========================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None


# =========================================================
# TRANSLATIONS
# =========================================================

TEXT = {
    "English": {
        "home": "Home",
        "crop": "Crop Suggestion",
        "yield": "Production Estimation",
        "cost": "Cost Estimation",
        "profit": "Profit Estimation",
        "weather": "Weather",
        "about": "About",
        "language": "Language",

        "welcome": "Welcome to AgriSense AI",
        "subtitle": "Smart agriculture assistance using Artificial Intelligence",

        "crop_title": "🌱 Crop Suggestion",
        "crop_desc": "Enter soil and weather information to get a suitable crop suggestion.",

        "automatic_weather": "🌦️ Automatic Weather",
        "manual_weather": "✍️ Manual Weather",

        "village": "Village",
        "district": "District",
        "state": "State",
        "get_weather": "Get Weather",

        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "rainfall": "Rainfall (mm)",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "Soil pH",

        "suggest_crop": "Get Crop Suggestion",
        "suggested_crop": "Recommended Crop",

        "yield_title": "📊 Production Estimation",
        "yield_desc": "Estimate crop production based on crop, state, season and area.",

        "crop_name": "Crop",
        "season": "Season",
        "area": "Area (Hectare)",
        "estimate_production": "Estimate Production",
        "estimated_yield": "Estimated Yield",
        "yield_unit": "Quintal/Hectare",

        "cost_title": "💰 Cost Estimation",
        "cost_desc": "Estimate cultivation cost based on crop, state and expected yield.",
        "yield_input": "Yield (Quintal/Hectare)",
        "estimate_cost": "Estimate Cost",
        "cultivation_cost": "Cultivation Cost",
        "cost_unit": "₹/Hectare",

        "profit_title": "📈 Profit Estimation",
        "profit_desc": "Calculate expected revenue and profit using your own current selling price.",
        "selling_price": "Selling Price (₹/Quintal)",
        "calculate_profit": "Calculate Profit",
        "total_revenue": "Total Revenue",
        "profit_value": "Estimated Profit",
        "profit_unit": "₹/Hectare",

        "weather_title": "🌦️ Weather",
        "weather_desc": "Get current weather using your village, district and state.",
        "weather_found": "Weather information received successfully.",
        "weather_failed": "Unable to get weather information.",

        "about_title": "ℹ️ About AgriSense AI",
        "about_text": "AgriSense AI is an agriculture assistance platform that uses machine learning to provide crop, production and cost insights.",

        "success": "Success",
        "error": "Error",
        "enter_required": "Please enter all required fields.",
        "api_error": "Backend API request failed.",
        "weather_api_missing": "OPENWEATHER_API_KEY is not configured.",
        "invalid_number": "Please enter a valid number.",

        "english": "English",
        "hindi": "Hindi"
    },

    "Hindi": {
        "home": "होम",
        "crop": "फसल सुझाव",
        "yield": "उत्पादन अनुमान",
        "cost": "लागत अनुमान",
        "profit": "लाभ अनुमान",
        "weather": "मौसम",
        "about": "हमारे बारे में",
        "language": "भाषा",

        "welcome": "AgriSense AI में आपका स्वागत है",
        "subtitle": "कृत्रिम बुद्धिमत्ता द्वारा स्मार्ट कृषि सहायता",

        "crop_title": "🌱 फसल सुझाव",
        "crop_desc": "उपयुक्त फसल का सुझाव प्राप्त करने के लिए मिट्टी और मौसम की जानकारी दर्ज करें।",

        "automatic_weather": "🌦️ स्वचालित मौसम",
        "manual_weather": "✍️ मैनुअल मौसम",

        "village": "गाँव",
        "district": "जिला",
        "state": "राज्य",
        "get_weather": "मौसम प्राप्त करें",

        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "rainfall": "वर्षा (mm)",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "ph": "मिट्टी का pH",

        "suggest_crop": "फसल सुझाव प्राप्त करें",
        "suggested_crop": "सुझाई गई फसल",

        "yield_title": "📊 उत्पादन अनुमान",
        "yield_desc": "फसल, राज्य, मौसम और क्षेत्रफल के आधार पर उत्पादन का अनुमान लगाएँ।",

        "crop_name": "फसल",
        "season": "मौसम",
        "area": "क्षेत्रफल (हेक्टेयर)",
        "estimate_production": "उत्पादन का अनुमान लगाएँ",
        "estimated_yield": "अनुमानित उत्पादन",
        "yield_unit": "क्विंटल/हेक्टेयर",

        "cost_title": "💰 लागत अनुमान",
        "cost_desc": "फसल, राज्य और अपेक्षित उत्पादन के आधार पर खेती की लागत का अनुमान लगाएँ।",
        "yield_input": "उत्पादन (क्विंटल/हेक्टेयर)",
        "estimate_cost": "लागत का अनुमान लगाएँ",
        "cultivation_cost": "खेती की लागत",
        "cost_unit": "₹/हेक्टेयर",

        "profit_title": "📈 लाभ अनुमान",
        "profit_desc": "अपनी वर्तमान बिक्री कीमत के आधार पर अनुमानित राजस्व और लाभ की गणना करें।",
        "selling_price": "बिक्री मूल्य (₹/क्विंटल)",
        "calculate_profit": "लाभ की गणना करें",
        "total_revenue": "कुल राजस्व",
        "profit_value": "अनुमानित लाभ",
        "profit_unit": "₹/हेक्टेयर",

        "weather_title": "🌦️ मौसम",
        "weather_desc": "गाँव, जिला और राज्य के आधार पर वर्तमान मौसम प्राप्त करें।",
        "weather_found": "मौसम की जानकारी सफलतापूर्वक प्राप्त हुई।",
        "weather_failed": "मौसम की जानकारी प्राप्त नहीं हो सकी।",

        "about_title": "ℹ️ AgriSense AI के बारे में",
        "about_text": "AgriSense AI एक कृषि सहायता प्लेटफॉर्म है जो मशीन लर्निंग की मदद से फसल, उत्पादन और लागत संबंधी जानकारी प्रदान करता है।",

        "success": "सफल",
        "error": "त्रुटि",
        "enter_required": "कृपया सभी आवश्यक जानकारी दर्ज करें।",
        "api_error": "Backend API request विफल हुई।",
        "weather_api_missing": "OPENWEATHER_API_KEY कॉन्फ़िगर नहीं है।",
        "invalid_number": "कृपया सही संख्या दर्ज करें।",

        "english": "English",
        "hindi": "Hindi"
    }
}


def t(key):
    return TEXT[st.session_state.language].get(key, key)


# =========================================================
# CROP NAME CLEANING
# =========================================================

CROP_HINDI = {
    "pigeonpeas": "अरहर",
    "pigeon pea": "अरहर",
    "pigeon peas": "अरहर",
    "chickpea": "चना",
    "chickpeas": "चना",
    "rice": "चावल",
    "maize": "मक्का",
    "corn": "मक्का",
    "wheat": "गेहूँ",
    "cotton": "कपास",
    "sugarcane": "गन्ना",
    "banana": "केला",
    "mango": "आम",
    "apple": "सेब",
    "grapes": "अंगूर",
    "watermelon": "तरबूज",
    "muskmelon": "खरबूजा",
    "orange": "संतरा",
    "papaya": "पपीता",
    "coconut": "नारियल",
    "coffee": "कॉफी",
    "blackgram": "उड़द",
    "black gram": "उड़द",
    "mungbean": "मूंग",
    "green gram": "मूंग",
    "lentil": "मसूर",
    "kidneybeans": "राजमा",
    "kidney beans": "राजमा",
    "mothbeans": "मोठ",
    "moth beans": "मोठ",
    "muskmelon": "खरबूजा",
    "jute": "जूट",
    "millet": "बाजरा",
    "bajra": "बाजरा",
    "sorghum": "ज्वार",
    "soybean": "सोयाबीन",
    "groundnut": "मूंगफली",
    "sunflower": "सूरजमुखी",
    "mustard": "सरसों",
}


def clean_crop_name(value):
    """
    Converts backend responses such as:
    'Recommended crop ispigeonpeas'
    into:
    'Pigeon Peas'
    """

    if value is None:
        return "Unknown"

    text = str(value).strip().lower()

    # Remove common backend prefixes
    patterns = [
        "recommended crop is",
        "recommended crop:",
        "recommended crop",
        "predict crop is",
        "predict_crop",
        "crop is",
        "crop:"
    ]

    for pattern in patterns:
        text = text.replace(pattern, "")

    text = text.strip(" :-_")

    # Remove accidental 'is'
    if text.startswith("is"):
        text = text[2:].strip()

    # Remove spaces/underscores for matching
    normalized = re.sub(r"[\s_-]+", "", text)

    aliases = {
        "pigeonpeas": "Pigeon Peas",
        "pigeonpea": "Pigeon Peas",
        "chickpea": "Chickpea",
        "chickpeas": "Chickpea",
        "blackgram": "Black Gram",
        "mungbean": "Green Gram",
        "greengram": "Green Gram",
        "kidneybeans": "Kidney Beans",
        "mothbeans": "Moth Beans",
    }

    if normalized in aliases:
        return aliases[normalized]

    # Normal formatting
    return text.title()


def crop_name_hindi(value):
    if value is None:
        return "अज्ञात"

    text = str(value).strip().lower()

    for key, hindi_name in CROP_HINDI.items():
        if key.replace(" ", "") in text.replace(" ", ""):
            return hindi_name

    cleaned = clean_crop_name(value)

    for key, hindi_name in CROP_HINDI.items():
        if key.replace(" ", "") in cleaned.lower().replace(" ", ""):
            return hindi_name

    return cleaned


# =========================================================
# NUMBER EXTRACTION
# =========================================================

def extract_number(value):
    """
    Handles responses like:

    'predict yield is 1.3 successfully'
    'predict12143invest cost is sussfully'
    12143
    {'predict_cost': '...12143...'}
    """

    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    if isinstance(value, dict):
        for v in value.values():
            result = extract_number(v)
            if result is not None:
                return result
        return None

    text = str(value)

    # Find decimal or integer
    matches = re.findall(r"-?\d+(?:\.\d+)?", text)

    if not matches:
        return None

    try:
        return float(matches[-1])
    except Exception:
        return None


# =========================================================
# API REQUEST
# =========================================================

def post_api(endpoint, payload):
    url = f"{FASTAPI_URL}{endpoint}"

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return None, f"HTTP {response.status_code}: {response.text[:300]}"

        try:
            return response.json(), None
        except Exception:
            return {"response": response.text}, None

    except requests.exceptions.Timeout:
        return None, "Request timed out."

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to backend."

    except Exception as e:
        return None, str(e)


# =========================================================
# OPENWEATHER
# =========================================================

def get_weather(village, district, state):
    if not OPENWEATHER_API_KEY:
        return None, t("weather_api_missing")

    location = f"{village}, {district}, {state}, India"

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": location,
        "appid": OPENWEATHER_API_KEY,
        "units": "metric"
    }

    try:
        response = requests.get(
            url,
            params=params,
            timeout=20
        )

        if response.status_code != 200:
            return None, response.text[:300]

        data = response.json()

        temperature = data.get("main", {}).get("temp", 0)
        humidity = data.get("main", {}).get("humidity", 0)

        # OpenWeather current weather may provide rainfall for last hour.
        rainfall = data.get("rain", {}).get("1h", 0)

        weather = {
            "temperature": float(temperature),
            "humidity": float(humidity),
            "rainfall": float(rainfall)
        }

        return weather, None

    except Exception as e:
        return None, str(e)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🌾 AgriSense AI")

    st.caption("Smart Agriculture Assistant")

    st.divider()

    language = st.radio(
        t("language"),
        ["English", "Hindi"],
        index=0 if st.session_state.language == "English" else 1
    )

    st.session_state.language = language

    st.divider()

    pages = {
        "Home": t("home"),
        "Crop": t("crop"),
        "Yield": t("yield"),
        "Cost": t("cost"),
        "Profit": t("profit"),
        "Weather": t("weather"),
        "About": t("about")
    }

    for page_key, page_label in pages.items():
        if st.button(
            page_label,
            use_container_width=True,
            key=f"nav_{page_key}"
        ):
            st.session_state.page = page_key

    st.divider()

    st.caption("AgriSense AI")
    st.caption("AI-powered agriculture assistance")


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.title("🌾 AgriSense AI")

    st.header(t("welcome"))

    st.write(t("subtitle"))

    st.info(
        "🌱 Crop Suggestion  •  "
        "📊 Production Estimation  •  "
        "💰 Cost Estimation  •  "
        "📈 Profit Estimation"
    )

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("🌱", t("crop"))

    with col2:
        st.metric("📊", t("yield"))

    with col3:
        st.metric("💰", t("cost"))

    with col4:
        st.metric("📈", t("profit"))

    st.divider()

    st.subheader("🌾 Smart Farming with AI")

    st.write(
        "AgriSense AI helps farmers and agriculture users "
        "make better decisions using soil, weather and crop information."
    )

    st.success(
        "Start with Crop Suggestion to get a suitable crop based on soil and weather data."
    )


# =========================================================
# CROP SUGGESTION
# =========================================================

elif st.session_state.page == "Crop":

    st.title(t("crop_title"))

    st.write(t("crop_desc"))

    # -----------------------------------------------------
    # AUTOMATIC WEATHER
    # -----------------------------------------------------

    st.subheader(t("automatic_weather"))

    st.info(
        "Village + District + State enter करें और "
        "Get Weather दबाएँ। Weather data OpenWeather से आएगा "
        "और Crop Suggestion में directly use होगा."
        if st.session_state.language == "Hindi"
        else
        "Enter Village + District + State and press Get Weather. "
        "Weather data will come from OpenWeather and will be directly used for Crop Suggestion."
    )

    weather_col1, weather_col2, weather_col3 = st.columns(3)

    with weather_col1:
        village = st.text_input(
            t("village"),
            key="crop_village"
        )

    with weather_col2:
        district = st.text_input(
            t("district"),
            key="crop_district"
        )

    with weather_col3:
        state = st.text_input(
            t("state"),
            key="crop_state"
        )

    if st.button(
        f"🌦️ {t('get_weather')}",
        use_container_width=True,
        key="crop_get_weather"
    ):

        if not village.strip() or not district.strip() or not state.strip():
            st.warning(t("enter_required"))

        else:
            with st.spinner("Getting weather..."):

                weather, error = get_weather(
                    village,
                    district,
                    state
                )

            if weather:
                st.session_state.weather_data = weather

                st.success(t("weather_found"))

            else:
                st.error(
                    f"{t('weather_failed')} {error}"
                )

    # Show automatic weather
    if st.session_state.weather_data:

        weather = st.session_state.weather_data

        st.subheader("🌦️ Current Weather")

        w1, w2, w3 = st.columns(3)

        with w1:
            st.metric(
                t("temperature"),
                f"{weather['temperature']:.1f} °C"
            )

        with w2:
            st.metric(
                t("humidity"),
                f"{weather['humidity']:.1f} %"
            )

        with w3:
            st.metric(
                t("rainfall"),
                f"{weather['rainfall']:.2f} mm"
            )

    # -----------------------------------------------------
    # MANUAL WEATHER
    # -----------------------------------------------------

    st.divider()

    st.subheader(t("manual_weather"))

    manual_col1, manual_col2, manual_col3 = st.columns(3)

    with manual_col1:
        manual_temperature = st.number_input(
            t("temperature"),
            min_value=-50.0,
            max_value=70.0,
            value=25.0,
            step=0.1,
            key="manual_temperature"
        )

    with manual_col2:
        manual_humidity = st.number_input(
            t("humidity"),
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=0.1,
            key="manual_humidity"
        )

    with manual_col3:
        manual_rainfall = st.number_input(
            t("rainfall"),
            min_value=0.0,
            max_value=5000.0,
            value=100.0,
            step=1.0,
            key="manual_rainfall"
        )

    # -----------------------------------------------------
    # SOIL INPUT
    # -----------------------------------------------------

    st.divider()

    st.subheader("🌱 Soil Information")

    soil_col1, soil_col2, soil_col3 = st.columns(3)

    with soil_col1:
        nitrogen = st.number_input(
            t("nitrogen"),
            min_value=0.0,
            max_value=500.0,
            value=50.0,
            step=1.0
        )

    with soil_col2:
        phosphorus = st.number_input(
            t("phosphorus"),
            min_value=0.0,
            max_value=500.0,
            value=50.0,
            step=1.0
        )

    with soil_col3:
        potassium = st.number_input(
            t("potassium"),
            min_value=0.0,
            max_value=500.0,
            value=50.0,
            step=1.0
        )

    ph_value = st.number_input(
        t("ph"),
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )

    # -----------------------------------------------------
    # WEATHER MODE
    # -----------------------------------------------------

    weather_mode = st.radio(
        "Weather Input",
        ["Automatic Weather", "Manual Weather"],
        horizontal=True,
        key="crop_weather_mode"
    )

    if weather_mode == "Automatic Weather":

        if st.session_state.weather_data is None:

            st.warning(
                "पहले Automatic Weather में Village, District और State डालकर Get Weather दबाएँ।"
                if st.session_state.language == "Hindi"
                else
                "First enter Village, District and State and press Get Weather."
            )

        else:
            final_weather = st.session_state.weather_data

            st.info(
                "Automatic weather values will be used for Crop Suggestion."
            )

    else:

        final_weather = {
            "temperature": manual_temperature,
            "humidity": manual_humidity,
            "rainfall": manual_rainfall
        }

        st.info(
            "Manual weather values will be used for Crop Suggestion."
        )

    # -----------------------------------------------------
    # CROP BUTTON
    # -----------------------------------------------------

    st.divider()

    if st.button(
        f"🌱 {t('suggest_crop')}",
        type="primary",
        use_container_width=True
    ):

        if (
            weather_mode == "Automatic Weather"
            and st.session_state.weather_data is None
        ):
            st.error(
                "Please get Automatic Weather first."
                if st.session_state.language == "English"
                else
                "पहले Automatic Weather प्राप्त करें।"
            )

        else:

            payload = {
                "N": float(nitrogen),
                "P": float(phosphorus),
                "K": float(potassium),
                "temperature": float(final_weather["temperature"]),
                "humidity": float(final_weather["humidity"]),
                "ph": float(ph_value),
                "rainfall": float(final_weather["rainfall"])
            }

            with st.spinner("Getting crop suggestion..."):

                result, error = post_api(
                    "/predict1",
                    payload
                )

            if error:

                st.error(
                    f"{t('api_error')} {error}"
                )

            else:

                raw_crop = None

                if isinstance(result, dict):

                    raw_crop = (
                        result.get("predict_crop")
                        or result.get("crop")
                        or result.get("prediction")
                    )

                if raw_crop is None:
                    raw_crop = result

                english_crop = clean_crop_name(raw_crop)
                hindi_crop = crop_name_hindi(raw_crop)

                st.success(t("success"))

                if st.session_state.language == "Hindi":
                    st.metric(
                        t("suggested_crop"),
                        hindi_crop
                    )

                    st.info(
                        f"English: {english_crop}"
                    )

                else:
                    st.metric(
                        t("suggested_crop"),
                        english_crop
                    )

                    st.info(
                        f"हिंदी: {hindi_crop}"
                    )


# =========================================================
# PRODUCTION / YIELD ESTIMATION
# =========================================================

elif st.session_state.page == "Yield":

    st.title(t("yield_title"))

    st.write(t("yield_desc"))

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            t("crop_name"),
            placeholder="Example: Rice"
        )

        state = st.text_input(
            t("state"),
            placeholder="Example: Uttar Pradesh"
        )

    with col2:

        season = st.text_input(
            t("season"),
            placeholder="Example: Kharif"
        )

        area = st.number_input(
            t("area"),
            min_value=0.01,
            value=1.0,
            step=0.1
        )

    st.caption(
        "Enter area in Hectare."
        if st.session_state.language == "English"
        else
        "क्षेत्रफल Hectare में दर्ज करें।"
    )

    if st.button(
        f"📊 {t('estimate_production')}",
        type="primary",
        use_container_width=True
    ):

        if not crop.strip() or not state.strip() or not season.strip():

            st.warning(t("enter_required"))

        else:

            payload = {
                "Crop": crop.strip(),
                "State": state.strip(),
                "Season": season.strip(),
                "Area": float(area)
            }

            with st.spinner("Estimating production..."):

                result, error = post_api(
                    "/predict2",
                    payload
                )

            if error:

                st.error(
                    f"{t('api_error')} {error}"
                )

            else:

                raw_value = None

                if isinstance(result, dict):

                    raw_value = (
                        result.get("predict_yield")
                        or result.get("yield")
                        or result.get("prediction")
                    )

                if raw_value is None:
                    raw_value = result

                estimated_yield = extract_number(raw_value)

                if estimated_yield is None:

                    st.error(
                        "Could not read production value from backend response."
                    )

                else:

                    st.success(t("success"))

                    st.metric(
                        t("estimated_yield"),
                        f"{estimated_yield:.2f} {t('yield_unit')}"
                    )


# =========================================================
# COST ESTIMATION
# =========================================================

elif st.session_state.page == "Cost":

    st.title(t("cost_title"))

    st.write(t("cost_desc"))

    crop = st.text_input(
        t("crop_name"),
        placeholder="Example: Rice"
    )

    state = st.text_input(
        t("state"),
        placeholder="Example: Uttar Pradesh"
    )

    yield_value = st.number_input(
        t("yield_input"),
        min_value=0.0,
        value=1.0,
        step=0.1
    )

    st.info(
        "This module is independent. Production Estimation values are not automatically carried here."
        if st.session_state.language == "English"
        else
        "यह मॉड्यूल स्वतंत्र है। Production Estimation की values यहाँ अपने आप नहीं आएँगी।"
    )

    if st.button(
        f"💰 {t('estimate_cost')}",
        type="primary",
        use_container_width=True
    ):

        if not crop.strip() or not state.strip():

            st.warning(t("enter_required"))

        else:

            payload = {
                "Crop": crop.strip(),
                "State": state.strip(),
                "Yield": float(yield_value)
            }

            with st.spinner("Estimating cultivation cost..."):

                result, error = post_api(
                    "/predict3",
                    payload
                )

            if error:

                st.error(
                    f"{t('api_error')} {error}"
                )

            else:

                raw_value = None

                if isinstance(result, dict):

                    raw_value = (
                        result.get("predict_cost")
                        or result.get("cost")
                        or result.get("prediction")
                    )

                if raw_value is None:
                    raw_value = result

                estimated_cost = extract_number(raw_value)

                if estimated_cost is None:

                    st.error(
                        "Could not read cost value from backend response."
                    )

                else:

                    st.success(t("success"))

                    st.metric(
                        t("cultivation_cost"),
                        f"₹{estimated_cost:,.2f} / Hectare"
                    )


# =========================================================
# PROFIT ESTIMATION
# =========================================================

elif st.session_state.page == "Profit":

    st.title(t("profit_title"))

    st.write(t("profit_desc"))

    st.info(
        "Profit Estimation is completely independent. Enter all values manually."
        if st.session_state.language == "English"
        else
        "लाभ अनुमान पूरी तरह स्वतंत्र है। सभी values यहाँ manually दर्ज करें।"
    )

    crop = st.text_input(
        t("crop_name"),
        placeholder="Example: Rice",
        key="profit_crop"
    )

    state = st.text_input(
        t("state"),
        placeholder="Example: Uttar Pradesh",
        key="profit_state"
    )

    profit_col1, profit_col2 = st.columns(2)

    with profit_col1:

        profit_yield = st.number_input(
            t("yield_input"),
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="profit_yield"
        )

        cultivation_cost = st.number_input(
            f"{t('cultivation_cost')} (₹/Hectare)",
            min_value=0.0,
            value=0.0,
            step=100.0,
            key="profit_cost"
        )

    with profit_col2:

        selling_price = st.number_input(
            t("selling_price"),
            min_value=0.0,
            value=2500.0,
            step=100.0,
            key="profit_selling_price"
        )

    st.caption(
        "Calculation is for 1 Hectare."
        if st.session_state.language == "English"
        else
        "गणना 1 Hectare के लिए है।"
    )

    if st.button(
        f"📈 {t('calculate_profit')}",
        type="primary",
        use_container_width=True
    ):

        if not crop.strip() or not state.strip():

            st.warning(t("enter_required"))

        else:

            # Revenue for 1 hectare
            total_revenue = (
                profit_yield * selling_price
            )

            # Profit for 1 hectare
            profit_value = (
                total_revenue - cultivation_cost
            )

            st.success(t("success"))

            result_col1, result_col2 = st.columns(2)

            with result_col1:

                st.metric(
                    t("total_revenue"),
                    f"₹{total_revenue:,.2f} / Hectare"
                )

            with result_col2:

                st.metric(
                    t("profit_value"),
                    f"₹{profit_value:,.2f} / Hectare"
                )

            if profit_value > 0:

                st.success(
                    "✅ Profitable"
                    if st.session_state.language == "English"
                    else
                    "✅ लाभ की स्थिति"
                )

            elif profit_value < 0:

                st.error(
                    "⚠️ Estimated loss"
                    if st.session_state.language == "English"
                    else
                    "⚠️ अनुमानित नुकसान"
                )

            else:

                st.warning(
                    "Break-even"
                    if st.session_state.language == "English"
                    else
                    "लाभ और नुकसान बराबर"
                )


# =========================================================
# WEATHER PAGE
# =========================================================

elif st.session_state.page == "Weather":

    st.title(t("weather_title"))

    st.write(t("weather_desc"))

    st.subheader(t("automatic_weather"))

    col1, col2, col3 = st.columns(3)

    with col1:
        weather_village = st.text_input(
            t("village"),
            key="weather_village"
        )

    with col2:
        weather_district = st.text_input(
            t("district"),
            key="weather_district"
        )

    with col3:
        weather_state = st.text_input(
            t("state"),
            key="weather_state"
        )

    if st.button(
        f"🌦️ {t('get_weather')}",
        type="primary",
        use_container_width=True,
        key="weather_page_button"
    ):

        if (
            not weather_village.strip()
            or not weather_district.strip()
            or not weather_state.strip()
        ):

            st.warning(t("enter_required"))

        else:

            with st.spinner("Getting weather..."):

                weather, error = get_weather(
                    weather_village,
                    weather_district,
                    weather_state
                )

            if weather:

                st.session_state.weather_data = weather

                st.success(t("weather_found"))

            else:

                st.error(
                    f"{t('weather_failed')} {error}"
                )

    if st.session_state.weather_data:

        weather = st.session_state.weather_data

        st.divider()

        st.subheader("🌦️ Current Weather")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                t("temperature"),
                f"{weather['temperature']:.1f} °C"
            )

        with col2:
            st.metric(
                t("humidity"),
                f"{weather['humidity']:.1f} %"
            )

        with col3:
            st.metric(
                t("rainfall"),
                f"{weather['rainfall']:.2f} mm"
            )

    st.divider()

    st.subheader(t("manual_weather"))

    m1, m2, m3 = st.columns(3)

    with m1:
        st.number_input(
            t("temperature"),
            value=25.0,
            step=0.1,
            key="weather_manual_temp"
        )

    with m2:
        st.number_input(
            t("humidity"),
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=0.1,
            key="weather_manual_humidity"
        )

    with m3:
        st.number_input(
            t("rainfall"),
            min_value=0.0,
            value=100.0,
            step=1.0,
            key="weather_manual_rainfall"
        )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.title(t("about_title"))

    st.write(t("about_text"))

    st.divider()

    st.subheader("🌾 AgriSense AI")

    st.write(
        """
        AgriSense AI combines agriculture data, machine learning
        and weather information to assist with farming decisions.
        """
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("🌱 Crop Suggestion")

    with col2:
        st.info("📊 Production Estimation")

    with col3:
        st.info("💰 Cost & Profit Analysis")


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌾 AgriSense AI | Smart Agriculture Assistant"
)