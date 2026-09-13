import os
import requests
import pandas as pd
import streamlit as st
from datetime import datetime


# =========================================================
# CONFIG
# =========================================================

API_URL = os.getenv(
    "AGRISENSE_API_URL",
    "https://agrisense-api.onrender.com"
).rstrip("/")

WEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY",
    ""
)

WEATHER_URL = (
    "https://api.openweathermap.org/data/2.5/weather"
)


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1250px;
    }

    .hero {
        padding: 40px;
        border-radius: 24px;
        margin-bottom: 25px;
        background: linear-gradient(
            135deg,
            #0b5d3b,
            #198754
        );
        color: white;
    }

    .hero h1,
    .hero h2,
    .hero h3,
    .hero p {
        color: white !important;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 10px;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.7;
    }

    .feature-card {
        padding: 22px;
        border-radius: 18px;
        min-height: 175px;
        margin-bottom: 18px;

        background: rgba(128, 128, 128, 0.08);

        border: 1px solid
        rgba(128, 128, 128, 0.25);
    }

    .feature-card h3 {
        color: #198754 !important;
    }

    .feature-card p {
        line-height: 1.6;
    }

    .result-card {
        padding: 26px;
        border-radius: 18px;
        margin-top: 20px;

        background: rgba(25, 135, 84, 0.10);

        border: 1px solid
        rgba(25, 135, 84, 0.35);

        border-left: 6px solid #198754;
    }

    .result-card h2,
    .result-card h3 {
        color: #198754 !important;
    }

    .info-card {
        padding: 22px;
        border-radius: 18px;

        background: rgba(128, 128, 128, 0.08);

        border: 1px solid
        rgba(128, 128, 128, 0.25);

        line-height: 1.7;
    }

    .weather-card {
        padding: 22px;
        border-radius: 18px;
        text-align: center;

        background: rgba(128, 128, 128, 0.08);

        border: 1px solid
        rgba(128, 128, 128, 0.25);
    }

    .footer {
        margin-top: 45px;
        padding: 20px;
        text-align: center;
        border-radius: 16px;

        background: #073b28;
        color: white !important;
    }

    .footer p {
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LANGUAGE
# =========================================================

language = st.sidebar.radio(
    "Language / भाषा",
    ["English", "हिंदी"]
)


if language == "English":

    HOME = "Home"
    WEATHER = "Weather"
    CROP = "Crop Prediction"
    YIELD = "Yield Prediction"
    COST = "Cost Prediction"
    DASHBOARD = "Farm Dashboard"
    HISTORY = "Prediction History"
    ABOUT = "About"

else:

    HOME = "होम"
    WEATHER = "मौसम"
    CROP = "फसल भविष्यवाणी"
    YIELD = "उत्पादन भविष्यवाणी"
    COST = "लागत भविष्यवाणी"
    DASHBOARD = "कृषि डैशबोर्ड"
    HISTORY = "भविष्यवाणी इतिहास"
    ABOUT = "हमारे बारे में"


# =========================================================
# SESSION STATE
# =========================================================

if "weather" not in st.session_state:
    st.session_state.weather = None

if "weather_source" not in st.session_state:
    st.session_state.weather_source = None

if "history" not in st.session_state:
    st.session_state.history = []

if "last_crop" not in st.session_state:
    st.session_state.last_crop = ""

if "last_yield" not in st.session_state:
    st.session_state.last_yield = ""

if "last_cost" not in st.session_state:
    st.session_state.last_cost = ""


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌱 AgriSense AI")

page = st.sidebar.radio(
    "Navigation / नेविगेशन",
    [
        HOME,
        WEATHER,
        CROP,
        YIELD,
        COST,
        DASHBOARD,
        HISTORY,
        ABOUT
    ]
)


# =========================================================
# WEATHER FUNCTION
# =========================================================

def fetch_weather(village, district, state):

    if not WEATHER_API_KEY:

        return None, (
            "OpenWeather API key is not configured."
            if language == "English"
            else
            "OpenWeather API key configure नहीं है।"
        )

    village = village.strip()
    district = district.strip()
    state = state.strip()

    locations = [
        f"{village}, {district}, {state}, India",
        f"{village}, {state}, India",
        f"{district}, {state}, India"
    ]

    last_error = ""

    for location in locations:

        try:

            response = requests.get(
                WEATHER_URL,
                params={
                    "q": location,
                    "appid": WEATHER_API_KEY,
                    "units": "metric"
                },
                timeout=15
            )

            data = response.json()

            if response.status_code == 200:

                main = data.get(
                    "main",
                    {}
                )

                wind = data.get(
                    "wind",
                    {}
                )

                weather_list = data.get(
                    "weather",
                    [{}]
                )

                weather_info = weather_list[0]

                rain = data.get(
                    "rain",
                    {}
                )

                rainfall = rain.get("1h")

                if rainfall is None:
                    rainfall = rain.get(
                        "3h",
                        0.0
                    )

                rainfall = float(
                    rainfall or 0.0
                )

                result = {

                    "city": data.get(
                        "name",
                        village
                    ),

                    "temperature": float(
                        main.get(
                            "temp",
                            0
                        )
                    ),

                    "humidity": float(
                        main.get(
                            "humidity",
                            0
                        )
                    ),

                    "wind": float(
                        wind.get(
                            "speed",
                            0
                        )
                    ),

                    "rainfall": rainfall,

                    "condition":
                        weather_info.get(
                            "description",
                            "N/A"
                        ).title(),

                    "searched_location":
                        location
                }

                return result, None

            last_error = data.get(
                "message",
                "Location not found"
            )

        except requests.RequestException as e:

            last_error = str(e)

    return None, last_error


# =========================================================
# HOME
# =========================================================

if page == HOME:

    if language == "English":

        st.markdown(
            """
            <div class="hero">

                <h1>🌱 AgriSense AI</h1>

                <h3>
                    AI-Powered Agriculture Decision
                    Support System
                </h3>

                <p>
                    AgriSense AI combines Weather Information
                    and Machine Learning to help farmers make
                    smarter farming decisions.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="hero">

                <h1>🌱 AgriSense AI</h1>

                <h3>
                    AI आधारित कृषि निर्णय सहायता प्रणाली
                </h3>

                <p>
                    AgriSense AI मौसम की जानकारी और
                    Machine Learning का उपयोग करके
                    किसानों को बेहतर कृषि निर्णय लेने
                    में सहायता करता है।
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    st.image(
        "https://images.unsplash.com/"
        "photo-1625246333195-78d9c38ad449"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )

    st.header(
        "🌾 Key Features"
        if language == "English"
        else
        "🌾 मुख्य विशेषताएँ"
    )

    features = [

        (
            "🌦️",
            "Automatic Weather"
            if language == "English"
            else
            "Automatic Weather",
            "Get weather using Village, District "
            "and State."
            if language == "English"
            else
            "गाँव, जिला और राज्य से मौसम की जानकारी प्राप्त करें।"
        ),

        (
            "✍️",
            "Manual Weather"
            if language == "English"
            else
            "Manual Weather",
            "Enter Temperature, Humidity and "
            "Rainfall manually."
            if language == "English"
            else
            "Temperature, Humidity और Rainfall "
            "खुद भरें।"
        ),

        (
            "🌱",
            "Crop Recommendation"
            if language == "English"
            else
            "फसल की सिफारिश",
            "AI-based crop recommendation using "
            "soil and weather data."
            if language == "English"
            else
            "मिट्टी और मौसम के आधार पर "
            "AI से फसल की सिफारिश।"
        ),

        (
            "🌾",
            "Yield Prediction"
            if language == "English"
            else
            "उत्पादन भविष्यवाणी",
            "Predict yield using crop, state, "
            "season and area."
            if language == "English"
            else
            "फसल, राज्य, सीजन और क्षेत्रफल से "
            "उत्पादन का अनुमान।"
        ),

        (
            "💰",
            "Cost Prediction"
            if language == "English"
            else
            "लागत भविष्यवाणी",
            "Estimate agricultural investment cost."
            if language == "English"
            else
            "कृषि निवेश लागत का अनुमान लगाएँ।"
        ),

        (
            "📊",
            "Farm Dashboard"
            if language == "English"
            else
            "कृषि डैशबोर्ड",
            "See important prediction information "
            "in one place."
            if language == "English"
            else
            "जरूरी prediction information एक ही जगह देखें।"
        )
    ]

    for i in range(0, len(features), 3):

        cols = st.columns(3)

        for col, item in zip(
            cols,
            features[i:i + 3]
        ):

            icon, title, text = item

            with col:

                st.markdown(
                    f"""
                    <div class="feature-card">

                        <h3>
                            {icon} {title}
                        </h3>

                        <p>
                            {text}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.header(
        "🌍 About AgriSense AI"
        if language == "English"
        else
        "🌍 AgriSense AI के बारे में"
    )

    st.markdown(
        """
        <div class="info-card">

        <p>
        AgriSense AI is designed to bring modern
        Artificial Intelligence and Machine Learning
        into agriculture.
        </p>

        <p>
        Farmers can use automatic weather data or
        manually enter weather values. The selected
        weather information can then be used for
        AI-based crop prediction.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# WEATHER
# =========================================================

elif page == WEATHER:

    st.title(
        "🌦️ Weather"
        if language == "English"
        else
        "🌦️ मौसम"
    )

    st.write(
        "Choose how you want to provide weather data."
        if language == "English"
        else
        "चुनें कि आप Weather Data किस तरह देना चाहते हैं।"
    )

    weather_mode = st.radio(
        "Weather Input Mode / Weather Input तरीका",
        [
            "Automatic Weather",
            "Manual Weather"
        ],
        horizontal=True
    )

    # =====================================================
    # AUTOMATIC WEATHER
    # =====================================================

    if weather_mode == "Automatic Weather":

        st.subheader(
            "📍 Automatic Weather"
            if language == "English"
            else
            "📍 Automatic Weather"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            village = st.text_input(
                "Village / गाँव",
                placeholder="Malihabad"
            )

        with c2:

            district = st.text_input(
                "District / जिला",
                placeholder="Lucknow"
            )

        with c3:

            state = st.text_input(
                "State / राज्य",
                placeholder="Uttar Pradesh"
            )

        st.info(
            "The system will try Village + District + State "
            "first. If unavailable, it will try other "
            "available locations."
            if language == "English"
            else
            "System पहले Village + District + State को "
            "search करेगा। उपलब्ध न होने पर दूसरे "
            "available location को try करेगा।"
        )

        if st.button(
            "🌦️ Fetch Automatic Weather"
            if language == "English"
            else
            "🌦️ Automatic Weather प्राप्त करें",
            type="primary",
            use_container_width=True
        ):

            if (
                not village.strip()
                or not district.strip()
                or not state.strip()
            ):

                st.warning(
                    "Please fill Village, District and State."
                    if language == "English"
                    else
                    "कृपया Village, District और State भरें।"
                )

            else:

                with st.spinner(
                    "Fetching weather..."
                    if language == "English"
                    else
                    "मौसम की जानकारी प्राप्त की जा रही है..."
                ):

                    weather, error = fetch_weather(
                        village,
                        district,
                        state
                    )

                if weather:

                    st.session_state.weather = weather

                    st.session_state.weather_source = (
                        "Automatic"
                    )

                    st.success(
                        "Weather data fetched successfully."
                        if language == "English"
                        else
                        "Weather data सफलतापूर्वक प्राप्त हो गया।"
                    )

                else:

                    st.error(
                        "Weather data could not be fetched."
                        if language == "English"
                        else
                        "Weather data प्राप्त नहीं हो सका।"
                    )

                    st.caption(
                        f"API response: {error}"
                    )

    # =====================================================
    # MANUAL WEATHER
    # =====================================================

    else:

        st.subheader(
            "✍️ Manual Weather"
            if language == "English"
            else
            "✍️ Manual Weather"
        )

        st.info(
            "Enter the weather values yourself. These "
            "values can be used directly in Crop Prediction."
            if language == "English"
            else
            "Weather values खुद भरें। ये values सीधे "
            "Crop Prediction में इस्तेमाल की जा सकती हैं।"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            manual_temperature = st.number_input(
                "Temperature (°C)",
                value=25.0,
                step=0.1
            )

        with c2:

            manual_humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0
            )

        with c3:

            manual_rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=100.0,
                step=0.1
            )

        if st.button(
            "💾 Use Manual Weather"
            if language == "English"
            else
            "💾 Manual Weather इस्तेमाल करें",
            type="primary",
            use_container_width=True
        ):

            st.session_state.weather = {

                "city": "Manual Input",

                "temperature":
                    manual_temperature,

                "humidity":
                    manual_humidity,

                "wind":
                    0.0,

                "rainfall":
                    manual_rainfall,

                "condition":
                    "Manual Weather",

                "searched_location":
                    "Manual Input"
            }

            st.session_state.weather_source = (
                "Manual"
            )

            st.success(
                "Manual weather data saved."
                if language == "English"
                else
                "Manual weather data save हो गया।"
            )

    # =====================================================
    # SHOW WEATHER DATA
    # =====================================================

    if st.session_state.weather:

        weather = st.session_state.weather

        st.divider()

        st.subheader(
            "🌦️ Selected Weather Data"
            if language == "English"
            else
            "🌦️ Selected Weather Data"
        )

        if st.session_state.weather_source == "Automatic":

            st.caption(
                "Source: Automatic / OpenWeather"
                if language == "English"
                else
                "Source: Automatic / OpenWeather"
            )

        else:

            st.caption(
                "Source: Manual Input"
                if language == "English"
                else
                "Source: Manual Input"
            )

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "🌡️ Temperature",
                f"{weather['temperature']:.1f} °C"
            )

        with c2:

            st.metric(
                "💧 Humidity",
                f"{weather['humidity']:.0f}%"
            )

        with c3:

            st.metric(
                "🌧️ Rainfall",
                f"{weather['rainfall']:.1f} mm"
            )

        with c4:

            st.metric(
                "💨 Wind",
                f"{weather['wind']:.1f} m/s"
            )

        st.success(
            "This selected weather data is available "
            "for Crop Prediction."
            if language == "English"
            else
            "यह selected weather data Crop Prediction "
            "में इस्तेमाल किया जा सकता है।"
        )


# =========================================================
# CROP PREDICTION
# POST /predict1
# =========================================================

elif page == CROP:

    st.title(
        "🌱 Crop Prediction"
        if language == "English"
        else
        "🌱 फसल भविष्यवाणी"
    )

    st.markdown(
        """
        <div class="info-card">

        <h3>🌦️ Weather Data → Crop Prediction</h3>

        <p>
        You can choose <b>Automatic Weather</b> or
        <b>Manual Weather</b>. The selected Temperature,
        Humidity and Rainfall will be sent to the
        Crop Prediction API.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # =====================================================
    # WEATHER SOURCE SELECTION
    # =====================================================

    crop_weather_mode = st.radio(
        "Select Weather Source / Weather Source चुनें",
        [
            "Use Automatic Weather",
            "Enter Weather Manually"
        ],
        horizontal=True
    )

    # =====================================================
    # AUTOMATIC WEATHER FOR CROP
    # =====================================================

    if crop_weather_mode == "Use Automatic Weather":

        if (
            st.session_state.weather
            and
            st.session_state.weather_source
            == "Automatic"
        ):

            weather = st.session_state.weather

            st.success(
                f"Using automatic weather for "
                f"{weather['city']}."
                if language == "English"
                else
                f"{weather['city']} का automatic weather use हो रहा है।"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                temperature = st.number_input(
                    "Temperature (°C)",
                    value=float(
                        weather["temperature"]
                    ),
                    step=0.1,
                    key="crop_auto_temp"
                )

            with c2:

                humidity = st.number_input(
                    "Humidity (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=float(
                        weather["humidity"]
                    ),
                    step=1.0,
                    key="crop_auto_humidity"
                )

            with c3:

                rainfall = st.number_input(
                    "Rainfall (mm)",
                    min_value=0.0,
                    value=float(
                        weather["rainfall"]
                    ),
                    step=0.1,
                    key="crop_auto_rainfall"
                )

        else:

            st.warning(
                "Automatic weather is not available. "
                "Go to Weather page and fetch weather first."
                if language == "English"
                else
                "Automatic weather उपलब्ध नहीं है। "
                "पहले Weather page पर जाकर weather fetch करें।"
            )

            c1, c2, c3 = st.columns(3)

            with c1:

                temperature = st.number_input(
                    "Temperature (°C)",
                    value=25.0,
                    key="crop_auto_temp_empty"
                )

            with c2:

                humidity = st.number_input(
                    "Humidity (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=70.0,
                    key="crop_auto_humidity_empty"
                )

            with c3:

                rainfall = st.number_input(
                    "Rainfall (mm)",
                    min_value=0.0,
                    value=100.0,
                    key="crop_auto_rainfall_empty"
                )

    # =====================================================
    # MANUAL WEATHER FOR CROP
    # =====================================================

    else:

        st.info(
            "Enter weather values manually."
            if language == "English"
            else
            "Weather values manually भरें।"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            temperature = st.number_input(
                "Temperature (°C)",
                value=25.0,
                step=0.1,
                key="crop_manual_temp"
            )

        with c2:

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                step=1.0,
                key="crop_manual_humidity"
            )

        with c3:

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=100.0,
                step=0.1,
                key="crop_manual_rainfall"
            )

    # =====================================================
    # SOIL INPUT
    # =====================================================

    st.subheader(
        "🌱 Soil Parameters"
        if language == "English"
        else
        "🌱 मिट्टी के Parameters"
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=50.0,
            step=1.0
        )

    with c2:

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=40.0,
            step=1.0
        )

    with c3:

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=40.0,
            step=1.0
        )

    with c4:

        ph = st.number_input(
            "Soil pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5,
            step=0.1
        )

    st.divider()

    if st.button(
        "🌱 Predict Crop"
        if language == "English"
        else
        "🌱 फसल बताएँ",
        type="primary",
        use_container_width=True
    ):

        payload = {

            "N":
                N,

            "P":
                P,

            "K":
                K,

            "temperature":
                temperature,

            "humidity":
                humidity,

            "ph":
                ph,

            "rainfall":
                rainfall
        }

        try:

            response = requests.post(
                f"{API_URL}/predict1",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                crop_result = result.get(
                    "predict_crop",
                    "N/A"
                )

                st.session_state.last_crop = (
                    crop_result
                )

                st.session_state.history.append({

                    "Time":
                        datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        ),

                    "Type":
                        "Crop Prediction",

                    "Crop":
                        crop_result,

                    "Yield":
                        "",

                    "Cost":
                        ""
                })

                st.markdown(
                    f"""
                    <div class="result-card">

                        <h2>
                            🌾 Recommended Crop
                        </h2>

                        <h3>
                            {crop_result}
                        </h3>

                        <p>
                            Weather Source:
                            {crop_weather_mode}
                        </p>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.error(
                    f"Crop prediction failed. "
                    f"({response.status_code})"
                )

                st.code(
                    response.text,
                    language="json"
                )

        except requests.RequestException as e:

            st.error(
                f"Crop API request failed: {e}"
            )


# =========================================================
# YIELD PREDICTION
# POST /predict2
# =========================================================

elif page == YIELD:

    st.title(
        "🌾 Yield Prediction"
        if language == "English"
        else
        "🌾 उत्पादन भविष्यवाणी"
    )

    st.write(
        "Enter Crop, State, Season and Area "
        "to predict agricultural yield."
        if language == "English"
        else
        "Crop, State, Season और Area डालकर "
        "कृषि उत्पादन का अनुमान लगाएँ।"
    )

    c1, c2 = st.columns(2)

    with c1:

        crop = st.text_input(
            "Crop / फसल",
            placeholder="Rice"
        )

        state = st.text_input(
            "State / राज्य",
            placeholder="Uttar Pradesh"
        )

    with c2:

        season = st.text_input(
            "Season / सीजन",
            placeholder="Kharif"
        )

        area = st.number_input(
            "Area / क्षेत्रफल",
            min_value=0.0,
            value=1.0,
            step=0.1
        )

    st.info(
        "Crop, State and Season must match the labels "
        "used during model training."
        if language == "English"
        else
        "Crop, State और Season के नाम model training "
        "के labels से match होने चाहिए।"
    )

    if st.button(
        "🌾 Predict Yield"
        if language == "English"
        else
        "🌾 उत्पादन बताएँ",
        type="primary",
        use_container_width=True
    ):

        if (
            not crop.strip()
            or not state.strip()
            or not season.strip()
        ):

            st.warning(
                "Please fill all fields."
                if language == "English"
                else
                "कृपया सभी fields भरें।"
            )

        else:

            payload = {

                "Crop":
                    crop.strip(),

                "State":
                    state.strip(),

                "Season":
                    season.strip(),

                "Area":
                    area
            }

            try:

                response = requests.post(
                    f"{API_URL}/predict2",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    yield_result = result.get(
                        "predict_yield",
                        "N/A"
                    )

                    st.session_state.last_yield = (
                        yield_result
                    )

                    st.session_state.history.append({

                        "Time":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                        "Type":
                            "Yield Prediction",

                        "Crop":
                            crop.strip(),

                        "Yield":
                            yield_result,

                        "Cost":
                            ""
                    })

                    st.markdown(
                        f"""
                        <div class="result-card">

                            <h2>
                                🌾 Predicted Yield
                            </h2>

                            <h3>
                                {yield_result}
                            </h3>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Yield prediction failed. "
                        f"({response.status_code})"
                    )

                    st.code(
                        response.text,
                        language="json"
                    )

            except requests.RequestException as e:

                st.error(
                    f"Yield API request failed: {e}"
                )


