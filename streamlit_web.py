import streamlit as st
import requests
import os
import re


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# CONFIGURATION
# =========================================================

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-n621.onrender.com"
).rstrip("/")

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY",
    ""
)


# =========================================================
# SESSION STATE
# =========================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "language" not in st.session_state:
    st.session_state.language = "English"

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None


# =========================================================
# BASIC STYLE
# =========================================================

st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    .main-title {
        font-size: 42px;
        font-weight: 700;
        color: #185c37;
    }

    .sub-title {
        color: #66736b;
        font-size: 17px;
    }

    .result-box {
        padding: 20px;
        border-radius: 12px;
        background-color: #eaf7ee;
        border: 1px solid #c9e8d2;
        margin-top: 20px;
    }

    .result-title {
        color: #39734a;
        font-size: 15px;
    }

    .result-value {
        color: #14532d;
        font-size: 28px;
        font-weight: 700;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TRANSLATIONS
# =========================================================

TEXT = {

    "English": {
        "home": "Home",
        "crop": "Crop Suggestion",
        "yield": "Yield Estimation",
        "cost": "Cost Estimation",
        "profit": "Profit Estimation",
        "about": "About",
        "title": "AgriSense AI",
        "subtitle": "Smart Agriculture Assistant",
        "crop_desc": "Get a suitable crop suggestion using soil and weather conditions.",
        "yield_desc": "Estimate agricultural yield based on crop, state, season and area.",
        "cost_desc": "Estimate cultivation cost per hectare.",
        "profit_desc": "Calculate expected revenue and profit.",
        "automatic_weather": "Automatic Weather",
        "manual_weather": "Manual Weather",
        "district": "District",
        "state": "State",
        "get_weather": "Get Weather",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "rainfall": "Rainfall (mm)",
        "soil": "Soil Information",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "Soil pH",
        "get_crop": "Get Crop Suggestion",
        "recommended": "Recommended Crop",
        "crop": "Crop",
        "season": "Season",
        "area": "Area (Hectare)",
        "estimate_yield": "Estimate Yield",
        "yield_result": "Yield Estimate",
        "yield_unit": "Quintal / Hectare",
        "estimate_cost": "Estimate Cost",
        "cost_result": "Cultivation Cost",
        "cost_unit": "₹ / Hectare",
        "profit_yield": "Yield (Quintal / Hectare)",
        "cultivation_cost": "Cultivation Cost (₹ / Hectare)",
        "selling_price": "Selling Price (₹ / Quintal)",
        "calculate_profit": "Calculate Profit",
        "revenue": "Total Revenue",
        "profit_result": "Estimated Profit",
        "per_hectare": "per hectare",
        "english": "English",
        "hindi": "हिन्दी"
    },

    "Hindi": {
        "home": "होम",
        "crop": "फसल सुझाव",
        "yield": "उत्पादन अनुमान",
        "cost": "लागत अनुमान",
        "profit": "लाभ अनुमान",
        "about": "जानकारी",
        "title": "AgriSense AI",
        "subtitle": "स्मार्ट कृषि सहायक",
        "crop_desc": "मिट्टी और मौसम की जानकारी के आधार पर उपयुक्त फसल का सुझाव प्राप्त करें।",
        "yield_desc": "फसल, राज्य, मौसम और क्षेत्रफल के आधार पर उत्पादन का अनुमान लगाएं।",
        "cost_desc": "प्रति हेक्टेयर खेती की लागत का अनुमान लगाएं।",
        "profit_desc": "कुल आय और अनुमानित लाभ की गणना करें।",
        "automatic_weather": "स्वचालित मौसम",
        "manual_weather": "मैनुअल मौसम",
        "district": "जिला",
        "state": "राज्य",
        "get_weather": "मौसम प्राप्त करें",
        "temperature": "तापमान (°C)",
        "humidity": "नमी (%)",
        "rainfall": "वर्षा (mm)",
        "soil": "मिट्टी की जानकारी",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "ph": "मिट्टी का pH",
        "get_crop": "फसल सुझाव प्राप्त करें",
        "recommended": "सुझाई गई फसल",
        "crop": "फसल",
        "season": "मौसम",
        "area": "क्षेत्रफल (हेक्टेयर)",
        "estimate_yield": "उत्पादन अनुमान लगाएं",
        "yield_result": "उत्पादन अनुमान",
        "yield_unit": "क्विंटल / हेक्टेयर",
        "estimate_cost": "लागत अनुमान लगाएं",
        "cost_result": "खेती की लागत",
        "cost_unit": "₹ / हेक्टेयर",
        "profit_yield": "उत्पादन (क्विंटल / हेक्टेयर)",
        "cultivation_cost": "खेती की लागत (₹ / हेक्टेयर)",
        "selling_price": "बिक्री मूल्य (₹ / क्विंटल)",
        "calculate_profit": "लाभ की गणना करें",
        "revenue": "कुल आय",
        "profit_result": "अनुमानित लाभ",
        "per_hectare": "प्रति हेक्टेयर",
        "english": "English",
        "hindi": "हिन्दी"
    }
}


def t(key):
    return TEXT[st.session_state.language].get(key, key)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌾 AgriSense AI")
    st.caption("Smart Agriculture Assistant")

    st.divider()

    if st.button("🏠 " + t("home"), use_container_width=True):
        st.session_state.page = "Home"

    if st.button("🌱 " + t("crop"), use_container_width=True):
        st.session_state.page = "Crop Suggestion"

    if st.button("📊 " + t("yield"), use_container_width=True):
        st.session_state.page = "Yield Estimation"

    if st.button("💰 " + t("cost"), use_container_width=True):
        st.session_state.page = "Cost Estimation"

    if st.button("📈 " + t("profit"), use_container_width=True):
        st.session_state.page = "Profit Estimation"

    if st.button("ℹ️ " + t("about"), use_container_width=True):
        st.session_state.page = "About"

    st.divider()

    st.write("Language")

    language = st.radio(
        "",
        ["English", "Hindi"],
        index=0 if st.session_state.language == "English" else 1
    )

    st.session_state.language = language


# =========================================================
# API HELPER
# =========================================================

def call_api(endpoint, payload):

    try:

        response = requests.post(
            f"{FASTAPI_URL}{endpoint}",
            json=payload,
            timeout=60
        )

        if response.status_code == 200:
            return response.json(), None

        return None, f"API Error: {response.status_code}"

    except requests.exceptions.Timeout:

        return None, "Request timed out. Please try again."

    except requests.exceptions.ConnectionError:

        return None, "FastAPI server is not reachable."

    except Exception as e:

        return None, str(e)


# =========================================================
# NUMBER EXTRACTOR
# =========================================================

def extract_number(value):

    if isinstance(value, (int, float)):
        return float(value)

    text = str(value)

    text = text.replace(",", "")

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        text
    )

    if numbers:
        return float(numbers[0])

    return 0.0


