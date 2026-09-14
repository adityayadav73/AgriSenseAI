# ============================================================
# AgriSense AI - Streamlit Frontend
# ============================================================

import os
import re
import requests
import streamlit as st


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CONFIGURATION
# ============================================================

API_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-n621.onrender.com"
).rstrip("/")

OPENWEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY",
    ""
)

OPENWEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)

IP_LOCATION_URL = "https://ipapi.co/json/"


# ============================================================
# LANGUAGE TEXT
# ============================================================

TEXT = {
    "English": {

        "app_title": "🌱 AgriSense AI",
        "tagline": "Smart Farming Decision Support System",

        "home": "🏠 Home",
        "weather": "🌦️ Weather",
        "crop": "🌾 Crop Suggestion",
        "yield": "📊 Yield Estimate",
        "cost": "💰 Cost Estimate",
        "profit": "📈 Profit Estimate",
        "about": "ℹ️ About",

        "language": "Language",

        "welcome": "Welcome to AgriSense AI",

        "home_desc": (
            "An AI-powered agriculture decision support system "
            "for crop selection, yield estimation, cultivation "
            "cost estimation and profit analysis."
        ),

        "features": "Key Features",

        "weather_title": "🌦️ Weather Information",
        "weather_mode": "Weather Mode",
        "automatic": "Automatic Weather",
        "manual": "Manual City",

        "detecting": "Detecting approximate location...",
        "location_detected": "Detected Location",
        "city": "City",
        "get_weather": "Get Weather",

        "temperature": "Temperature",
        "humidity": "Humidity",
        "rainfall": "Rainfall",
        "wind": "Wind Speed",

        "api_key_missing": (
            "OpenWeather API key is not configured. "
            "Please add OPENWEATHER_API_KEY in Render."
        ),

        "weather_success": (
            "Weather data loaded successfully."
        ),

        "weather_failed": (
            "Unable to get weather data."
        ),

        "crop_title": "🌾 Crop Suggestion",

        "crop_desc": (
            "Enter soil and weather conditions "
            "to get a suitable crop suggestion."
        ),

        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "Soil pH",
        "temperature_input": "Temperature (°C)",
        "humidity_input": "Humidity (%)",
        "rainfall_input": "Rainfall (mm)",

        "suggest_crop": "🌱 Suggest Crop",

        "crop_result": "फसल सुझाव",

        "recommended_crop": "Recommended Crop",

        "yield_title": "📊 Yield Estimate",

        "yield_desc": (
            "Estimate expected crop yield using "
            "crop, state, season and area."
        ),

        "crop_name": "Crop",
        "state": "State",
        "season": "Season",
        "area": "Area (Hectare)",

        "area_help": (
            "Enter farm area in Hectare."
        ),

        "estimate_yield": "📊 Estimate Yield",

        "yield_result": "Estimated Yield",

        "yield_unit": "Quintal/Hectare",

        "cost_title": "💰 Cost Estimate",

        "cost_desc": (
            "Estimate cultivation cost for one hectare "
            "using crop, state and yield."
        ),

        "yield_input": "Yield (Quintal/Hectare)",

        "yield_help": (
            "Enter yield in Quintal/Hectare."
        ),

        "estimate_cost": "💰 Estimate Cost",

        "cost_result": "Estimated Cultivation Cost",

        "cost_unit": "₹/Hectare",

        "profit_title": "📈 Profit Estimate",

        "profit_desc": (
            "Calculate expected revenue and profit "
            "for one hectare."
        ),

        "cultivation_cost": (
            "Cultivation Cost (₹/Hectare)"
        ),

        "selling_price": (
            "Selling Price (₹/Quintal)"
        ),

        "selling_price_help": (
            "Enter the current selling price "
            "for 1 Quintal."
        ),

        "calculate_profit": (
            "📈 Calculate Profit"
        ),

        "total_revenue": "Total Revenue",

        "profit": "Profit",

        "loss": "Loss",

        "revenue_formula": (
            "Revenue = Yield × Selling Price"
        ),

        "profit_formula": (
            "Profit = Revenue − Cultivation Cost"
        ),

        "positive_profit": "✅ Expected Profit",

        "negative_profit": "⚠️ Expected Loss",

        "about_title": "ℹ️ About AgriSense AI",

        "about_text": (
            "AgriSense AI is a smart farming decision "
            "support application that combines machine "
            "learning and weather information to assist "
            "farmers in making better agricultural decisions."
        ),

        "backend": "Backend API",

        "status": "System Status",

        "api_success": (
            "Backend connected successfully."
        ),

        "api_error": (
            "Backend connection failed."
        ),

        "required_fields": (
            "Please fill all required fields."
        ),
    },

    "Hindi": {

        "app_title": "🌱 AgriSense AI",

        "tagline": (
            "स्मार्ट कृषि निर्णय सहायता प्रणाली"
        ),

        "home": "🏠 होम",

        "weather": "🌦️ मौसम",

        "crop": "🌾 फसल सुझाव",

        "yield": "📊 उत्पादन अनुमान",

        "cost": "💰 लागत अनुमान",

        "profit": "📈 लाभ अनुमान",

        "about": "ℹ️ हमारे बारे में",

        "language": "भाषा",

        "welcome": (
            "AgriSense AI में आपका स्वागत है"
        ),

        "home_desc": (
            "फसल चयन, उत्पादन, खेती की लागत और लाभ "
            "का अनुमान लगाने के लिए AI आधारित "
            "कृषि निर्णय सहायता प्रणाली।"
        ),

        "features": "मुख्य सुविधाएँ",

        "weather_title": "🌦️ मौसम की जानकारी",

        "weather_mode": "मौसम का तरीका",

        "automatic": "स्वचालित मौसम",

        "manual": "शहर चुनें",

        "detecting": (
            "अनुमानित स्थान खोजा जा रहा है..."
        ),

        "location_detected": "पता चला स्थान",

        "city": "शहर",

        "get_weather": "मौसम प्राप्त करें",

        "temperature": "तापमान",

        "humidity": "नमी",

        "rainfall": "वर्षा",

        "wind": "हवा की गति",

        "api_key_missing": (
            "OpenWeather API key सेट नहीं है। "
            "Render में OPENWEATHER_API_KEY जोड़ें।"
        ),

        "weather_success": (
            "मौसम की जानकारी सफलतापूर्वक प्राप्त हुई।"
        ),

        "weather_failed": (
            "मौसम की जानकारी प्राप्त नहीं हो सकी।"
        ),

        "crop_title": "🌾 फसल सुझाव",

        "crop_desc": (
            "मिट्टी और मौसम की जानकारी दर्ज करके "
            "उपयुक्त फसल का सुझाव प्राप्त करें।"
        ),

        "nitrogen": "नाइट्रोजन (N)",

        "phosphorus": "फॉस्फोरस (P)",

        "potassium": "पोटैशियम (K)",

        "ph": "मिट्टी का pH",

        "temperature_input": "तापमान (°C)",

        "humidity_input": "नमी (%)",

        "rainfall_input": "वर्षा (mm)",

        "suggest_crop": (
            "🌱 फसल सुझाव प्राप्त करें"
        ),

        "crop_result": "फसल सुझाव",

        "recommended_crop": (
            "अनुशंसित फसल"
        ),

        "yield_title": "📊 उत्पादन अनुमान",

        "yield_desc": (
            "फसल, राज्य, मौसम और क्षेत्रफल के आधार पर "
            "संभावित उत्पादन का अनुमान लगाएँ।"
        ),

        "crop_name": "फसल",

        "state": "राज्य",

        "season": "मौसम/सीजन",

        "area": "क्षेत्रफल (हेक्टेयर)",

        "area_help": (
            "क्षेत्रफल हेक्टेयर में दर्ज करें।"
        ),

        "estimate_yield": (
            "📊 उत्पादन का अनुमान"
        ),

        "yield_result": (
            "अनुमानित उत्पादन"
        ),

        "yield_unit": (
            "क्विंटल/हेक्टेयर"
        ),

        "cost_title": "💰 लागत अनुमान",

        "cost_desc": (
            "फसल, राज्य और उत्पादन के आधार पर "
            "एक हेक्टेयर की खेती की लागत का अनुमान लगाएँ।"
        ),

        "yield_input": (
            "उत्पादन (क्विंटल/हेक्टेयर)"
        ),

        "yield_help": (
            "उत्पादन क्विंटल/हेक्टेयर में दर्ज करें।"
        ),

        "estimate_cost": (
            "💰 लागत का अनुमान"
        ),

        "cost_result": (
            "अनुमानित खेती की लागत"
        ),

        "cost_unit": (
            "₹/हेक्टेयर"
        ),

        "profit_title": "📈 लाभ अनुमान",

        "profit_desc": (
            "एक हेक्टेयर के लिए अनुमानित आय "
            "और लाभ की गणना करें।"
        ),

        "cultivation_cost": (
            "खेती की लागत (₹/हेक्टेयर)"
        ),

        "selling_price": (
            "बिक्री मूल्य (₹/क्विंटल)"
        ),

        "selling_price_help": (
            "1 क्विंटल की वर्तमान बिक्री कीमत दर्ज करें।"
        ),

        "calculate_profit": (
            "📈 लाभ की गणना करें"
        ),

        "total_revenue": "कुल आय",

        "profit": "लाभ",

        "loss": "नुकसान",

        "revenue_formula": (
            "आय = उत्पादन × बिक्री मूल्य"
        ),

        "profit_formula": (
            "लाभ = आय − खेती की लागत"
        ),

        "positive_profit": (
            "✅ अनुमानित लाभ"
        ),

        "negative_profit": (
            "⚠️ अनुमानित नुकसान"
        ),

        "about_title": (
            "ℹ️ AgriSense AI के बारे में"
        ),

        "about_text": (
            "AgriSense AI एक स्मार्ट कृषि निर्णय "
            "सहायता एप्लिकेशन है जो मशीन लर्निंग और "
            "मौसम की जानकारी का उपयोग करके किसानों "
            "को बेहतर कृषि निर्णय लेने में सहायता करता है।"
        ),

        "backend": "Backend API",

        "status": "सिस्टम स्थिति",

        "api_success": (
            "Backend सफलतापूर्वक जुड़ा हुआ है।"
        ),

        "api_error": (
            "Backend से कनेक्शन नहीं हो पाया।"
        ),

        "required_fields": (
            "कृपया सभी जरूरी जानकारी भरें।"
        ),
    }
}


