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

if "recommended_crop" not in st.session_state:
    st.session_state.recommended_crop = None


# =========================================================
# BASIC STYLE
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
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

    .section-heading {
        color: #185c37;
        font-size: 25px;
        font-weight: 700;
        margin-top: 10px;
    }

    .weather-card {
        padding: 18px;
        border-radius: 14px;
        background: #ffffff;
        border: 1px solid #dcebe1;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(0, 0, 0, 0.04);
    }

    .weather-icon {
        font-size: 25px;
    }

    .weather-label {
        color: #66736b;
        font-size: 13px;
        margin-top: 4px;
    }

    .weather-value {
        color: #14532d;
        font-size: 23px;
        font-weight: 700;
        margin-top: 3px;
    }

    .weather-condition {
        color: #39734a;
        font-size: 14px;
        font-weight: 600;
        margin-top: 3px;
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

        "crop_desc":
            "Get a suitable crop suggestion using soil and weather conditions.",

        "yield_desc":
            "Estimate agricultural yield based on crop, state, season and area.",

        "cost_desc":
            "Estimate cultivation cost per hectare.",

        "profit_desc":
            "Calculate expected revenue and profit.",

        "automatic_weather": "Automatic Weather",
        "manual_weather": "Manual Weather",

        "district": "District",
        "state": "State",
        "city": "City",

        "get_weather": "Get Weather",

        "weather_loaded":
            "Weather loaded successfully.",

        "weather_not_found":
            "Weather not found. Please check District and State.",

        "weather_api_missing":
            "OPENWEATHER_API_KEY is not configured.",

        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "rainfall": "Rainfall (mm)",
        "wind": "Wind Speed",
        "condition": "Condition",

        "rainfall_last_hour":
            "Rainfall (last 1 hour)",

        "soil": "Soil Information",

        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "Soil pH",

        "soil_hint":
            "Enter the available soil nutrient values for better crop suggestion.",

        "get_crop": "Get Crop Suggestion",

        "recommended": "Recommended Crop",
        "crop_suggestion": "Crop Suggestion",

        "weather_mode": "Weather Mode",

        "auto_weather_option":
            "Automatic Weather",

        "manual_weather_option":
            "Manual Weather",

        "weather_required":
            "First enter District and State and click Get Weather.",

        "crop_success":
            "Crop suggestion generated successfully.",

        "season": "Season",
        "area": "Area (Hectare)",

        "estimate_yield": "Estimate Yield",
        "yield_result": "Estimated Yield",
        "yield_unit": "Quintal / Hectare",

        "estimate_cost": "Estimate Cost",
        "cost_result": "Estimated Cultivation Cost",
        "cost_unit": "₹ / Hectare",

        "profit_yield": "Yield (Quintal / Hectare)",
        "cultivation_cost": "Cultivation Cost (₹ / Hectare)",
        "selling_price": "Selling Price (₹ / Quintal)",

        "calculate_profit": "Calculate Profit",

        "revenue": "Total Revenue",
        "profit_result": "Estimated Profit",

        "english": "English",
        "hindi": "हिन्दी",

        "loading_options": "Loading model options...",
        "options_error": "Unable to load model options.",
        "select_crop": "Select Crop",
        "select_state": "Select State",
        "select_season": "Select Season"
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

        "crop_desc":
            "मिट्टी और मौसम की जानकारी के आधार पर उपयुक्त फसल का सुझाव प्राप्त करें।",

        "yield_desc":
            "फसल, राज्य, मौसम और क्षेत्रफल के आधार पर उत्पादन का अनुमान लगाएं।",

        "cost_desc":
            "प्रति हेक्टेयर खेती की लागत का अनुमान लगाएं।",

        "profit_desc":
            "कुल आय और अनुमानित लाभ की गणना करें।",

        "automatic_weather": "स्वचालित मौसम",
        "manual_weather": "मैनुअल मौसम",

        "district": "जिला",
        "state": "राज्य",
        "city": "शहर",

        "get_weather": "मौसम प्राप्त करें",

        "weather_loaded":
            "मौसम की जानकारी सफलतापूर्वक प्राप्त हो गई।",

        "weather_not_found":
            "मौसम की जानकारी नहीं मिली। कृपया जिला और राज्य जांचें।",

        "weather_api_missing":
            "OPENWEATHER_API_KEY कॉन्फ़िगर नहीं है।",

        "temperature": "तापमान (°C)",
        "humidity": "नमी (%)",
        "rainfall": "वर्षा (mm)",
        "wind": "हवा की गति",
        "condition": "मौसम",

        "rainfall_last_hour":
            "वर्षा (पिछले 1 घंटे)",

        "soil": "मिट्टी की जानकारी",

        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "ph": "मिट्टी का pH",

        "soil_hint":
            "बेहतर फसल सुझाव के लिए उपलब्ध मिट्टी के पोषक तत्वों की जानकारी दर्ज करें।",

        "get_crop": "फसल सुझाव प्राप्त करें",

        "recommended": "सुझाई गई फसल",
        "crop_suggestion": "फसल सुझाव",

        "weather_mode": "मौसम मोड",

        "auto_weather_option":
            "स्वचालित मौसम",

        "manual_weather_option":
            "मैनुअल मौसम",

        "weather_required":
            "पहले जिला और राज्य दर्ज करके मौसम प्राप्त करें।",

        "crop_success":
            "फसल सुझाव सफलतापूर्वक प्राप्त हो गया।",

        "season": "मौसम",
        "area": "क्षेत्रफल (हेक्टेयर)",

        "estimate_yield": "उत्पादन अनुमान लगाएं",
        "yield_result": "अनुमानित उत्पादन",
        "yield_unit": "क्विंटल / हेक्टेयर",

        "estimate_cost": "लागत अनुमान लगाएं",
        "cost_result": "अनुमानित खेती लागत",
        "cost_unit": "₹ / हेक्टेयर",

        "profit_yield": "उत्पादन (क्विंटल / हेक्टेयर)",
        "cultivation_cost": "खेती की लागत (₹ / हेक्टेयर)",
        "selling_price": "बिक्री मूल्य (₹ / क्विंटल)",

        "calculate_profit": "लाभ की गणना करें",

        "revenue": "कुल आय",
        "profit_result": "अनुमानित लाभ",

        "english": "English",
        "hindi": "हिन्दी",

        "loading_options": "मॉडल विकल्प लोड हो रहे हैं...",
        "options_error": "मॉडल विकल्प लोड नहीं हो सके।",
        "select_crop": "फसल चुनें",
        "select_state": "राज्य चुनें",
        "select_season": "मौसम चुनें"
    }
}


