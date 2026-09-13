import os
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

# Render par Environment Variable:
# FASTAPI_URL=https://your-fastapi-service.onrender.com

API_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-gps1.onrender.com"
).rstrip("/")


# Render par Environment Variable:
# OPENWEATHER_API_KEY=your_api_key

WEATHER_API_KEY = os.getenv(
    "OPENWEATHER_API_KEY"
    
)


WEATHER_URL = (
    "https://agrisenseai-n621.onrender.com"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

    /* ================================
       GENERAL
       ================================ */

    .stApp {
        background: #0b0f14;
    }

    .main .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* ================================
       SIDEBAR
       ================================ */

    section[data-testid="stSidebar"] {
        background: #20232b;
        border-right: 1px solid #343942;
    }

    section[data-testid="stSidebar"] * {
        color: #ffffff;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px;
    }


    /* ================================
       HERO
       ================================ */

    .hero {
        background:
            linear-gradient(
                135deg,
                #064e32 0%,
                #087443 50%,
                #0b5d3b 100%
            );

        padding: 38px;
        border-radius: 0 0 24px 24px;

        color: white;

        margin-bottom: 25px;

        box-shadow:
            0 10px 35px rgba(0, 0, 0, 0.25);
    }

    .hero h1 {
        color: white;
        font-size: 48px;
        margin: 0 0 10px 0;
        font-weight: 700;
    }

    .hero h3 {
        color: #d9ffe9;
        font-size: 23px;
        margin-top: 8px;
    }

    .hero p {
        color: #ecfff4;
        font-size: 17px;
        line-height: 1.7;
    }


    /* ================================
       SECTION TITLE
       ================================ */

    .section-title {
        color: white;
        font-size: 30px;
        font-weight: 700;
        margin-top: 30px;
        margin-bottom: 20px;
    }


    /* ================================
       FEATURE CARDS
       ================================ */

    .feature-card {
        background: #171b21;
        border: 1px solid #30353e;
        border-radius: 18px;

        padding: 25px;

        min-height: 190px;

        box-shadow:
            0 5px 20px rgba(0, 0, 0, 0.18);

        margin-bottom: 20px;

        transition: 0.2s;
    }

    .feature-card:hover {
        border-color: #159957;
    }

    .feature-card h3 {
        color: #ffffff;
        font-size: 20px;
        margin-bottom: 15px;
    }

    .feature-card p {
        color: #c9ced6;
        font-size: 15px;
        line-height: 1.7;
    }


    /* ================================
       RESULT BOX
       ================================ */

    .result-box {
        background:
            linear-gradient(
                135deg,
                #063e29,
                #096b40
            );

        border-left: 6px solid #36d681;

        border-radius: 15px;

        padding: 25px;

        margin-top: 20px;

        color: white;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.2);
    }

    .result-box h2 {
        color: #ffffff;
        margin-top: 0;
    }

    .result-value {
        font-size: 28px;
        font-weight: 700;
        color: #9dffc5;
    }


    /* ================================
       INFO BOX
       ================================ */

    .info-box {
        background: #131c25;

        border: 1px solid #2e526b;

        border-left: 5px solid #2196f3;

        border-radius: 12px;

        padding: 18px;

        color: #dceeff;

        margin: 15px 0;
    }


    /* ================================
       WEATHER CARD
       ================================ */

    .weather-card {
        background: #171b21;

        border: 1px solid #30353e;

        border-radius: 18px;

        padding: 25px;

        margin-top: 20px;

        color: white;
    }


    /* ================================
       DASHBOARD CARD
       ================================ */

    .dashboard-card {
        background: #171b21;

        border: 1px solid #30353e;

        border-radius: 18px;

        padding: 20px;

        min-height: 130px;

        text-align: center;

        margin-bottom: 20px;
    }

    .dashboard-card h4 {
        color: #aeb6c2;
        margin-bottom: 10px;
    }

    .dashboard-card .value {
        color: #ffffff;
        font-size: 25px;
        font-weight: 700;
    }


    /* ================================
       ABOUT
       ================================ */

    .about-box {
        background: #171b21;

        border: 1px solid #30353e;

        border-radius: 18px;

        padding: 30px;

        color: #e4e8ed;

        line-height: 1.8;
    }

    .about-box h2 {
        color: white;
    }

    .about-box h3 {
        color: #5be89b;
        margin-top: 25px;
    }


    /* ================================
       FOOTER
       ================================ */

    .footer {
        background: #063b27;

        color: #e5fff0;

        text-align: center;

        padding: 25px;

        border-radius: 18px;

        margin-top: 50px;

        border: 1px solid #0b7148;
    }


    /* ================================
       BUTTON
       ================================ */

    div.stButton > button {
        background: #087f49;
        color: white;

        border: none;

        border-radius: 10px;

        padding: 10px 22px;

        font-weight: 600;
    }

    div.stButton > button:hover {
        background: #0aa45e;
        color: white;
    }

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "weather_data" not in st.session_state:
    st.session_state.weather_data = None