# ============================================================
# LANGUAGE STATE
# ============================================================

if "language" not in st.session_state:
    st.session_state.language = "English"


def t(key):
    return TEXT[
        st.session_state.language
    ].get(key, key)


# ============================================================
# CROP CLEANING
# ============================================================

def clean_crop_name(value):

    if value is None:
        return "Unknown Crop"

    text = str(value).strip()

    text = re.sub(
        r"recommended\s*crop\s*(is|:)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = re.sub(
        r"predict\s*crop\s*(is|:)?",
        "",
        text,
        flags=re.IGNORECASE
    )

    text = text.strip()

    crop_map = {

        "ispigeonpeas": "Pigeon Peas",
        "pigeonpeas": "Pigeon Peas",
        "pigeon peas": "Pigeon Peas",

        "rice": "Rice",

        "maize": "Maize",

        "wheat": "Wheat",

        "cotton": "Cotton",

        "sugarcane": "Sugarcane",

        "banana": "Banana",

        "mango": "Mango",

        "apple": "Apple",

        "grapes": "Grapes",

        "orange": "Orange",

        "papaya": "Papaya",

        "watermelon": "Watermelon",

        "muskmelon": "Muskmelon",

        "chickpea": "Chickpea",

        "kidneybeans": "Kidney Beans",

        "kidney beans": "Kidney Beans",

        "blackgram": "Black Gram",

        "black gram": "Black Gram",

        "lentil": "Lentil",

        "mothbeans": "Moth Beans",

        "mungbean": "Mung Bean",

        "coffee": "Coffee",

        "coconut": "Coconut",

        "jute": "Jute",
    }

    key = text.lower().strip()

    if key in crop_map:
        return crop_map[key]

    normalized = re.sub(
        r"[^a-z]",
        "",
        key
    )

    for name, clean_name in crop_map.items():

        normalized_name = re.sub(
            r"[^a-z]",
            "",
            name
        )

        if normalized == normalized_name:
            return clean_name

    return text


