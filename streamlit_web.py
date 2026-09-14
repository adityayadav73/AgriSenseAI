import os
import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================

API_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-n621.onrender.com"
)

WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="wide"
)


# =========================================================
# PROFESSIONAL CSS
# =========================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    .hero {
        padding: 35px;
        border-radius: 22px;
        background: linear-gradient(
            135deg,
            #0b5d3b,
            #198754
        );
        color: white;
        margin-bottom: 25px;
    }

    .hero h1 {
        font-size: 48px;
        margin-bottom: 8px;
    }

    .hero h3 {
        margin-bottom: 15px;
    }

    .feature-card {
        padding: 22px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #dce8df;
        min-height: 170px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }

    .feature-card h3 {
        color: #126b45;
    }

    .result-box {
        padding: 25px;
        border-radius: 18px;
        background-color: #e9f7ef;
        border-left: 6px solid #198754;
        margin-top: 20px;
    }

    .weather-box {
        padding: 20px;
        border-radius: 18px;
        background-color: #f4f9f5;
        border: 1px solid #dce8df;
        margin-top: 15px;
    }

    .about-box {
        padding: 25px;
        border-radius: 18px;
        background-color: white;
        border: 1px solid #dce8df;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
    }

    .footer {
        text-align: center;
        padding: 20px;
        margin-top: 40px;
        background-color: #073b28;
        color: white;
        border-radius: 15px;
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


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🌱 AgriSense AI")

if language == "English":

    pages = [
        "Home",
        "Weather",
        "Crop Prediction",
        "Yield Prediction",
        "Cost Prediction",
        "About"
    ]

else:

    pages = [
        "होम",
        "मौसम",
        "फसल सुझाव",
        "उत्पादन अनुमान",
        "लागत अनुमान",
        "हमारे बारे में"
    ]


page = st.sidebar.radio(
    "Navigation / नेविगेशन",
    pages
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_weather(city):
    """
    Get current weather from OpenWeather.
    """

    if not WEATHER_API_KEY:
        return None, "OpenWeather API key is not configured."

    try:

        response = requests.get(
            WEATHER_URL,
            params={
                "q": city.strip(),
                "appid": WEATHER_API_KEY,
                "units": "metric"
            },
            timeout=10
        )

        data = response.json()

        if response.status_code == 200:
            return data, None

        return None, (
            f"Weather data could not be fetched. "
            f"({response.status_code}) "
            f"{data.get('message', '')}"
        )

    except Exception as e:

        return None, f"Weather request failed: {e}"


def clean_crop_name(crop):
    """
    Convert model output into a user-friendly crop name.
    """

    if not crop:
        return "Unknown Crop"

    crop = str(crop).strip()

    crop_lower = crop.lower()

    crop_lower = crop_lower.replace(" ", "")
    crop_lower = crop_lower.replace("_", "")
    crop_lower = crop_lower.replace("-", "")

    crop_names = {

        "ispigeonpeas":
            "Pigeon Peas",

        "pigeonpeas":
            "Pigeon Peas",

        "pigeonpea":
            "Pigeon Peas",

        "rice":
            "Rice",

        "maize":
            "Maize",

        "wheat":
            "Wheat",

        "chickpea":
            "Chickpea",

        "chickpeas":
            "Chickpea",

        "kidneybeans":
            "Kidney Beans",

        "kidneybean":
            "Kidney Beans",

        "blackgram":
            "Black Gram",

        "mungbean":
            "Mung Bean",

        "mothbeans":
            "Moth Beans",

        "lentil":
            "Lentil",

        "cotton":
            "Cotton",

        "jute":
            "Jute",

        "coffee":
            "Coffee",

        "banana":
            "Banana",

        "mango":
            "Mango",

        "grapes":
            "Grapes",

        "apple":
            "Apple",

        "orange":
            "Orange",

        "papaya":
            "Papaya",

        "watermelon":
            "Watermelon",

        "muskmelon":
            "Muskmelon",

        "coconut":
            "Coconut"
    }

    return crop_names.get(
        crop_lower,
        crop.replace("is", "").strip().title()
    )


# =========================================================
# HOME
# =========================================================

if page in ["Home", "होम"]:

    if language == "English":

        st.markdown(
            """
            <div class="hero">

                <h1>🌱 AgriSense AI</h1>

                <h3>
                    Smart Agriculture Decision Support Platform
                </h3>

                <p>
                    Use weather and data-driven agricultural insights
                    to make smarter farming decisions.
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
                    स्मार्ट कृषि निर्णय सहायता प्लेटफॉर्म
                </h3>

                <p>
                    मौसम और कृषि डेटा की मदद से बेहतर
                    खेती के निर्णय लेने में सहायता।
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.image(
        "https://images.unsplash.com/photo-1625246333195-78d9c38ad449"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )


    if language == "English":

        st.header("🌾 Key Features")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌦️ Weather Information</h3>

                    <p>
                    Check weather automatically using a
                    village or city name.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌱 Crop Suggestion</h3>

                    <p>
                    Get a crop suggestion using soil
                    and weather conditions.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌾 Yield Estimate</h3>

                    <p>
                    Estimate agricultural production using
                    crop, state, season and area.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        col4, col5, col6 = st.columns(3)


        with col4:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>💰 Cost Estimate</h3>

                    <p>
                    Estimate agricultural investment cost
                    using crop, state and yield.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col5:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌦️ Flexible Weather Input</h3>

                    <p>
                    Choose between automatic weather
                    or manual weather input.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col6:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>📊 Data-Driven Insights</h3>

                    <p>
                    Transform agricultural data into
                    useful farming insights.
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        st.header("🌍 About AgriSense AI")

        st.markdown(
            """
            <div class="about-box">

            <p>
            AgriSense AI is a smart agriculture platform designed
            to support farmers with practical, data-driven insights.
            </p>

            <p>
            Weather information can be obtained automatically or
            entered manually. The selected weather information can
            then be used directly in the Crop Suggestion feature
            along with soil information.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.header("🌾 मुख्य विशेषताएँ")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌦️ मौसम की जानकारी</h3>

                    <p>
                    गांव या शहर के नाम से मौसम की जानकारी प्राप्त करें।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col2:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌱 फसल सुझाव</h3>

                    <p>
                    मिट्टी और मौसम की स्थिति के आधार पर
                    फसल का सुझाव प्राप्त करें।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col3:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌾 उत्पादन अनुमान</h3>

                    <p>
                    फसल, राज्य, सीजन और क्षेत्रफल के आधार पर
                    उत्पादन का अनुमान लगाएँ।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        col4, col5, col6 = st.columns(3)


        with col4:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>💰 लागत अनुमान</h3>

                    <p>
                    फसल, राज्य और उत्पादन के आधार पर
                    कृषि लागत का अनुमान लगाएँ।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col5:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>🌦️ मौसम डेटा विकल्प</h3>

                    <p>
                    Automatic या Manual मौसम डेटा में से
                    अपनी सुविधा के अनुसार विकल्प चुनें।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


        with col6:

            st.markdown(
                """
                <div class="feature-card">

                    <h3>📊 कृषि डेटा अंतर्दृष्टि</h3>

                    <p>
                    कृषि डेटा को उपयोगी farming insights
                    में बदलने में सहायता।
                    </p>

                </div>
                """,
                unsafe_allow_html=True
            )


# =========================================================
# WEATHER
# =========================================================

elif page in ["Weather", "मौसम"]:

    if language == "English":

        st.title("🌦️ Weather")

        st.info(
            "Choose automatic weather or enter weather information manually."
        )

        weather_mode = st.radio(
            "Select Weather Data Method",
            [
                "Automatic Weather",
                "Manual Weather"
            ]
        )

    else:

        st.title("🌦️ मौसम")

        st.info(
            "Automatic मौसम या Manual मौसम में से कोई एक विकल्प चुनें।"
        )

        weather_mode = st.radio(
            "मौसम डेटा का तरीका चुनें",
            [
                "Automatic मौसम",
                "Manual मौसम"
            ]
        )


    # -----------------------------------------------------
    # AUTOMATIC
    # -----------------------------------------------------

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
            placeholder="Lucknow"
        )


        if st.button(
            "🌦️ Get Weather / मौसम देखें",
            type="primary"
        ):

            if not city.strip():

                st.warning(
                    "Please enter a village or city."
                    if language == "English"
                    else
                    "कृपया गांव या शहर का नाम डालें।"
                )

            else:

                data, error = get_weather(city)

                if error:

                    st.error(error)

                else:

                    st.session_state["weather_data"] = data


        if "weather_data" in st.session_state:

            data = st.session_state["weather_data"]

            rainfall = data.get(
                "rain",
                {}
            ).get(
                "1h",
                0
            )


            st.success(
                f"Weather loaded for {data['name']}."
                if language == "English"
                else
                f"{data['name']} का मौसम लोड हो गया है।"
            )


            col1, col2, col3, col4 = st.columns(4)


            with col1:

                st.metric(
                    "Temperature",
                    f"{data['main']['temp']} °C"
                )


            with col2:

                st.metric(
                    "Humidity",
                    f"{data['main']['humidity']}%"
                )


            with col3:

                st.metric(
                    "Wind",
                    f"{data['wind']['speed']} m/s"
                )


            with col4:

                st.metric(
                    "Rainfall",
                    f"{rainfall} mm"
                )


            st.markdown(
                f"""
                <div class="weather-box">

                    <b>Weather:</b>
                    {data["weather"][0]["description"].title()}

                    <br><br>

                    <b>Location:</b>
                    {data["name"]}

                </div>
                """,
                unsafe_allow_html=True
            )


    # -----------------------------------------------------
    # MANUAL
    # -----------------------------------------------------

    else:

        st.subheader(
            "✍️ Manual Weather"
            if language == "English"
            else
            "✍️ Manual मौसम"
        )

        manual_temperature = st.number_input(
            "Temperature (°C)",
            value=25.0
        )

        manual_humidity = st.number_input(
            "Humidity (%)",
            min_value=0.0,
            max_value=100.0,
            value=70.0
        )

        manual_rainfall = st.number_input(
            "Rainfall (mm)",
            min_value=0.0,
            value=100.0
        )


        st.session_state["manual_weather"] = {

            "temperature":
                manual_temperature,

            "humidity":
                manual_humidity,

            "rainfall":
                manual_rainfall
        }


        st.success(
            "Manual weather data is ready."
            if language == "English"
            else
            "Manual मौसम डेटा तैयार है।"
        )


# =========================================================
# CROP SUGGESTION
# =========================================================

elif page in [
    "Crop Prediction",
    "फसल सुझाव"
]:

    if language == "English":

        st.title("🌱 Crop Suggestion")

        st.write(
            "Provide soil and weather information to receive "
            "an AI-based crop suggestion."
        )

        st.info(
            "Weather data selected below will be used directly "
            "for the crop suggestion."
        )

    else:

        st.title("🌱 फसल सुझाव")

        st.write(
            "मिट्टी और मौसम की जानकारी देकर AI आधारित "
            "फसल सुझाव प्राप्त करें।"
        )

        st.info(
            "नीचे चुना गया मौसम डेटा फसल सुझाव में सीधे इस्तेमाल होगा।"
        )


    # =====================================================
    # WEATHER SOURCE
    # =====================================================

    if language == "English":

        weather_source = st.radio(
            "How do you want to provide weather data?",
            [
                "Automatic Weather",
                "Manual Weather"
            ]
        )

    else:

        weather_source = st.radio(
            "मौसम डेटा कैसे देना चाहते हैं?",
            [
                "Automatic मौसम",
                "Manual मौसम"
            ]
        )


    # =====================================================
    # AUTOMATIC WEATHER
    # =====================================================

    if weather_source in [
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
            placeholder="Lucknow"
        )


        if st.button(
            "🌦️ Load Weather",
            key="load_crop_weather"
        ):

            if not city.strip():

                st.warning(
                    "Please enter village or city."
                    if language == "English"
                    else
                    "कृपया गांव या शहर का नाम डालें।"
                )

            else:

                data, error = get_weather(city)

                if error:

                    st.error(error)

                else:

                    rainfall = data.get(
                        "rain",
                        {}
                    ).get(
                        "1h",
                        0
                    )


                    st.session_state["crop_weather"] = {

                        "temperature":
                            float(data["main"]["temp"]),

                        "humidity":
                            float(data["main"]["humidity"]),

                        "rainfall":
                            float(rainfall)
                    }


                    st.success(
                        f"Weather loaded for {data['name']}."
                        if language == "English"
                        else
                        f"{data['name']} का मौसम लोड हो गया है।"
                    )


        weather = st.session_state.get(
            "crop_weather",
            {
                "temperature": 25.0,
                "humidity": 70.0,
                "rainfall": 100.0
            }
        )


        st.markdown(
            "### 🌦️ Weather Data"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            temperature = st.number_input(
                "Temperature (°C)",
                value=float(
                    weather["temperature"]
                ),
                key="auto_temperature"
            )


        with col2:

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=float(
                    weather["humidity"]
                ),
                key="auto_humidity"
            )


        with col3:

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=float(
                    weather["rainfall"]
                ),
                key="auto_rainfall"
            )


        st.success(
            "Weather data is ready for crop suggestion."
            if language == "English"
            else
            "मौसम डेटा फसल सुझाव के लिए तैयार है।"
        )


    # =====================================================
    # MANUAL WEATHER
    # =====================================================

    else:

        st.subheader(
            "✍️ Manual Weather"
            if language == "English"
            else
            "✍️ Manual मौसम"
        )


        col1, col2, col3 = st.columns(3)


        with col1:

            temperature = st.number_input(
                "Temperature (°C)",
                value=25.0,
                key="manual_temperature_crop"
            )


        with col2:

            humidity = st.number_input(
                "Humidity (%)",
                min_value=0.0,
                max_value=100.0,
                value=70.0,
                key="manual_humidity_crop"
            )


        with col3:

            rainfall = st.number_input(
                "Rainfall (mm)",
                min_value=0.0,
                value=100.0,
                key="manual_rainfall_crop"
            )


        st.success(
            "Manual weather data will be used for crop suggestion."
            if language == "English"
            else
            "Manual मौसम डेटा फसल सुझाव में इस्तेमाल होगा।"
        )


    # =====================================================
    # SOIL INFORMATION
    # =====================================================

    st.subheader(
        "🌱 Soil Information"
        if language == "English"
        else
        "🌱 मिट्टी की जानकारी"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        N = st.number_input(
            "Nitrogen (N)",
            min_value=0.0,
            value=50.0
        )


    with col2:

        P = st.number_input(
            "Phosphorus (P)",
            min_value=0.0,
            value=40.0
        )


    with col3:

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=40.0
        )


    with col4:

        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5
        )


    # =====================================================
    # PREDICT
    # =====================================================

    if st.button(
        "🌱 Get Crop Suggestion / फसल सुझाव लें",
        type="primary"
    ):

        payload = {

            "N": N,
            "P": P,
            "K": K,

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
                    "Prediction received."
                )


                crop_name = clean_crop_name(
                    crop_result
                )


                st.markdown(
                    f"""
                    <div class="result-box">

                        <h2>
                            🌱
                            {"Crop Suggestion"
                             if language == "English"
                             else
                             "फसल सुझाव"}
                        </h2>

                        <h1>
                            {crop_name}
                        </h1>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


            else:

                st.error(
                    f"Crop suggestion failed. "
                    f"({response.status_code})"
                )

                st.code(
                    response.text
                )


        except Exception as e:

            st.error(
                f"API request failed: {e}"
            )


# =========================================================
# YIELD PREDICTION
# =========================================================

elif page in [
    "Yield Prediction",
    "उत्पादन अनुमान"
]:

    if language == "English":

        st.title("🌾 Yield Estimate")

        st.write(
            "Enter crop, state, season and area to estimate agricultural production."
        )

    else:

        st.title("🌾 उत्पादन अनुमान")

        st.write(
            "फसल, राज्य, सीजन और क्षेत्रफल डालकर कृषि उत्पादन का अनुमान लगाएँ।"
        )


    crop = st.text_input(
        "Crop / फसल",
        placeholder="Rice"
    )


    state = st.text_input(
        "State / राज्य",
        placeholder="Uttar Pradesh"
    )


    season = st.text_input(
        "Season / सीजन",
        placeholder="Kharif"
    )


    area = st.number_input(
        "Area / क्षेत्रफल",
        min_value=0.0,
        value=1.0
    )


    st.info(
        "Crop, State and Season should match the labels used during model training."
        if language == "English"
        else
        "Crop, State और Season के नाम model training में इस्तेमाल labels से match होने चाहिए।"
    )


    if st.button(
        "🌾 Get Yield Estimate / उत्पादन अनुमान लें",
        type="primary"
    ):

        if not crop.strip() or not state.strip() or not season.strip():

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
                        "Yield estimate received."
                    )


                    st.markdown(
                        f"""
                        <div class="result-box">

                            <h2>
                                🌾
                                {"Yield Estimate"
                                 if language == "English"
                                 else
                                 "उत्पादन अनुमान"}
                            </h2>

                            <h1>
                                {yield_result}
                            </h1>

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
                        response.text
                    )


            except Exception as e:

                st.error(
                    f"API request failed: {e}"
                )