if "manual_weather" not in st.session_state:
    st.session_state.manual_weather = {
        "temperature": 25.0,
        "humidity": 70.0,
        "rainfall": 100.0
    }


if "crop_weather" not in st.session_state:
    st.session_state.crop_weather = None


if "crop_prediction" not in st.session_state:
    st.session_state.crop_prediction = None


if "yield_prediction" not in st.session_state:
    st.session_state.yield_prediction = None


if "cost_prediction" not in st.session_state:
    st.session_state.cost_prediction = None


if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def add_history(prediction_type, result, inputs=None):
    """
    Prediction History me result save karta hai.
    """

    st.session_state.history.append(
        {
            "type": prediction_type,
            "result": str(result),
            "inputs": inputs or {}
        }
    )


def get_weather(city):
    """
    OpenWeather API se weather data fetch karta hai.
    """

    if not WEATHER_API_KEY:
        return None, "OPENWEATHER_API_KEY is not configured."

    try:

        response = requests.get(
            WEATHER_URL,
            params={
                "q": city,
                "appid": WEATHER_API_KEY,
                "units": "metric"
            },
            timeout=15
        )

        try:
            data = response.json()
        except Exception:
            data = {}

        if response.status_code == 200:

            return data, None

        message = data.get(
            "message",
            "Unable to fetch weather."
        )

        return None, message

    except requests.exceptions.Timeout:

        return None, "Weather API request timed out."

    except requests.exceptions.ConnectionError:

        return None, "Could not connect to weather service."

    except Exception as e:

        return None, str(e)


def call_fastapi(endpoint, payload):
    """
    FastAPI endpoint ko POST request bhejta hai.
    """

    try:

        response = requests.post(
            f"{API_URL}{endpoint}",
            json=payload,
            timeout=60
        )

        try:
            data = response.json()
        except Exception:
            data = {
                "raw_response": response.text
            }

        if response.status_code == 200:

            return data, None

        return None, (
            f"API Error {response.status_code}: "
            f"{response.text}"
        )

    except requests.exceptions.Timeout:

        return None, (
            "FastAPI request timed out. "
            "Please check whether your Render API service is running."
        )

    except requests.exceptions.ConnectionError:

        return None, (
            "Could not connect to FastAPI. "
            "Check FASTAPI_URL."
        )

    except Exception as e:

        return None, str(e)