# ============================================================
# HINDI CROP NAMES
# ============================================================

def crop_hindi_name(crop):

    mapping = {

        "Pigeon Peas": "अरहर",

        "Rice": "धान",

        "Maize": "मक्का",

        "Wheat": "गेहूँ",

        "Cotton": "कपास",

        "Sugarcane": "गन्ना",

        "Banana": "केला",

        "Mango": "आम",

        "Apple": "सेब",

        "Grapes": "अंगूर",

        "Orange": "संतरा",

        "Papaya": "पपीता",

        "Watermelon": "तरबूज",

        "Muskmelon": "खरबूजा",

        "Chickpea": "चना",

        "Kidney Beans": "राजमा",

        "Black Gram": "उड़द",

        "Lentil": "मसूर",

        "Moth Beans": "मोठ",

        "Mung Bean": "मूंग",

        "Coffee": "कॉफी",

        "Coconut": "नारियल",

        "Jute": "जूट",
    }

    return mapping.get(
        crop,
        crop
    )


# ============================================================
# NUMBER EXTRACTION
# ============================================================

def extract_number(value):

    if value is None:
        return None

    matches = re.findall(
        r"-?\d+(?:\.\d+)?",
        str(value)
    )

    if not matches:
        return None

    try:
        return float(matches[-1])
    except Exception:
        return None