# =========================================================
# CROP NAME CLEANER
# =========================================================

def clean_crop_name(value):

    crop = str(value)

    crop = re.sub(
        r"recommended crop is",
        "",
        crop,
        flags=re.IGNORECASE
    )

    crop = re.sub(
        r"recommended crop",
        "",
        crop,
        flags=re.IGNORECASE
    )

    crop = crop.strip()

    crop_map = {

        "pigeonpeas": "Pigeon Peas",
        "pigeon peas": "Pigeon Peas",

        "kidneybeans": "Kidney Beans",
        "kidney beans": "Kidney Beans",

        "blackgram": "Black Gram",
        "black gram": "Black Gram",

        "chickpea": "Chickpea",
        "chickpeas": "Chickpeas",

        "rice": "Rice",
        "maize": "Maize",
        "cotton": "Cotton",
        "jute": "Jute",
        "coffee": "Coffee",
        "banana": "Banana",
        "apple": "Apple",
        "grapes": "Grapes",
        "mango": "Mango",
        "watermelon": "Watermelon",
        "muskmelon": "Muskmelon",
        "orange": "Orange",
        "papaya": "Papaya",
        "coconut": "Coconut",
        "lentil": "Lentil"

    }

    key = crop.lower().strip()

    return crop_map.get(
        key,
        crop.replace("_", " ").title()
    )


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        f'<div class="main-title">🌾 {t("title")}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="sub-title">{t("subtitle")}</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.success(
        "Smart farming decisions using Machine Learning and agricultural data."
        if st.session_state.language == "English"
        else
        "मशीन लर्निंग और कृषि डेटा की मदद से बेहतर खेती के निर्णय लें।"
    )

    st.subheader("🌱 " + t("crop"))

    st.write(t("crop_desc"))

    if st.button(
        "🌱 " + t("get_crop"),
        type="primary"
    ):

        st.session_state.page = "Crop Suggestion"
        st.rerun()

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.info(
            "🌱\n\n**" + t("crop") + "**\n\n" +
            t("crop_desc")
        )

    with col2:
        st.info(
            "📊\n\n**" + t("yield") + "**\n\n" +
            t("yield_desc")
        )

    with col3:
        st.info(
            "💰\n\n**" + t("cost") + "**\n\n" +
            t("cost_desc")
        )

    with col4:
        st.info(
            "📈\n\n**" + t("profit") + "**\n\n" +
            t("profit_desc")
        )