# =========================================================
# COST PREDICTION
# POST /predict3
# =========================================================

elif page == COST:

    st.title(
        "💰 Cost Prediction"
        if language == "English"
        else
        "💰 लागत भविष्यवाणी"
    )

    c1, c2 = st.columns(2)

    with c1:

        crop = st.text_input(
            "Crop / फसल",
            placeholder="Rice"
        )

    with c2:

        state = st.text_input(
            "State / राज्य",
            placeholder="Uttar Pradesh"
        )

    yield_value = st.number_input(
        "Yield / उत्पादन",
        min_value=0.0,
        value=10.0,
        step=0.1
    )

    if st.button(
        "💰 Predict Cost"
        if language == "English"
        else
        "💰 लागत बताएँ",
        type="primary",
        use_container_width=True
    ):

        if (
            not crop.strip()
            or not state.strip()
        ):

            st.warning(
                "Please fill Crop and State."
                if language == "English"
                else
                "कृपया Crop और State भरें।"
            )

        else:

            payload = {

                "Crop":
                    crop.strip(),

                "State":
                    state.strip(),

                "Yield":
                    yield_value
            }

            try:

                response = requests.post(
                    f"{API_URL}/predict3",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    cost_result = result.get(
                        "predict_cost",
                        "N/A"
                    )

                    st.session_state.last_cost = (
                        cost_result
                    )

                    st.session_state.history.append({

                        "Time":
                            datetime.now().strftime(
                                "%Y-%m-%d %H:%M:%S"
                            ),

                        "Type":
                            "Cost Prediction",

                        "Crop":
                            crop.strip(),

                        "Yield":
                            yield_value,

                        "Cost":
                            cost_result
                    })

                    st.markdown(
                        f"""
                        <div class="result-card">

                            <h2>
                                💰 Estimated Cost
                            </h2>

                            <h3>
                                {cost_result}
                            </h3>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Cost prediction failed. "
                        f"({response.status_code})"
                    )

                    st.code(
                        response.text,
                        language="json"
                    )

            except requests.RequestException as e:

                st.error(
                    f"Cost API request failed: {e}"
                )


# =========================================================
# FARM DASHBOARD
# =========================================================

elif page == DASHBOARD:

    st.title(
        "📊 Farm Dashboard"
        if language == "English"
        else
        "📊 कृषि डैशबोर्ड"
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(
            "🌱 Last Crop",
            st.session_state.last_crop or "—"
        )

    with c2:

        st.metric(
            "🌾 Last Yield",
            st.session_state.last_yield or "—"
        )

    with c3:

        st.metric(
            "💰 Last Cost",
            st.session_state.last_cost or "—"
        )

    st.divider()

    st.subheader(
        "🌦️ Current Selected Weather"
        if language == "English"
        else
        "🌦️ Selected Weather"
    )

    if st.session_state.weather:

        weather = st.session_state.weather

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(
                "Temperature",
                f"{weather['temperature']:.1f} °C"
            )

        with c2:

            st.metric(
                "Humidity",
                f"{weather['humidity']:.0f}%"
            )

        with c3:

            st.metric(
                "Rainfall",
                f"{weather['rainfall']:.1f} mm"
            )

        with c4:

            st.metric(
                "Wind",
                f"{weather['wind']:.1f} m/s"
            )

    else:

        st.info(
            "No weather selected yet."
            if language == "English"
            else
            "अभी कोई weather select नहीं किया गया है।"
        )


# =========================================================
# HISTORY
# =========================================================

elif page == HISTORY:

    st.title(
        "🕘 Prediction History"
        if language == "English"
        else
        "🕘 भविष्यवाणी इतिहास"
    )

    if not st.session_state.history:

        st.info(
            "No prediction history yet."
            if language == "English"
            else
            "अभी कोई prediction history नहीं है।"
        )

    else:

        df = pd.DataFrame(
            st.session_state.history
        )

        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "🗑️ Clear History"
            if language == "English"
            else
            "🗑️ इतिहास साफ करें"
        ):

            st.session_state.history = []

            st.rerun()


# =========================================================
# ABOUT
# =========================================================

elif page == ABOUT:

    st.title(
        "🌿 About AgriSense AI"
        if language == "English"
        else
        "🌿 AgriSense AI के बारे में"
    )

    st.image(
        "https://images.unsplash.com/"
        "photo-1495107334309-fcf20504a5ab"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )

    if language == "English":

        st.markdown(
            """
            <div class="info-card">

            <h2>🌱 AgriSense AI</h2>

            <p>
            AgriSense AI is an intelligent agriculture
            decision-support platform that combines
            Weather Information and Machine Learning.
            </p>

            <h3>🌾 Main Features</h3>

            <ul>
                <li>Automatic Village Weather</li>
                <li>Manual Weather Input</li>
                <li>AI Crop Recommendation</li>
                <li>Yield Prediction</li>
                <li>Cost Prediction</li>
                <li>Farm Dashboard</li>
                <li>Prediction History</li>
            </ul>

            <h3>🔗 FastAPI Endpoints</h3>

            <p>
            <b>POST /predict1</b>
            → Crop Prediction
            </p>

            <p>
            <b>POST /predict2</b>
            → Yield Prediction
            </p>

            <p>
            <b>POST /predict3</b>
            → Yield + Cost Prediction
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            """
            <div class="info-card">

            <h2>🌱 AgriSense AI</h2>

            <p>
            AgriSense AI एक intelligent agriculture
            decision-support platform है जो Weather
            Information और Machine Learning को एक साथ
            उपयोग करता है।
            </p>

            <h3>🌾 मुख्य सुविधाएँ</h3>

            <ul>
                <li>Automatic Village Weather</li>
                <li>Manual Weather Input</li>
                <li>AI आधारित फसल सिफारिश</li>
                <li>उत्पादन भविष्यवाणी</li>
                <li>लागत भविष्यवाणी</li>
                <li>कृषि डैशबोर्ड</li>
                <li>भविष्यवाणी इतिहास</li>
            </ul>

            <h3>🔗 FastAPI Endpoints</h3>

            <p>
            <b>POST /predict1</b>
            → Crop Prediction
            </p>

            <p>
            <b>POST /predict2</b>
            → Yield Prediction
            </p>

            <p>
            <b>POST /predict3</b>
            → Yield + Cost Prediction
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        <p>
            🌱 <b>AgriSense AI</b>
        </p>

        <p>
            Smart Farming • AI • Machine Learning
            • Better Agriculture
        </p>

    </div>
    """,
    unsafe_allow_html=True
)