def t(key):
    return TEXT[
        st.session_state.language
    ].get(key, key)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## 🌾 AgriSense AI")

    st.caption(
        "Smart Agriculture Assistant"
    )

    st.divider()

    if st.button(
        "🏠 " + t("home"),
        use_container_width=True
    ):
        st.session_state.page = "Home"

    if st.button(
        "🌱 " + t("crop"),
        use_container_width=True
    ):
        st.session_state.page = "Crop Suggestion"

    if st.button(
        "📊 " + t("yield"),
        use_container_width=True
    ):
        st.session_state.page = "Yield Estimation"

    if st.button(
        "💰 " + t("cost"),
        use_container_width=True
    ):
        st.session_state.page = "Cost Estimation"

    if st.button(
        "📈 " + t("profit"),
        use_container_width=True
    ):
        st.session_state.page = "Profit Estimation"

    if st.button(
        "ℹ️ " + t("about"),
        use_container_width=True
    ):
        st.session_state.page = "About"

    st.divider()

    st.write("Language")

    language = st.radio(
        "",
        ["English", "Hindi"],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        )
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

        try:

            error_data = response.json()

            detail = error_data.get(
                "detail",
                "Unknown API error"
            )

            return (
                None,
                f"API Error {response.status_code}: {detail}"
            )

        except Exception:

            return (
                None,
                f"API Error {response.status_code}"
            )

    except requests.exceptions.Timeout:

        return (
            None,
            "Request timed out. Please try again."
        )

    except requests.exceptions.ConnectionError:

        return (
            None,
            "FastAPI server is not reachable."
        )

    except Exception as e:

        return None, str(e)