# =========================================================
# CROP SUGGESTION
# =========================================================

elif st.session_state.page == "Crop Suggestion":

    st.title("🌱 " + t("crop"))

    st.write(t("crop_desc"))

    st.divider()

    # -----------------------------------------
    # AUTOMATIC WEATHER
    # -----------------------------------------

    st.subheader("🌦️ " + t("automatic_weather"))

    st.info(
        "Enter District and State to get current weather."
        if st.session_state.language == "English"
        else
        "जिला और राज्य दर्ज करके वर्तमान मौसम की जानकारी प्राप्त करें।"
    )

    col1, col2 = st.columns(2)

    with col1:

        district = st.text_input(
            t("district"),
            placeholder="Prayagraj"
        )

    with col2:

        weather_state = st.text_input(
            t("state"),
            placeholder="Uttar Pradesh"
        )


    if st.button(
        "🌦️ " + t("get_weather"),
        key="weather_button"
    ):

        if not district or not weather_state:

            st.warning(
                "Please enter District and State."
                if st.session_state.language == "English"
                else
                "कृपया जिला और राज्य दर्ज करें।"
            )

        elif not OPENWEATHER_API_KEY:

            st.error(
                "OPENWEATHER_API_KEY is not configured."
            )

        else:

            try:

                query = f"{district}, {weather_state}, India"

                url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                    f"?q={requests.utils.quote(query)}"
                    f"&appid={OPENWEATHER_API_KEY}"
                    "&units=metric"
                )

                response = requests.get(
                    url,
                    timeout=20
                )

                if response.status_code != 200:

                    st.error(
                        "Weather not found. Check District and State."
                    )

                else:

                    weather = response.json()

                    temperature = float(
                        weather["main"]["temp"]
                    )

                    humidity = float(
                        weather["main"]["humidity"]
                    )

                    rainfall = float(
                        weather.get("rain", {}).get(
                            "1h",
                            0
                        )
                    )

                    st.session_state.weather_data = {

                        "temperature": temperature,
                        "humidity": humidity,
                        "rainfall": rainfall

                    }

                    st.success(
                        "Weather loaded successfully."
                        if st.session_state.language == "English"
                        else
                        "मौसम की जानकारी सफलतापूर्वक प्राप्त हो गई।"
                    )

            except Exception as e:

                st.error(
                    f"Weather Error: {e}"
                )


    # Show automatic weather

    if st.session_state.weather_data:

        weather = st.session_state.weather_data

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🌡️ " + t("temperature"),
                f"{weather['temperature']:.1f} °C"
            )

        with col2:
            st.metric(
                "💧 " + t("humidity"),
                f"{weather['humidity']:.1f} %"
            )

        with col3:
            st.metric(
                "🌧️ " + t("rainfall"),
                f"{weather['rainfall']:.1f} mm"
            )


    st.divider()


    # -----------------------------------------
    # MANUAL WEATHER
    # -----------------------------------------

    st.subheader("✍️ " + t("manual_weather"))

    col1, col2, col3 = st.columns(3)

    with col1:

        manual_temperature = st.number_input(
            t("temperature"),
            value=25.0,
            step=0.1
        )

    with col2:

        manual_humidity = st.number_input(
            t("humidity"),
            value=60.0,
            step=0.1
        )

    with col3:

        manual_rainfall = st.number_input(
            t("rainfall"),
            value=100.0,
            step=0.1
        )


    weather_mode = st.radio(
        "Weather Mode",
        [
            "Automatic Weather",
            "Manual Weather"
        ],
        horizontal=True
    )


    st.divider()


    # -----------------------------------------
    # SOIL
    # -----------------------------------------

    st.subheader("🌱 " + t("soil"))

    col1, col2, col3 = st.columns(3)

    with col1:

        nitrogen = st.number_input(
            t("nitrogen"),
            value=50.0,
            step=0.1
        )

    with col2:

        phosphorus = st.number_input(
            t("phosphorus"),
            value=50.0,
            step=0.1
        )

    with col3:

        potassium = st.number_input(
            t("potassium"),
            value=50.0,
            step=0.1
        )


    ph_value = st.number_input(
        t("ph"),
        value=6.5,
        min_value=0.0,
        max_value=14.0,
        step=0.1
    )


    st.write("")


    # -----------------------------------------
    # SELECT WEATHER VALUES
    # -----------------------------------------

    if weather_mode == "Automatic Weather":

        if st.session_state.weather_data is None:

            st.warning(
                "First enter District and State and click Get Weather."
                if st.session_state.language == "English"
                else
                "पहले जिला और राज्य दर्ज करके मौसम प्राप्त करें।"
            )

            weather_ready = False

        else:

            weather = st.session_state.weather_data

            temperature = weather["temperature"]
            humidity = weather["humidity"]
            rainfall = weather["rainfall"]

            weather_ready = True

    else:

        temperature = manual_temperature
        humidity = manual_humidity
        rainfall = manual_rainfall

        weather_ready = True


    # -----------------------------------------
    # CROP BUTTON
    # -----------------------------------------

    if st.button(
        "🌱 " + t("get_crop"),
        type="primary",
        use_container_width=True
    ):

        if not weather_ready:

            st.warning(
                "Please load automatic weather first."
            )

        else:

            payload = {

                "N": float(nitrogen),

                "P": float(phosphorus),

                "K": float(potassium),

                "temperature": float(
                    temperature
                ),

                "humidity": float(
                    humidity
                ),

                "ph": float(ph_value),

                "rainfall": float(
                    rainfall
                )

            }


            with st.spinner(
                "Getting crop suggestion..."
            ):

                data, error = call_api(
                    "/predict1",
                    payload
                )


            if error:

                st.error(error)

            else:

                raw_crop = data.get(
                    "predict_crop",
                    ""
                )

                crop_name = clean_crop_name(
                    raw_crop
                )

                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-title">
                            🌾 {t("recommended")}
                        </div>
                        <div class="result-value">
                            {crop_name}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# YIELD ESTIMATION