# ============================================================
# FASTAPI POST
# ============================================================

def post_to_api(endpoint, payload):

    url = f"{API_URL}{endpoint}"

    try:

        response = requests.post(
            url,
            json=payload,
            timeout=60
        )

        if response.status_code == 200:

            try:
                return response.json(), None

            except Exception:

                return {
                    "result": response.text
                }, None

        if response.status_code == 429:

            return None, (
                "API rate limit (429). "
                "Please wait and try again."
            )

        return None, (
            f"API Error: HTTP "
            f"{response.status_code}"
        )

    except requests.exceptions.Timeout:

        return None, (
            "Backend request timed out."
        )

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to FastAPI backend."
        )

    except Exception as e:

        return None, str(e)


# ============================================================
# WEATHER
# ============================================================

def get_weather(city):

    if not OPENWEATHER_API_KEY:

        return None, "API_KEY_MISSING"

    try:

        params = {
            "q": city,
            "appid": OPENWEATHER_API_KEY,
            "units": "metric"
        }

        response = requests.get(
            OPENWEATHER_URL,
            params=params,
            timeout=20
        )

        if response.status_code != 200:

            return None, (
                f"Weather API Error: "
                f"HTTP {response.status_code}"
            )

        data = response.json()

        weather = {

            "city": data.get(
                "name",
                city
            ),

            "country": data.get(
                "sys",
                {}
            ).get(
                "country",
                ""
            ),

            "temperature": data.get(
                "main",
                {}
            ).get(
                "temp"
            ),

            "humidity": data.get(
                "main",
                {}
            ).get(
                "humidity"
            ),

            "wind": data.get(
                "wind",
                {}
            ).get(
                "speed"
            ),

            "rainfall": (
                data.get(
                    "rain",
                    {}
                ).get(
                    "1h",
                    0
                )
                if data.get("rain")
                else 0
            ),

            "description": (
                data.get(
                    "weather",
                    [{}]
                )[0].get(
                    "description",
                    ""
                )
            )
        }

        return weather, None

    except requests.exceptions.Timeout:

        return None, (
            "Weather request timed out."
        )

    except Exception as e:

        return None, str(e)


# ============================================================
# AUTOMATIC LOCATION
# ============================================================