# =========================================================
# OPTIONS HELPER
# =========================================================

@st.cache_data(ttl=300)
def get_options(endpoint):

    try:

        response = requests.get(
            f"{FASTAPI_URL}{endpoint}",
            timeout=30
        )

        if response.status_code == 200:

            return response.json(), None

        try:

            data = response.json()

            detail = data.get(
                "detail",
                "Unable to load options"
            )

            return (
                None,
                f"API Error {response.status_code}: {detail}"
            )

        except Exception:

            return (
                None,
                f"API Error {response.status_code}"
            )

    except requests.exceptions.Timeout:

        return None, "Request timed out."

    except requests.exceptions.ConnectionError:

        return None, "FastAPI server is not reachable."

    except Exception as e:

        return None, str(e)


# =========================================================
# NUMBER EXTRACTOR
# =========================================================

def extract_number(value):

    if isinstance(
        value,
        (int, float)
    ):

        return float(value)

    text = str(value)

    text = text.replace(",", "")

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        text
    )

    if numbers:

        return float(
            numbers[0]
        )

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
        crop.replace(
            "_",
            " "
        ).title()
    )


# =========================================================
# WEATHER ICON
# =========================================================

def get_weather_icon(condition):

    condition = str(
        condition
    ).lower()

    if "clear" in condition:
        return "☀️"

    if "cloud" in condition:
        return "☁️"

    if "rain" in condition:
        return "🌧️"

    if "drizzle" in condition:
        return "🌦️"

    if "thunder" in condition:
        return "⛈️"

    if "snow" in condition:
        return "❄️"

    if (
        "mist" in condition
        or "fog" in condition
        or "haze" in condition
    ):
        return "🌫️"

    return "🌤️"


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        f"""
        <div class="main-title">
            🌾 {t("title")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="sub-title">
            {t("subtitle")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    st.success(
        "Smart farming decisions using Machine Learning and agricultural data."
        if st.session_state.language == "English"
        else
        "मशीन लर्निंग और कृषि डेटा की मदद से बेहतर खेती के निर्णय लें।"
    )

    st.subheader(
        "🌱 " + t("crop")
    )

    st.write(
        t("crop_desc")
    )

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
            "🌱\n\n**"
            + t("crop")
            + "**\n\n"
            + t("crop_desc")
        )

    with col2:

        st.info(
            "📊\n\n**"
            + t("yield")
            + "**\n\n"
            + t("yield_desc")
        )

    with col3:

        st.info(
            "💰\n\n**"
            + t("cost")
            + "**\n\n"
            + t("cost_desc")
        )

    with col4:

        st.info(
            "📈\n\n**"
            + t("profit")
            + "**\n\n"
            + t("profit_desc")
        )


# =========================================================
# CROP SUGGESTION
# =========================================================

elif st.session_state.page == "Crop Suggestion":

    st.title(
        "🌱 " + t("crop_suggestion")
    )

    st.write(
        t("crop_desc")
    )

    st.divider()

    # =====================================================
    # WEATHER
    # =====================================================

    st.markdown(
        f"""
        <div class="section-heading">
            🌦️ {t("automatic_weather")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        "Get current weather for your location."
        if st.session_state.language == "English"
        else
        "अपने स्थान का वर्तमान मौसम प्राप्त करें।"
    )

    col1, col2 = st.columns(2)

    with col1:

        district = st.text_input(
            t("district"),
            value="Prayagraj",
            placeholder="Prayagraj",
            key="weather_district"
        )

    with col2:

        weather_state = st.text_input(
            t("state"),
            value="Uttar Pradesh",
            placeholder="Uttar Pradesh",
            key="weather_state"
        )

    if st.button(
        "🌦️ " + t("get_weather"),
        type="secondary",
        use_container_width=True,
        key="get_weather_button"
    ):

        if (
            not district.strip()
            or not weather_state.strip()
        ):

            st.warning(
                "Please enter District and State."
                if st.session_state.language == "English"
                else
                "कृपया जिला और राज्य दर्ज करें।"
            )

        elif not OPENWEATHER_API_KEY:

            st.error(
                t("weather_api_missing")
            )

        else:

            try:

                query = (
                    f"{district.strip()}, "
                    f"{weather_state.strip()}, India"
                )

                weather_url = (
                    "https://api.openweathermap.org/data/2.5/weather"
                )

                params = {
                    "q": query,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric"
                }

                weather_response = requests.get(
                    weather_url,
                    params=params,
                    timeout=30
                )

                if weather_response.status_code == 200:

                    weather_json = weather_response.json()

                    st.session_state.weather_data = {
                        "temperature":
                            weather_json["main"]["temp"],

                        "humidity":
                            weather_json["main"]["humidity"],

                        "rainfall":
                            weather_json.get(
                                "rain",
                                {}
                            ).get(
                                "1h",
                                0.0
                            ),

                        "wind":
                            weather_json.get(
                                "wind",
                                {}
                            ).get(
                                "speed",
                                0.0
                            ),

                        "condition":
                            weather_json.get(
                                "weather",
                                [{}]
                            )[0].get(
                                "description",
                                "Unknown"
                            )
                    }

                    st.success(
                        t("weather_loaded")
                    )

                else:

                    st.session_state.weather_data = None

                    st.error(
                        t("weather_not_found")
                    )

            except Exception as e:

                st.session_state.weather_data = None

                st.error(
                    f"Weather Error: {e}"
                )

    # =====================================================
    # WEATHER DISPLAY
    # =====================================================

    if st.session_state.weather_data:

        weather = st.session_state.weather_data

        st.write("")

        w1, w2, w3, w4 = st.columns(4)

        with w1:

            st.metric(
                "🌡️ " + t("temperature"),
                f'{weather["temperature"]:.1f} °C'
            )

        with w2:

            st.metric(
                "💧 " + t("humidity"),
                f'{weather["humidity"]:.0f} %'
            )

        with w3:

            st.metric(
                "🌧️ " + t("rainfall_last_hour"),
                f'{weather["rainfall"]:.1f} mm'
            )

        with w4:

            icon = get_weather_icon(
                weather["condition"]
            )

            st.metric(
                f"{icon} " + t("condition"),
                str(
                    weather["condition"]
                ).title()
            )

    # =====================================================
    # MANUAL WEATHER
    # =====================================================

    st.divider()

    weather_mode = st.radio(
        t("weather_mode"),
        [
            t("auto_weather_option"),
            t("manual_weather_option")
        ],
        horizontal=True
    )

    # =====================================================
    # WEATHER VALUES
    # =====================================================

    if weather_mode == t("manual_weather_option"):

        st.markdown(
            f"""
            <div class="section-heading">
                🌦️ {t("manual_weather")}
            </div>
            """,
            unsafe_allow_html=True
        )

        m1, m2, m3 = st.columns(3)

        with m1:

            temperature = st.number_input(
                t("temperature"),
                value=25.0,
                step=0.1
            )

        with m2:

            humidity = st.number_input(
                t("humidity"),
                value=60.0,
                step=1.0
            )

        with m3:

            rainfall = st.number_input(
                t("rainfall"),
                value=100.0,
                step=1.0
            )

    else:

        if st.session_state.weather_data:

            temperature = float(
                st.session_state.weather_data[
                    "temperature"
                ]
            )

            humidity = float(
                st.session_state.weather_data[
                    "humidity"
                ]
            )

            rainfall = float(
                st.session_state.weather_data[
                    "rainfall"
                ]
            )

        else:

            temperature = 25.0
            humidity = 60.0
            rainfall = 100.0

    # =====================================================
    # SOIL
    # =====================================================

    st.divider()

    st.markdown(
        f"""
        <div class="section-heading">
            🌱 {t("soil")}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption(
        t("soil_hint")
    )

    s1, s2, s3, s4 = st.columns(4)

    with s1:

        nitrogen = st.number_input(
            t("nitrogen"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with s2:

        phosphorus = st.number_input(
            t("phosphorus"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with s3:

        potassium = st.number_input(
            t("potassium"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with s4:

        ph_value = st.number_input(
            t("ph"),
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )

    st.write("")

    # =====================================================
    # CROP BUTTON
    # =====================================================

    if st.button(
        "🌱 " + t("get_crop"),
        type="primary",
        use_container_width=True,
        key="crop_prediction_button"
    ):

        payload = {

            "N": float(nitrogen),

            "P": float(phosphorus),

            "K": float(potassium),

            "temperature":
                float(temperature),

            "humidity":
                float(humidity),

            "ph":
                float(ph_value),

            "rainfall":
                float(rainfall)
        }

        data, error = call_api(
            "/predict1",
            payload
        )

        if error:

            st.error(error)

        elif data:

            raw_crop = data.get(
                "predicted_crop",
                ""
            )

            crop_name = clean_crop_name(
                raw_crop
            )

            st.session_state.recommended_crop = crop_name

            st.success(
                t("crop_success")
            )

            # =================================================
            # SIMPLE OUTPUT - NO DIV / NO HTML
            # =================================================

            st.markdown(
                f"## 🌾 {crop_name}"
            )

            st.caption(
                "Based on the provided soil and weather conditions."
            )


# =========================================================
# YIELD ESTIMATION
# =========================================================

elif st.session_state.page == "Yield Estimation":

    st.title(
        "📊 " + t("yield")
    )

    st.write(
        t("yield_desc")
    )

    st.divider()

    options, options_error = get_options(
        "/yield-options"
    )

    if options_error:

        st.error(options_error)

    elif options:

        crops = options.get(
            "crops",
            []
        )

        states = options.get(
            "states",
            []
        )

        seasons = options.get(
            "seasons",
            []
        )

        if (
            not crops
            or not states
            or not seasons
        ):

            st.warning(
                t("options_error")
            )

        else:

            c1, c2, c3, c4 = st.columns(4)

            with c1:

                selected_crop = st.selectbox(
                    "🌱 " + t("crop"),
                    crops
                )

            with c2:

                selected_state = st.selectbox(
                    "📍 " + t("state"),
                    states
                )

            with c3:

                selected_season = st.selectbox(
                    "🌤️ " + t("season"),
                    seasons
                )

            with c4:

                area = st.number_input(
                    "📐 " + t("area"),
                    min_value=0.01,
                    value=1.0,
                    step=0.1
                )

            st.write("")

            if st.button(
                "📊 " + t("estimate_yield"),
                type="primary",
                use_container_width=True,
                key="yield_button"
            ):

                payload = {

                    "Crop":
                        selected_crop,

                    "State":
                        selected_state,

                    "Season":
                        selected_season,

                    "Area":
                        float(area)
                }

                data, error = call_api(
                    "/predict2",
                    payload
                )

                if error:

                    st.error(error)

                elif data:

                    yield_value = extract_number(
                        data.get(
                            "predicted_yield",
                            0
                        )
                    )

                    st.success(
                        "Yield estimation generated successfully."
                        if st.session_state.language == "English"
                        else
                        "उत्पादन अनुमान सफलतापूर्वक प्राप्त हो गया।"
                    )

                    # =================================================
                    # SIMPLE YIELD OUTPUT
                    # =================================================

                    st.metric(
                        label="📊 " + t("yield_result"),
                        value=f"{yield_value:.2f}",
                        delta=t("yield_unit")
                    )


# =========================================================
# COST ESTIMATION
# =========================================================

elif st.session_state.page == "Cost Estimation":

    st.title(
        "💰 " + t("cost")
    )

    st.write(
        t("cost_desc")
    )

    st.divider()

    options, options_error = get_options(
        "/cost-options"
    )

    if options_error:

        st.error(options_error)

    elif options:

        crops = options.get(
            "crops",
            []
        )

        states = options.get(
            "states",
            []
        )

        if not crops or not states:

            st.warning(
                t("options_error")
            )

        else:

            c1, c2, c3 = st.columns(3)

            with c1:

                selected_crop = st.selectbox(
                    "🌱 " + t("crop"),
                    crops
                )

            with c2:

                selected_state = st.selectbox(
                    "📍 " + t("state"),
                    states
                )

            with c3:

                yield_input = st.number_input(
                    "🌾 Yield (Quintal / Hectare)",
                    min_value=0.0,
                    value=5.0,
                    step=0.1
                )

            st.write("")

            if st.button(
                "💰 " + t("estimate_cost"),
                type="primary",
                use_container_width=True,
                key="cost_button"
            ):

                payload = {

                    "Crop":
                        selected_crop,

                    "State":
                        selected_state,

                    "Yield":
                        float(yield_input)
                }

                data, error = call_api(
                    "/predict3",
                    payload
                )

                if error:

                    st.error(error)

                elif data:

                    cost_value = extract_number(
                        data.get(
                            "predicted_cost",
                            0
                        )
                    )

                    st.success(
                        "Cost estimation generated successfully."
                        if st.session_state.language == "English"
                        else
                        "लागत अनुमान सफलतापूर्वक प्राप्त हो गया।"
                    )

                    # =================================================
                    # SIMPLE COST OUTPUT
                    # =================================================

                    st.metric(
                        label="💰 " + t("cost_result"),
                        value=f"₹ {cost_value:,.2f}",
                        delta=t("cost_unit")
                    )


# =========================================================
# PROFIT ESTIMATION
# =========================================================

elif st.session_state.page == "Profit Estimation":

    st.title(
        "📈 " + t("profit")
    )

    st.write(
        t("profit_desc")
    )

    st.divider()

    p1, p2, p3 = st.columns(3)

    with p1:

        profit_yield = st.number_input(
            t("profit_yield"),
            min_value=0.0,
            value=5.0,
            step=0.1
        )

    with p2:

        cultivation_cost = st.number_input(
            t("cultivation_cost"),
            min_value=0.0,
            value=10000.0,
            step=100.0
        )

    with p3:

        selling_price = st.number_input(
            t("selling_price"),
            min_value=0.0,
            value=2500.0,
            step=50.0
        )

    st.write("")

    if st.button(
        "📈 " + t("calculate_profit"),
        type="primary",
        use_container_width=True,
        key="profit_button"
    ):

        revenue = (
            profit_yield
            * selling_price
        )

        profit = (
            revenue
            - cultivation_cost
        )

        st.success(
            "Profit estimation calculated successfully."
            if st.session_state.language == "English"
            else
            "लाभ अनुमान सफलतापूर्वक प्राप्त हो गया।"
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                label="💵 " + t("revenue"),
                value=f"₹ {revenue:,.2f}"
            )

        with col2:

            st.metric(
                label="📈 " + t("profit_result"),
                value=f"₹ {profit:,.2f}"
            )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.title(
        "ℹ️ " + t("about")
    )

    st.write("")

    if st.session_state.language == "English":

        st.markdown(
            """
            ### 🌾 AgriSense AI

            AgriSense AI is a smart agriculture assistant
            designed to support farmers using Machine Learning
            and agricultural data.

            ### Features

            - 🌱 Crop Suggestion
            - 📊 Yield Estimation
            - 💰 Cost Estimation
            - 📈 Profit Estimation
            - 🌦️ Weather-based crop assistance

            The system uses trained Machine Learning models
            through a FastAPI backend and provides an easy-to-use
            Streamlit interface.
            """
        )

    else:

        st.markdown(
            """
            ### 🌾 AgriSense AI

            AgriSense AI एक स्मार्ट कृषि सहायक है जो
            मशीन लर्निंग और कृषि डेटा की मदद से किसानों
            को बेहतर निर्णय लेने में सहायता करता है।

            ### सुविधाएँ

            - 🌱 फसल सुझाव
            - 📊 उत्पादन अनुमान
            - 💰 लागत अनुमान
            - 📈 लाभ अनुमान
            - 🌦️ मौसम आधारित कृषि सहायता

            यह सिस्टम FastAPI backend और Streamlit interface
            के माध्यम से Machine Learning models का उपयोग करता है।
            """
        )