def show_weather_card(data):
    """
    Weather data ko UI me display karta hai.
    """

    if not data:
        return

    temperature = data.get("main", {}).get(
        "temp",
        "N/A"
    )

    humidity = data.get("main", {}).get(
        "humidity",
        "N/A"
    )

    pressure = data.get("main", {}).get(
        "pressure",
        "N/A"
    )

    wind = data.get("wind", {}).get(
        "speed",
        "N/A"
    )

    rainfall = data.get(
        "rain",
        {}
    ).get(
        "1h",
        0
    )

    weather_list = data.get(
        "weather",
        []
    )

    description = "N/A"

    if weather_list:
        description = weather_list[0].get(
            "description",
            "N/A"
        ).title()

    city_name = data.get(
        "name",
        "Unknown"
    )

    country = data.get(
        "sys",
        {}
    ).get(
        "country",
        ""
    )

    st.markdown(
        f"""
        <div class="weather-card">

            <h2>🌦️ {city_name}, {country}</h2>

            <p>
                Current Condition:
                <b>{description}</b>
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "🌡️ Temperature",
            f"{temperature} °C"
        )

    with col2:

        st.metric(
            "💧 Humidity",
            f"{humidity}%"
        )

    with col3:

        st.metric(
            "💨 Wind",
            f"{wind} m/s"
        )

    with col4:

        st.metric(
            "🌧️ Rainfall",
            f"{rainfall} mm"
        )

    with col5:

        st.metric(
            "🔵 Pressure",
            f"{pressure} hPa"
        )


# ============================================================
# LANGUAGE
# ============================================================

st.sidebar.markdown(
    "### 🌐 Language / भाषा"
)

language = st.sidebar.radio(
    "Select Language",
    [
        "English",
        "हिंदी"
    ],
    label_visibility="collapsed"
)


# ============================================================
# SIDEBAR BRAND
# ============================================================

st.sidebar.markdown(
    """
    <div style="
        text-align:center;
        padding:20px 0 15px 0;
    ">

        <div style="
            font-size:40px;
        ">
            🌱
        </div>

        <div style="
            font-size:23px;
            font-weight:700;
            color:white;
        ">
            AgriSense AI
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# NAVIGATION LABELS
# ============================================================

if language == "English":

    home_label = "Home"
    weather_label = "Weather"
    crop_label = "Crop Prediction"
    yield_label = "Yield Prediction"
    cost_label = "Cost Prediction"
    dashboard_label = "Farm Dashboard"
    history_label = "Prediction History"
    about_label = "About"

else:

    home_label = "होम"
    weather_label = "मौसम"
    crop_label = "फसल भविष्यवाणी"
    yield_label = "उत्पादन भविष्यवाणी"
    cost_label = "लागत भविष्यवाणी"
    dashboard_label = "फार्म डैशबोर्ड"
    history_label = "भविष्यवाणी इतिहास"
    about_label = "हमारे बारे में"


# ============================================================
# NAVIGATION
# ============================================================

st.sidebar.markdown(
    "### 🧭 Navigation / नेविगेशन"
)

page = st.sidebar.radio(
    "Navigation",
    [
        home_label,
        weather_label,
        crop_label,
        yield_label,
        cost_label,
        dashboard_label,
        history_label,
        about_label
    ],
    label_visibility="collapsed"
)


# ============================================================
# HOME PAGE
# ============================================================

if page == home_label:

    if language == "English":

        title = "AgriSense AI"

        subtitle = (
            "AI-Powered Agriculture "
            "Decision Support System"
        )

        description = (
            "AgriSense AI combines weather information "
            "and Machine Learning to help farmers make "
            "smarter farming decisions."
        )

    else:

        title = "AgriSense AI"

        subtitle = (
            "AI आधारित कृषि "
            "निर्णय सहायता प्रणाली"
        )

        description = (
            "AgriSense AI मौसम की जानकारी और "
            "Machine Learning को मिलाकर किसानों को "
            "बेहतर कृषि निर्णय लेने में सहायता करता है।"
        )

    # HERO
    st.markdown(
        f"""
        <div class="hero">

            <h1>🌱 {title}</h1>

            <h3>{subtitle}</h3>

            <p>{description}</p>

        </div>
        """,
        unsafe_allow_html=True
    )


    # IMAGE
    st.image(
        "https://images.unsplash.com/photo-1625246333195-78d9c38ad449"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )


    if language == "English":

        st.markdown(
            '<div class="section-title">'
            '🌾 Smart Agriculture Features'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="section-title">'
            '🌾 स्मार्ट कृषि सुविधाएँ'
            '</div>',
            unsafe_allow_html=True
        )


    # ROW 1

    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            """
            <div class="feature-card">

                <h3>🌦️ Automatic Weather</h3>

                <p>
                    Enter your village or city and get
                    current weather information such as
                    temperature, humidity, rainfall and wind.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            """
            <div class="feature-card">

                <h3>✍️ Manual Weather</h3>

                <p>
                    If automatic weather is unavailable,
                    users can manually enter temperature,
                    humidity and rainfall.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            """
            <div class="feature-card">

                <h3>🌱 Crop Recommendation</h3>

                <p>
                    Use soil nutrients and weather
                    conditions to get an AI-based
                    crop recommendation.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ROW 2

    col4, col5, col6 = st.columns(3)


    with col4:

        st.markdown(
            """
            <div class="feature-card">

                <h3>🌾 Yield Prediction</h3>

                <p>
                    Predict expected agricultural yield
                    using crop, state, season and area.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col5:

        st.markdown(
            """
            <div class="feature-card">

                <h3>💰 Cost Prediction</h3>

                <p>
                    Estimate agricultural investment
                    cost using crop, state and yield.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col6:

        st.markdown(
            """
            <div class="feature-card">

                <h3>📊 Farm Dashboard</h3>

                <p>
                    View weather, crop prediction,
                    yield prediction and cost
                    information in one place.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# WEATHER PAGE
# ============================================================

elif page == weather_label:

    st.title("🌦️ Weather / मौसम")

    st.write(
        "Get current weather information for your "
        "village or city."
        if language == "English"
        else
        "अपने गांव या शहर की वर्तमान मौसम जानकारी प्राप्त करें।"
    )


    weather_mode = st.radio(
        "Weather Input Method / मौसम का तरीका",
        [
            "Automatic Weather",
            "Manual Weather"
        ]
        if language == "English"
        else
        [
            "Automatic मौसम",
            "Manual मौसम"
        ]
    )


    # --------------------------------------------------------
    # AUTOMATIC WEATHER
    # --------------------------------------------------------

    if weather_mode in [
        "Automatic Weather",
        "Automatic मौसम"
    ]:

        st.subheader(
            "📍 Automatic Weather"
            if language == "English"
            else
            "📍 Automatic मौसम"
        )

        city = st.text_input(
            "Village / City / गांव / शहर",
            placeholder="Prayagraj"
        )


        if st.button(
            "🌦️ Get Weather / मौसम देखें",
            type="primary"
        ):

            if not city.strip():

                st.warning(
                    "Please enter village or city name."
                    if language == "English"
                    else
                    "कृपया गांव या शहर का नाम डालें।"
                )

            else:

                with st.spinner(
                    "Fetching weather..."
                ):

                    data, error = get_weather(
                        city.strip()
                    )


                if error:

                    st.error(
                        f"Weather Error: {error}"
                    )

                else:

                    st.session_state.weather_data = data

                    st.success(
                        "Weather data loaded successfully."
                        if language == "English"
                        else
                        "मौसम की जानकारी सफलतापूर्वक प्राप्त हो गई।"
                    )


        if st.session_state.weather_data:

            show_weather_card(
                st.session_state.weather_data
            )


    # --------------------------------------------------------
    # MANUAL WEATHER
    # --------------------------------------------------------

    else:

        st.subheader(
            "✍️ Manual Weather"
            if language == "English"
            else
            "✍️ Manual मौसम"
        )


        temperature = st.number_input(
            "🌡️ Temperature (°C)",
            value=float(
                st.session_state.manual_weather[
                    "temperature"
                ]
            )
        )


        humidity = st.number_input(
            "💧 Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                st.session_state.manual_weather[
                    "humidity"
                ]
            )
        )


        rainfall = st.number_input(
            "🌧️ Rainfall (mm)",
            min_value=0.0,
            value=float(
                st.session_state.manual_weather[
                    "rainfall"
                ]
            )
        )


        if st.button(
            "💾 Save Weather Data",
            type="primary"
        ):

            st.session_state.manual_weather = {
                "temperature": temperature,
                "humidity": humidity,
                "rainfall": rainfall
            }

            st.success(
                "Manual weather data saved."
                if language == "English"
                else
                "Manual मौसम डेटा सेव हो गया।"
            )


        st.markdown(
            """
            <div class="info-box">

                🌱 These weather values can be used
                as input for Crop Prediction.

            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# CROP PREDICTION
# ============================================================

elif page == crop_label:

    st.title(
        "🌱 Crop Prediction / फसल भविष्यवाणी"
    )

    st.write(
        "Enter soil and weather conditions to get "
        "an AI-based crop recommendation."
        if language == "English"
        else
        "मिट्टी और मौसम की जानकारी डालकर "
        "AI आधारित फसल की सिफारिश प्राप्त करें।"
    )


    # --------------------------------------------------------
    # WEATHER INPUT
    # --------------------------------------------------------

    st.subheader(
        "🌦️ Weather Information"
        if language == "English"
        else
        "🌦️ मौसम की जानकारी"
    )


    weather_source = st.radio(
        "Select Weather Source",
        [
            "Use Automatic Weather",
            "Enter Weather Manually"
        ]
        if language == "English"
        else
        [
            "Automatic मौसम इस्तेमाल करें",
            "मौसम manually भरें"
        ]
    )


    # --------------------------------------------------------
    # AUTOMATIC WEATHER
    # --------------------------------------------------------

    if weather_source == "Use Automatic Weather":

        city = st.text_input(
            "Village / City",
            placeholder="Prayagraj"
        )


        if st.button(
            "🌦️ Load Weather"
        ):

            if not city.strip():

                st.warning(
                    "Please enter village or city."
                )

            else:

                data, error = get_weather(
                    city.strip()
                )

                if error:

                    st.error(
                        f"Weather Error: {error}"
                    )

                else:

                    st.session_state.crop_weather = {
                        "temperature":
                            data["main"]["temp"],

                        "humidity":
                            data["main"]["humidity"],

                        "rainfall":
                            data.get(
                                "rain",
                                {}
                            ).get(
                                "1h",
                                0
                            )
                    }

                    st.success(
                        f"Weather loaded for {data.get('name', city)}."
                    )


        weather = st.session_state.crop_weather


        if weather:

            temperature = st.number_input(
                "🌡️ Temperature (°C)",
                value=float(
                    weather["temperature"]
                )
            )


            humidity = st.number_input(
                "💧 Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(
                    weather["humidity"]
                )
            )


            rainfall = st.number_input(
                "🌧️ Rainfall (mm)",
                min_value=0.0,
                value=float(
                    weather["rainfall"]
                )
            )

        else:

            st.info(
                "Enter a city and click Load Weather."
            )

            temperature = st.number_input(
                "🌡️ Temperature (°C)",
                value=25.0
            )

            humidity = st.number_input(
                "💧 Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0
            )

            rainfall = st.number_input(
                "🌧️ Rainfall (mm)",
                min_value=0.0,
                value=100.0
            )


    # --------------------------------------------------------
    # MANUAL WEATHER
    # --------------------------------------------------------

    else:

        temperature = st.number_input(
            "🌡️ Temperature (°C)",
            value=25.0
        )


        humidity = st.number_input(
            "💧 Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0
        )


        rainfall = st.number_input(
            "🌧️ Rainfall (mm)",
            min_value=0.0,
            value=100.0
        )


    # --------------------------------------------------------
    # SOIL INPUT
    # --------------------------------------------------------

    st.subheader(
        "🌱 Soil Information"
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        nitrogen = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=50.0
        )


    with col2:

        phosphorus = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=40.0
        )


    with col3:

        potassium = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=40.0
        )


    ph = st.number_input(
        "Soil pH",
        min_value=0.0,
        max_value=14.0,
        value=6.5
    )


    st.markdown(
        """
        <div class="info-box">

            🌱 Crop prediction uses:

            <br><br>

            Nitrogen + Phosphorus + Potassium +
            Temperature + Humidity + pH + Rainfall

        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # PREDICTION
    # --------------------------------------------------------

    if st.button(
        "🌱 Predict Crop / फसल बताएँ",
        type="primary"
    ):

        payload = {

            "N": nitrogen,

            "P": phosphorus,

            "K": potassium,

            "temperature": temperature,

            "humidity": humidity,

            "ph": ph,

            "rainfall": rainfall
        }


        with st.spinner(
            "Running ML model..."
        ):

            result, error = call_fastapi(
                "/predict1",
                payload
            )


        if error:

            st.error(error)

        else:

            prediction = result.get(
                "predict_crop",
                result.get(
                    "prediction",
                    result.get(
                        "crop",
                        "Prediction received"
                    )
                )
            )


            st.session_state.crop_prediction = prediction


            add_history(
                "Crop Prediction",
                prediction,
                payload
            )


            st.markdown(
                f"""
                <div class="result-box">

                    <h2>🌾 Recommended Crop</h2>

                    <div class="result-value">
                        {prediction}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# YIELD PREDICTION
# ============================================================

elif page == yield_label:

    st.title(
        "🌾 Yield Prediction / उत्पादन भविष्यवाणी"
    )


    st.write(
        "Predict agricultural yield using crop, state, "
        "season and area."
    )


    crop = st.text_input(
        "🌱 Crop / फसल",
        placeholder="Rice"
    )


    state = st.text_input(
        "📍 State / राज्य",
        placeholder="Uttar Pradesh"
    )


    season = st.text_input(
        "🌦️ Season / सीजन",
        placeholder="Kharif"
    )


    area = st.number_input(
        "📐 Area / क्षेत्रफल",
        min_value=0.0,
        value=1.0
    )


    st.markdown(
        """
        <div class="info-box">

            ⚠️ Crop, State and Season values should
            match the categories used while training
            your ML model.

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🌾 Predict Yield / उत्पादन बताएँ",
        type="primary"
    ):

        if not crop.strip():

            st.warning(
                "Please enter crop."
            )

        elif not state.strip():

            st.warning(
                "Please enter state."
            )

        elif not season.strip():

            st.warning(
                "Please enter season."
            )

        else:

            payload = {

                "Crop": crop.strip(),

                "State": state.strip(),

                "Season": season.strip(),

                "Area": area
            }


            with st.spinner(
                "Running Yield ML model..."
            ):

                result, error = call_fastapi(
                    "/predict2",
                    payload
                )


            if error:

                st.error(error)

            else:

                prediction = result.get(
                    "predict_yield",
                    result.get(
                        "prediction",
                        result.get(
                            "yield",
                            "Prediction received"
                        )
                    )
                )


                st.session_state.yield_prediction = (
                    prediction
                )


                add_history(
                    "Yield Prediction",
                    prediction,
                    payload
                )


                st.markdown(
                    f"""
                    <div class="result-box">

                        <h2>🌾 Predicted Yield</h2>

                        <div class="result-value">
                            {prediction}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# COST PREDICTION
# ============================================================

elif page == cost_label:

    st.title(
        "💰 Cost Prediction / लागत भविष्यवाणी"
    )


    st.write(
        "Estimate agricultural investment cost "
        "using crop, state and yield."
    )


    crop = st.text_input(
        "🌱 Crop / फसल",
        placeholder="Rice"
    )


    state = st.text_input(
        "📍 State / राज्य",
        placeholder="Uttar Pradesh"
    )


    yield_value = st.number_input(
        "🌾 Yield / उत्पादन",
        min_value=0.0,
        value=10.0
    )


    if st.button(
        "💰 Predict Cost / लागत बताएँ",
        type="primary"
    ):

        if not crop.strip():

            st.warning(
                "Please enter crop."
            )

        elif not state.strip():

            st.warning(
                "Please enter state."
            )

        else:

            payload = {

                "Crop": crop.strip(),

                "State": state.strip(),

                "Yield": yield_value
            }


            with st.spinner(
                "Running Cost ML model..."
            ):

                result, error = call_fastapi(
                    "/predict3",
                    payload
                )


            if error:

                st.error(error)

            else:

                prediction = result.get(
                    "predict_cost",
                    result.get(
                        "prediction",
                        result.get(
                            "cost",
                            "Prediction received"
                        )
                    )
                )


                st.session_state.cost_prediction = (
                    prediction
                )


                add_history(
                    "Cost Prediction",
                    prediction,
                    payload
                )


                st.markdown(
                    f"""
                    <div class="result-box">

                        <h2>💰 Estimated Cost</h2>

                        <div class="result-value">
                            {prediction}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# FARM DASHBOARD
# ============================================================

elif page == dashboard_label:

    st.title(
        "📊 Farm Dashboard / फार्म डैशबोर्ड"
    )


    st.write(
        "Your latest agriculture predictions and weather information."
    )


    # --------------------------------------------------------
    # WEATHER
    # --------------------------------------------------------

    weather = st.session_state.weather_data


    if weather:

        temperature = weather.get(
            "main",
            {}
        ).get(
            "temp",
            "N/A"
        )

        humidity = weather.get(
            "main",
            {}
        ).get(
            "humidity",
            "N/A"
        )

        rainfall = weather.get(
            "rain",
            {}
        ).get(
            "1h",
            0
        )

        weather_city = weather.get(
            "name",
            "N/A"
        )

    else:

        temperature = "N/A"
        humidity = "N/A"
        rainfall = "N/A"
        weather_city = "Not loaded"


    # --------------------------------------------------------
    # DASHBOARD
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>🌦️ Weather</h4>

                <div class="value">
                    {weather_city}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>🌡️ Temperature</h4>

                <div class="value">
                    {temperature} °C
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>🌱 Crop</h4>

                <div class="value">
                    {st.session_state.crop_prediction or "Not predicted"}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col4:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>🌾 Yield</h4>

                <div class="value">
                    {st.session_state.yield_prediction or "Not predicted"}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    col5, col6, col7 = st.columns(3)


    with col5:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>💰 Estimated Cost</h4>

                <div class="value">
                    {st.session_state.cost_prediction or "Not predicted"}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col6:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>💧 Humidity</h4>

                <div class="value">
                    {humidity}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col7:

        st.markdown(
            f"""
            <div class="dashboard-card">

                <h4>🌧️ Rainfall</h4>

                <div class="value">
                    {rainfall} mm
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        """
        <div class="info-box">

            💡 <b>Tip:</b>

            Go to Crop Prediction, Yield Prediction
            and Cost Prediction to generate new results.

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PREDICTION HISTORY
# ============================================================

elif page == history_label:

    st.title(
        "🕘 Prediction History / भविष्यवाणी इतिहास"
    )


    if not st.session_state.history:

        st.info(
            "No prediction history yet."
        )

    else:

        st.write(
            f"Total predictions: "
            f"{len(st.session_state.history)}"
        )


        for index, item in enumerate(
            reversed(
                st.session_state.history
            ),
            start=1
        ):

            st.markdown(
                f"""
                <div class="feature-card">

                    <h3>
                        {index}. {item["type"]}
                    </h3>

                    <p>
                        <b>Result:</b>
                        {item["result"]}
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        if st.button(
            "🗑️ Clear Prediction History"
        ):

            st.session_state.history = []

            st.success(
                "Prediction history cleared."
            )

            st.rerun()


# ============================================================
# ABOUT
# ============================================================

elif page == about_label:

    st.title(
        "🌍 About AgriSense AI"
    )


    st.markdown(
        """
        <div class="about-box">

            <h2>🌱 AgriSense AI</h2>

            <p>
                AgriSense AI is an AI-powered agriculture
                decision support system designed to bring
                modern Artificial Intelligence and Machine
                Learning into agriculture.
            </p>

            <h3>🌦️ Weather Information</h3>

            <p>
                Farmers can obtain current weather
                information by entering their village
                or city. Manual weather input is also
                available.
            </p>

            <h3>🌱 Crop Prediction</h3>

            <p>
                The system uses soil nutrients and
                weather conditions to provide an
                AI-based crop recommendation.
            </p>

            <h3>🌾 Yield Prediction</h3>

            <p>
                Users can enter crop, state, season
                and area to estimate agricultural yield.
            </p>

            <h3>💰 Cost Prediction</h3>

            <p>
                Users can estimate agricultural cost
                using crop, state and predicted yield.
            </p>

            <h3>📊 Farm Dashboard</h3>

            <p>
                The dashboard brings important
                weather and prediction results together
                in one place.
            </p>

            <h3>🤖 Technology</h3>

            <p>
                Frontend: Streamlit
                <br>
                Backend: FastAPI
                <br>
                Machine Learning: Python ML Models
                <br>
                Weather: OpenWeather API
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

        <div style="font-size:24px;">
            🌱 <b>AgriSense AI</b>
        </div>

        <br>

        Smart Farming • Artificial Intelligence
        • Machine Learning

        <br><br>

        <span style="color:#b8eacb;">
            AI + Agriculture for Better Farming Decisions
        </span>

    </div>
    """,
    unsafe_allow_html=True
)