# =========================================================
# COST PREDICTION
# =========================================================

elif page in [
    "Cost Prediction",
    "लागत अनुमान"
]:

    if language == "English":

        st.title("💰 Cost Estimate")

        st.write(
            "Enter crop, state and yield to estimate agricultural cost."
        )

    else:

        st.title("💰 लागत अनुमान")

        st.write(
            "फसल, राज्य और उत्पादन डालकर कृषि लागत का अनुमान लगाएँ।"
        )


    crop = st.text_input(
        "Crop / फसल",
        placeholder="Rice"
    )


    state = st.text_input(
        "State / राज्य",
        placeholder="Uttar Pradesh"
    )


    yield_value = st.number_input(
        "Yield / उत्पादन",
        min_value=0.0,
        value=10.0
    )


    if st.button(
        "💰 Get Cost Estimate / लागत अनुमान लें",
        type="primary"
    ):

        if not crop.strip() or not state.strip():

            st.warning(
                "Please enter Crop and State."
                if language == "English"
                else
                "कृपया Crop और State डालें।"
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
                        "Cost estimate received."
                    )


                    st.markdown(
                        f"""
                        <div class="result-box">

                            <h2>
                                💰
                                {"Cost Estimate"
                                 if language == "English"
                                 else
                                 "लागत अनुमान"}
                            </h2>

                            <h1>
                                {cost_result}
                            </h1>

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
                        response.text
                    )


            except Exception as e:

                st.error(
                    f"API request failed: {e}"
                )


# =========================================================
# ABOUT
# =========================================================

elif page in [
    "About",
    "हमारे बारे में"
]:

    if language == "English":

        st.title("🌿 About AgriSense AI")

        st.markdown(
            """
            <div class="about-box">

            <h3>Smart Agriculture Decision Support</h3>

            <p>
            AgriSense AI is designed to make agricultural
            information easier to use through modern
            data-driven technology.
            </p>

            <p>
            The platform provides weather information,
            crop suggestions, yield estimates and cost estimates.
            </p>

            <p>
            For crop suggestion, users can choose either
            automatic weather data or manually enter
            temperature, humidity and rainfall.
            </p>

            <p>
            Automatic weather information is fetched using
            the selected village or city and can be reviewed
            before being used for crop suggestion.
            </p>

            </div>
            """,
            unsafe_allow_html=True
        )


    else:

        st.title("🌿 AgriSense AI के बारे में")

        st.markdown(
            """
            <div class="about-box">

            <h3>स्मार्ट कृषि निर्णय सहायता</h3>

            <p>
            AgriSense AI का उद्देश्य आधुनिक data-driven
            technology की मदद से कृषि संबंधी जानकारी
            को आसान बनाना है।
            </p>

            <p>
            यह प्लेटफॉर्म मौसम की जानकारी, फसल सुझाव,
            उत्पादन अनुमान और लागत अनुमान प्रदान करता है।
            </p>

            <p>
            फसल सुझाव के लिए User Automatic मौसम या
            Manual मौसम में से अपनी सुविधा के अनुसार
            कोई भी विकल्प चुन सकता है।
            </p>

            <p>
            Automatic मौसम में गांव या शहर का नाम डालकर
            मौसम की जानकारी प्राप्त की जा सकती है और
            उस जानकारी को फसल सुझाव में इस्तेमाल किया जा सकता है।
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

        🌱 <b>AgriSense AI</b>
        <br>
        Smart Agriculture Decision Support Platform
        <br><br>
        AI • Weather • Crop Suggestion • Yield • Cost

    </div>
    """,
    unsafe_allow_html=True
)