# =========================================================

elif st.session_state.page == "Yield Estimation":

    st.title("📊 " + t("yield"))

    st.write(t("yield_desc"))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            t("crop"),
            placeholder="Rice"
        )

    with col2:

        state = st.text_input(
            t("state"),
            placeholder="Uttar Pradesh"
        )


    season = st.selectbox(
        t("season"),
        [
            "Kharif",
            "Rabi",
            "Whole Year",
            "Summer",
            "Winter"
        ]
    )


    area = st.number_input(
        t("area"),
        min_value=0.01,
        value=1.0,
        step=0.1
    )


    if st.button(
        "📊 " + t("estimate_yield"),
        type="primary",
        use_container_width=True
    ):

        if not crop or not state:

            st.warning(
                "Please enter Crop and State."
            )

        else:

            payload = {

                "Crop": crop.strip(),

                "State": state.strip(),

                "Season": season.strip(),

                "Area": float(area)

            }


            with st.spinner(
                "Estimating yield..."
            ):

                data, error = call_api(
                    "/predict2",
                    payload
                )


            if error:

                st.error(error)

            else:

                raw_value = data.get(
                    "predict_yield",
                    data.get("yield", 0)
                )

                yield_value = extract_number(
                    raw_value
                )


                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-title">
                            📊 {t("yield_result")}
                        </div>
                        <div class="result-value">
                            {yield_value:.2f}
                        </div>
                        <div>
                            {t("yield_unit")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# COST ESTIMATION
# =========================================================

elif st.session_state.page == "Cost Estimation":

    st.title("💰 " + t("cost"))

    st.write(t("cost_desc"))

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            t("crop"),
            placeholder="Rice"
        )

    with col2:

        state = st.text_input(
            t("state"),
            placeholder="Uttar Pradesh"
        )


    yield_value = st.number_input(
        "Yield (Quintal / Hectare)",
        min_value=0.01,
        value=1.0,
        step=0.1
    )


    if st.button(
        "💰 " + t("estimate_cost"),
        type="primary",
        use_container_width=True
    ):

        if not crop or not state:

            st.warning(
                "Please enter Crop and State."
            )

        else:

            payload = {

                "Crop": crop.strip(),

                "State": state.strip(),

                "Yield": float(
                    yield_value
                )

            }


            with st.spinner(
                "Estimating cost..."
            ):

                data, error = call_api(
                    "/predict3",
                    payload
                )


            if error:

                st.error(error)

            else:

                raw_cost = data.get(
                    "predict_cost",
                    data.get("cost", 0)
                )

                cost_value = extract_number(
                    raw_cost
                )


                st.markdown(
                    f"""
                    <div class="result-box">
                        <div class="result-title">
                            💰 {t("cost_result")}
                        </div>
                        <div class="result-value">
                            ₹{cost_value:,.2f}
                        </div>
                        <div>
                            {t("cost_unit")}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# PROFIT ESTIMATION
# =========================================================

elif st.session_state.page == "Profit Estimation":

    st.title("📈 " + t("profit"))

    st.write(
        "This section is independent. "
        "Enter your own values."
        if st.session_state.language == "English"
        else
        "यह सेक्शन स्वतंत्र है। अपनी जानकारी अलग से दर्ज करें।"
    )

    st.divider()


    crop = st.text_input(
        t("crop"),
        placeholder="Rice"
    )


    state = st.text_input(
        t("state"),
        placeholder="Uttar Pradesh"
    )


    profit_yield = st.number_input(
        t("profit_yield"),
        min_value=0.01,
        value=1.0,
        step=0.1
    )


    cultivation_cost = st.number_input(
        t("cultivation_cost"),
        min_value=0.0,
        value=10000.0,
        step=100.0
    )


    selling_price = st.number_input(
        t("selling_price"),
        min_value=0.0,
        value=2500.0,
        step=50.0
    )


    if st.button(
        "📈 " + t("calculate_profit"),
        type="primary",
        use_container_width=True
    ):

        if not crop or not state:

            st.warning(
                "Please enter Crop and State."
            )

        else:

            # For 1 hectare:
            total_revenue = (
                profit_yield *
                selling_price
            )

            profit = (
                total_revenue -
                cultivation_cost
            )


            col1, col2 = st.columns(2)


            with col1:

                st.metric(
                    t("revenue"),
                    f"₹{total_revenue:,.2f}"
                )

                st.caption(
                    t("per_hectare")
                )


            with col2:

                st.metric(
                    t("profit_result"),
                    f"₹{profit:,.2f}"
                )

                st.caption(
                    t("per_hectare")
                )


            if profit >= 0:

                st.success(
                    "Profit is positive."
                    if st.session_state.language == "English"
                    else
                    "लाभ सकारात्मक है।"
                )

            else:

                st.error(
                    "Estimated loss."
                    if st.session_state.language == "English"
                    else
                    "अनुमानित नुकसान।"
                )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.title("ℹ️ " + t("about"))

    st.divider()

    st.subheader("🌾 AgriSense AI")

    st.write(
        """
        AgriSense AI is a smart agriculture application
        that uses Machine Learning to assist farmers.

        The application provides:

        • Crop Suggestion

        • Yield Estimation

        • Cost Estimation

        • Profit Estimation

        • Automatic and Manual Weather support
        """
    )

    st.info(
        "Built with Python, Streamlit, FastAPI and Machine Learning."
    )