def get_ip_location():

    try:

        response = requests.get(
            IP_LOCATION_URL,
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        city = data.get("city")

        if not city:
            return None

        return {

            "city": city,

            "region": data.get(
                "region",
                ""
            ),

            "country": data.get(
                "country_name",
                ""
            )
        }

    except Exception:

        return None


# ============================================================
# WEATHER DISPLAY
# ============================================================

def show_weather_cards(weather):

    if not weather:
        return

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            t("temperature"),
            f"{weather['temperature']} °C"
        )

    with col2:

        st.metric(
            t("humidity"),
            f"{weather['humidity']} %"
        )

    with col3:

        st.metric(
            t("rainfall"),
            f"{weather['rainfall']} mm"
        )

    with col4:

        st.metric(
            t("wind"),
            f"{weather['wind']} m/s"
        )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🌱 AgriSense AI")

    selected_language = st.selectbox(
        t("language"),
        [
            "English",
            "Hindi"
        ],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        )
    )

    st.session_state.language = (
        selected_language
    )

    st.divider()

    page = st.radio(
        "Menu",
        [
            t("home"),
            t("weather"),
            t("crop"),
            t("yield"),
            t("cost"),
            t("profit"),
            t("about")
        ]
    )

    st.divider()

    st.caption(
        "AgriSense AI"
    )

    st.caption(
        "Smart Farming 🌱"
    )


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    t("app_title")
)

st.caption(
    t("tagline")
)

st.divider()


# ============================================================
# HOME
# ============================================================

if page == t("home"):

    st.header(
        t("welcome")
    )

    st.write(
        t("home_desc")
    )

    st.divider()

    st.subheader(
        t("features")
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.info(
            "🌦️ Weather\n\n"
            "Automatic + Manual weather"
        )

        st.success(
            "🌾 Crop Suggestion\n\n"
            "Suitable crop recommendation"
        )

    with col2:

        st.info(
            "📊 Yield Estimate\n\n"
            "Quintal/Hectare"
        )

        st.success(
            "💰 Cost Estimate\n\n"
            "₹/Hectare"
        )

    with col3:

        st.info(
            "📈 Profit Estimate\n\n"
            "Revenue, profit and loss"
        )

        st.success(
            "🇬🇧 / 🇮🇳 Language\n\n"
            "English and Hindi"
        )

    st.divider()

    st.subheader(
        "🚀 System Information"
    )

    st.write(
        f"**FastAPI Backend:** `{API_URL}`"
    )

    st.write(
        "**Frontend:** Streamlit"
    )


# ============================================================
# WEATHER
# ============================================================

elif page == t("weather"):

    st.header(
        t("weather_title")
    )

    mode = st.radio(
        t("weather_mode"),
        [
            t("automatic"),
            t("manual")
        ],
        horizontal=True
    )

    # --------------------------------------------------------
    # AUTOMATIC WEATHER
    # --------------------------------------------------------

    if mode == t("automatic"):

        st.info(
            "Automatic location uses approximate "
            "IP-based location."
            if st.session_state.language == "English"
            else
            "स्वचालित स्थान अनुमानित IP location "
            "का उपयोग करता है।"
        )

        if st.button(
            "📍 Detect Location & Get Weather",
            use_container_width=True
        ):

            with st.spinner(
                t("detecting")
            ):

                location = (
                    get_ip_location()
                )

            if location:

                st.success(
                    f"{t('location_detected')}: "
                    f"{location['city']}"
                )

                weather, error = (
                    get_weather(
                        location["city"]
                    )
                )

                if weather:

                    st.success(
                        t("weather_success")
                    )

                    st.subheader(
                        f"📍 {weather['city']}, "
                        f"{weather['country']}"
                    )

                    if weather["description"]:

                        st.caption(
                            weather[
                                "description"
                            ].title()
                        )

                    show_weather_cards(
                        weather
                    )

                else:

                    if error == "API_KEY_MISSING":

                        st.error(
                            t("api_key_missing")
                        )

                    else:

                        st.error(
                            f"{t('weather_failed')} "
                            f"{error}"
                        )

            else:

                st.error(
                    "Automatic location failed. "
                    "Please use Manual City."
                    if st.session_state.language == "English"
                    else
                    "स्वचालित स्थान नहीं मिल सका। "
                    "Manual City का उपयोग करें।"
                )

    # --------------------------------------------------------
    # MANUAL WEATHER
    # --------------------------------------------------------

    else:

        city = st.text_input(
            t("city"),
            placeholder=(
                "e.g. Prayagraj"
                if st.session_state.language == "English"
                else
                "जैसे प्रयागराज"
            )
        )

        if st.button(
            "🌦️ " + t("get_weather"),
            use_container_width=True
        ):

            if not city.strip():

                st.warning(
                    t("required_fields")
                )

            else:

                with st.spinner(
                    "Getting weather..."
                    if st.session_state.language == "English"
                    else
                    "मौसम की जानकारी प्राप्त की जा रही है..."
                ):

                    weather, error = (
                        get_weather(
                            city.strip()
                        )
                    )

                if weather:

                    st.success(
                        t("weather_success")
                    )

                    st.subheader(
                        f"📍 {weather['city']}, "
                        f"{weather['country']}"
                    )

                    if weather["description"]:

                        st.caption(
                            weather[
                                "description"
                            ].title()
                        )

                    show_weather_cards(
                        weather
                    )

                else:

                    if error == "API_KEY_MISSING":

                        st.error(
                            t("api_key_missing")
                        )

                    else:

                        st.error(
                            f"{t('weather_failed')} "
                            f"{error}"
                        )


# ============================================================
# CROP SUGGESTION
# ============================================================

elif page == t("crop"):

    st.header(
        t("crop_title")
    )

    st.write(
        t("crop_desc")
    )

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:

        nitrogen = st.number_input(
            t("nitrogen"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

        phosphorus = st.number_input(
            t("phosphorus"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

        potassium = st.number_input(
            t("potassium"),
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with col2:

        temperature = st.number_input(
            t("temperature_input"),
            value=25.0,
            step=0.1
        )

        humidity = st.number_input(
            t("humidity_input"),
            min_value=0.0,
            max_value=100.0,
            value=60.0,
            step=1.0
        )

    with col3:

        ph_value = st.number_input(
            t("ph"),
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )

        rainfall = st.number_input(
            t("rainfall_input"),
            min_value=0.0,
            value=100.0,
            step=1.0
        )

    st.divider()

    if st.button(
        t("suggest_crop"),
        type="primary",
        use_container_width=True
    ):

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

            "ph": float(
                ph_value
            ),

            "rainfall": float(
                rainfall
            )
        }

        with st.spinner(
            "Getting crop suggestion..."
            if st.session_state.language == "English"
            else
            "फसल सुझाव प्राप्त किया जा रहा है..."
        ):

            result, error = post_to_api(
                "/predict1",
                payload
            )

        if result:

            raw_crop = (

                result.get(
                    "predict_crop"
                )

                or result.get(
                    "crop"
                )

                or result.get(
                    "prediction"
                )

                or result.get(
                    "result"
                )
            )

            crop_name = (
                clean_crop_name(
                    raw_crop
                )
            )

            st.success(
                t("crop_result")
            )

            if (
                st.session_state.language
                == "Hindi"
            ):

                st.subheader(
                    f"🌾 "
                    f"{crop_hindi_name(crop_name)}"
                )

                st.caption(
                    f"English: {crop_name}"
                )

            else:

                st.subheader(
                    f"🌾 {crop_name}"
                )

        else:

            st.error(
                f"{t('api_error')} {error}"
            )


# ============================================================
# YIELD ESTIMATE
# ============================================================

elif page == t("yield"):

    st.header(
        t("yield_title")
    )

    st.write(
        t("yield_desc")
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        crop = st.text_input(
            t("crop_name"),
            placeholder=(
                "e.g. Rice"
                if st.session_state.language == "English"
                else
                "जैसे धान"
            )
        )

        state = st.text_input(
            t("state"),
            placeholder=(
                "e.g. Uttar Pradesh"
                if st.session_state.language == "English"
                else
                "जैसे उत्तर प्रदेश"
            )
        )

    with col2:

        season = st.text_input(
            t("season"),
            placeholder=(
                "e.g. Kharif"
                if st.session_state.language == "English"
                else
                "जैसे खरीफ"
            )
        )

        area = st.number_input(
            t("area"),
            min_value=0.01,
            value=1.0,
            step=0.1,
            help=t("area_help")
        )

    st.info(
        "📌 Area must be entered in Hectare."
        if st.session_state.language == "English"
        else
        "📌 क्षेत्रफल हेक्टेयर में ही दर्ज करें।"
    )

    st.divider()

    if st.button(
        t("estimate_yield"),
        type="primary",
        use_container_width=True
    ):

        if (
            not crop.strip()
            or not state.strip()
            or not season.strip()
        ):

            st.warning(
                t("required_fields")
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
                if st.session_state.language == "English"
                else
                "उत्पादन का अनुमान लगाया जा रहा है..."
            ):

                result, error = post_to_api(
                    "/predict2",
                    payload
                )

            if result:

                raw_yield = (

                    result.get(
                        "predict_yield"
                    )

                    or result.get(
                        "yield"
                    )

                    or result.get(
                        "predicted_yield"
                    )

                    or result.get(
                        "prediction"
                    )

                    or result.get(
                        "result"
                    )
                )

                estimated_yield = (
                    extract_number(
                        raw_yield
                    )
                )

                if estimated_yield is not None:

                    st.success(
                        t("yield_result")
                    )

                    st.metric(
                        t("yield_result"),
                        f"{estimated_yield:,.2f} "
                        f"{t('yield_unit')}"
                    )

                else:

                    st.warning(
                        "Could not read numeric "
                        "yield from backend."
                    )

            else:

                st.error(
                    f"{t('api_error')} {error}"
                )


# ============================================================
# COST ESTIMATE
# ============================================================

elif page == t("cost"):

    st.header(
        t("cost_title")
    )

    st.write(
        t("cost_desc")
    )

    st.divider()

    # Completely independent from Yield Estimate

    crop = st.text_input(
        t("crop_name"),
        placeholder=(
            "e.g. Rice"
            if st.session_state.language == "English"
            else
            "जैसे धान"
        ),
        key="cost_crop"
    )

    state = st.text_input(
        t("state"),
        placeholder=(
            "e.g. Uttar Pradesh"
            if st.session_state.language == "English"
            else
            "जैसे उत्तर प्रदेश"
        ),
        key="cost_state"
    )

    yield_value = st.number_input(
        t("yield_input"),
        min_value=0.01,
        value=1.0,
        step=0.1,
        help=t("yield_help"),
        key="cost_yield"
    )

    st.info(
        "📌 Enter Yield in Quintal/Hectare."
        if st.session_state.language == "English"
        else
        "📌 उत्पादन क्विंटल/हेक्टेयर में दर्ज करें।"
    )

    st.divider()

    if st.button(
        t("estimate_cost"),
        type="primary",
        use_container_width=True
    ):

        if (
            not crop.strip()
            or not state.strip()
            or yield_value <= 0
        ):

            st.warning(
                t("required_fields")
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
                "Estimating cultivation cost..."
                if st.session_state.language == "English"
                else
                "खेती की लागत का अनुमान लगाया जा रहा है..."
            ):

                result, error = post_to_api(
                    "/predict3",
                    payload
                )

            if result:

                raw_cost = (

                    result.get(
                        "predict_cost"
                    )

                    or result.get(
                        "cost"
                    )

                    or result.get(
                        "predicted_cost"
                    )

                    or result.get(
                        "prediction"
                    )

                    or result.get(
                        "result"
                    )
                )

                estimated_cost = (
                    extract_number(
                        raw_cost
                    )
                )

                if estimated_cost is not None:

                    st.success(
                        t("cost_result")
                    )

                    st.metric(
                        t("cost_result"),
                        f"₹{estimated_cost:,.2f} "
                        f"{t('cost_unit')}"
                    )

                else:

                    st.warning(
                        "Could not read numeric "
                        "cost from backend."
                    )

            else:

                st.error(
                    f"{t('api_error')} {error}"
                )


# ============================================================
# PROFIT ESTIMATE
# ============================================================

elif page == t("profit"):

    st.header(
        t("profit_title")
    )

    st.write(
        t("profit_desc")
    )

    st.divider()

    st.info(
        "📌 Enter all values separately. "
        "Nothing is automatically taken from other sections."
        if st.session_state.language == "English"
        else
        "📌 सभी जानकारी अलग से दर्ज करें। "
        "दूसरे sections से कोई data automatically नहीं लिया जाएगा।"
    )

    col1, col2 = st.columns(2)

    with col1:

        profit_crop = st.text_input(
            t("crop_name"),
            placeholder=(
                "e.g. Rice"
                if st.session_state.language == "English"
                else
                "जैसे धान"
            ),
            key="profit_crop"
        )

        profit_state = st.text_input(
            t("state"),
            placeholder=(
                "e.g. Uttar Pradesh"
                if st.session_state.language == "English"
                else
                "जैसे उत्तर प्रदेश"
            ),
            key="profit_state"
        )

        profit_yield = st.number_input(
            t("yield_input"),
            min_value=0.01,
            value=1.0,
            step=0.1,
            help=t("yield_help"),
            key="profit_yield"
        )

    with col2:

        cultivation_cost = st.number_input(
            t("cultivation_cost"),
            min_value=0.0,
            value=10000.0,
            step=100.0,
            key="profit_cost"
        )

        selling_price = st.number_input(
            t("selling_price"),
            min_value=0.0,
            value=2500.0,
            step=50.0,
            help=t("selling_price_help"),
            key="profit_selling_price"
        )

    st.divider()

    st.caption(
        t("revenue_formula")
    )

    st.caption(
        t("profit_formula")
    )

    if st.button(
        t("calculate_profit"),
        type="primary",
        use_container_width=True
    ):

        if (
            not profit_crop.strip()
            or not profit_state.strip()
            or profit_yield <= 0
            or cultivation_cost < 0
            or selling_price < 0
        ):

            st.warning(
                t("required_fields")
            )

        else:

            # ------------------------------------------------
            # Calculation for 1 Hectare
            # ------------------------------------------------

            total_revenue = (
                profit_yield
                * selling_price
            )

            profit_value = (
                total_revenue
                - cultivation_cost
            )

            st.divider()

            st.subheader(
                "📊 Result"
            )

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    t("yield_result"),
                    f"{profit_yield:,.2f} "
                    f"{t('yield_unit')}"
                )

            with col2:

                st.metric(
                    t("total_revenue"),
                    f"₹{total_revenue:,.2f}"
                )

            with col3:

                st.metric(
                    t("cultivation_cost"),
                    f"₹{cultivation_cost:,.2f}"
                )

            st.divider()

            if profit_value >= 0:

                st.success(
                    f"{t('positive_profit')}: "
                    f"₹{profit_value:,.2f} / Hectare"
                )

            else:

                st.error(
                    f"{t('negative_profit')}: "
                    f"₹{abs(profit_value):,.2f} / Hectare"
                )

            st.divider()

            st.write(
                f"**{t('crop_name')}:** "
                f"{profit_crop}"
            )

            st.write(
                f"**{t('state')}:** "
                f"{profit_state}"
            )

            st.write(
                f"**{t('yield_input')}:** "
                f"{profit_yield:,.2f}"
            )

            st.write(
                f"**{t('selling_price')}:** "
                f"₹{selling_price:,.2f}"
            )

            st.write(
                f"**{t('total_revenue')}:** "
                f"₹{total_revenue:,.2f}"
            )

            st.write(
                f"**{t('cultivation_cost')}:** "
                f"₹{cultivation_cost:,.2f}"
            )

            st.write(
                f"**{t('profit')}:** "
                f"₹{profit_value:,.2f}"


            )


# ============================================================
# ABOUT
# ============================================================

elif page == t("about"):

    st.header(
        t("about_title")
    )

    st.write(
        t("about_text")
    )

    st.divider()

    st.subheader(
        "🌱 AgriSense AI"
    )

    st.write(
        """
        **Main Modules**

        1. 🌾 Crop Suggestion
        2. 📊 Yield Estimate
        3. 💰 Cost Estimate
        4. 📈 Profit Estimate
        """
    )

    st.divider()

    st.subheader(
        t("status")
    )

    st.write(
        f"**{t('backend')}:** `{API_URL}`"
    )

    try:

        response = requests.get(
            API_URL,
            timeout=15
        )

        if response.status_code == 200:

            st.success(
                t("api_success")
            )

        else:

            st.warning(
                f"{t('api_error')} "
                f"HTTP {response.status_code}"
            )

    except Exception:

        st.error(
            t("api_error")
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "🌱 AgriSense AI • Smart Farming Decision Support System"
)