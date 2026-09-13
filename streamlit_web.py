import os
import requests
import streamlit as st


# =========================================================
# CONFIG
# =========================================================

API_URL = "https://agrisense-api.onrender.com"

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
# CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f5f9f4;
}

.block-container {
    padding-top: 1rem;
}

.hero {
    padding: 35px;
    border-radius: 20px;
    background: linear-gradient(135deg, #0b5d3b, #198754);
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 48px;
    margin-bottom: 10px;
}

.hero p {
    font-size: 18px;
}

.card {
    padding: 22px;
    border-radius: 16px;
    background: white;
    border: 1px solid #dce8df;
    min-height: 170px;
    margin-bottom: 20px;
}

.card h3 {
    color: #126b45;
}

.result {
    padding: 25px;
    border-radius: 16px;
    background: #e9f7ef;
    border-left: 6px solid #198754;
}

.about {
    padding: 25px;
    border-radius: 16px;
    background: white;
    border: 1px solid #dce8df;
}

.footer {
    text-align: center;
    padding: 20px;
    margin-top: 40px;
    background: #073b28;
    color: white;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)


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
    ABOUT = "About"

else:

    HOME = "होम"
    WEATHER = "मौसम"
    CROP = "फसल भविष्यवाणी"
    YIELD = "उत्पादन भविष्यवाणी"
    COST = "लागत भविष्यवाणी"
    ABOUT = "हमारे बारे में"


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
        ABOUT
    ]
)


# =========================================================
# HOME
# =========================================================

if page == HOME:

    if language == "English":

        title = "AgriSense AI"
        subtitle = "AI-Powered Agriculture Decision Support System"

        description = """
        AgriSense AI is a smart agriculture platform that uses
        Artificial Intelligence and Machine Learning to help farmers
        make better farming decisions.
        """

    else:

        title = "AgriSense AI"
        subtitle = "AI आधारित कृषि निर्णय सहायता प्रणाली"

        description = """
        AgriSense AI एक स्मार्ट कृषि प्लेटफॉर्म है जो Artificial
        Intelligence और Machine Learning की मदद से किसानों को
        बेहतर कृषि निर्णय लेने में सहायता करता है।
        """

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

    # Agriculture image
    st.image(
        "https://images.unsplash.com/photo-1625246333195-78d9c38ad449"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )

    if language == "English":

        st.header("🌾 Key Features")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="card">
                <h3>🌦️ Weather Information</h3>
                <p>
                Get current weather information for your city
                to support better farming decisions.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card">
                <h3>🌱 Crop Recommendation</h3>
                <p>
                Get AI-based crop recommendations using
                soil and weather conditions.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="card">
                <h3>🌾 Yield Prediction</h3>
                <p>
                Predict expected agricultural yield using
                crop, state, season and area.
                </p>
            </div>
            """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown("""
            <div class="card">
                <h3>💰 Cost Prediction</h3>
                <p>
                Estimate agricultural investment cost
                using crop, state and yield.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown("""
            <div class="card">
                <h3>📊 Smart Dashboard</h3>
                <p>
                A simple and clean dashboard for
                agriculture-related predictions.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown("""
            <div class="card">
                <h3>🤖 Machine Learning</h3>
                <p>
                Machine Learning models provide
                data-driven agricultural predictions.
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.header("🌍 About AgriSense AI")

        st.markdown("""
        <div class="about">

        <p>
        AgriSense AI is designed to bring modern AI technology
        into agriculture. It combines weather information and
        Machine Learning models to provide useful insights
        for crop selection, yield estimation and cost estimation.
        </p>

        <p>
        The main goal is to make agricultural data easier to
        understand and help farmers make smarter decisions.
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.header("🌾 मुख्य विशेषताएँ")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="card">
                <h3>🌦️ मौसम की जानकारी</h3>
                <p>
                अपने शहर के वर्तमान मौसम की जानकारी प्राप्त करें।
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="card">
                <h3>🌱 फसल की सिफारिश</h3>
                <p>
                मिट्टी और मौसम की स्थिति के आधार पर
                AI से फसल की सिफारिश प्राप्त करें।
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="card">
                <h3>🌾 उत्पादन भविष्यवाणी</h3>
                <p>
                फसल, राज्य, सीजन और क्षेत्रफल के आधार पर
                उत्पादन का अनुमान लगाएँ।
                </p>
            </div>
            """, unsafe_allow_html=True)

        col4, col5, col6 = st.columns(3)

        with col4:
            st.markdown("""
            <div class="card">
                <h3>💰 लागत भविष्यवाणी</h3>
                <p>
                फसल, राज्य और उत्पादन के आधार पर
                कृषि निवेश लागत का अनुमान लगाएँ।
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col5:
            st.markdown("""
            <div class="card">
                <h3>📊 स्मार्ट डैशबोर्ड</h3>
                <p>
                कृषि भविष्यवाणियों के लिए आसान और
                साफ-सुथरा डैशबोर्ड।
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col6:
            st.markdown("""
            <div class="card">
                <h3>🤖 Machine Learning</h3>
                <p>
                Machine Learning मॉडल के माध्यम से
                data-driven कृषि भविष्यवाणी।
                </p>
            </div>
            """, unsafe_allow_html=True)

        st.header("🌍 AgriSense AI के बारे में")

        st.markdown("""
        <div class="about">

        <p>
        AgriSense AI का उद्देश्य आधुनिक AI तकनीक को कृषि
        के क्षेत्र में उपयोगी बनाना है। यह मौसम की जानकारी
        और Machine Learning मॉडल को एक साथ उपयोग करके
        फसल चयन, उत्पादन और लागत से संबंधित जानकारी देता है।
        </p>

        <p>
        इसका मुख्य उद्देश्य कृषि संबंधी जानकारी को आसान
        बनाना और किसानों को बेहतर निर्णय लेने में सहायता करना है।
        </p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# WEATHER
# =========================================================

elif page == WEATHER:

    st.title("🌦️ Weather / मौसम")

    city = st.text_input(
        "City / शहर",
        placeholder="Lucknow"
    )

    if st.button("Get Weather / मौसम देखें"):

        if not city.strip():

            st.warning(
                "Please enter a city."
                if language == "English"
                else
                "कृपया शहर का नाम डालें।"
            )

        elif not WEATHER_API_KEY:

            st.error(
                "OpenWeather API key is not configured."
                if language == "English"
                else
                "OpenWeather API key configure नहीं है।"
            )

        else:

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
                            "Weather",
                            data["weather"][0]["description"].title()
                        )

                    st.success(
                        f"Weather data loaded for {data['name']}."
                        if language == "English"
                        else
                        f"{data['name']} के लिए मौसम की जानकारी मिल गई।"
                    )

                else:

                    st.error(
                        f"Weather data could not be fetched. "
                        f"({response.status_code}) "
                        f"{data.get('message', '')}"
                        if language == "English"
                        else
                        f"मौसम की जानकारी प्राप्त नहीं हो सकी। "
                        f"({response.status_code}) "
                        f"{data.get('message', '')}"
                    )

            except Exception as e:

                st.error(
                    f"Weather request failed: {e}"
                    if language == "English"
                    else
                    f"Weather request fail हो गई: {e}"
                )


# =========================================================
# CROP PREDICTION
# FastAPI: POST /predict1
# =========================================================

elif page == CROP:

    st.title("🌱 Crop Prediction / फसल भविष्यवाणी")

    if language == "English":

        st.write(
            "Enter soil nutrients and weather conditions "
            "to get an AI-based crop recommendation."
        )

    else:

        st.write(
            "मिट्टी के पोषक तत्व और मौसम की स्थिति डालकर "
            "AI आधारित फसल की सिफारिश प्राप्त करें।"
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
            value=40.0
        )

        K = st.number_input(
            "Potassium (K)",
            min_value=0.0,
            value=40.0
        )

    with col2:

        temperature = st.number_input(
            "Temperature",
            value=25.0
        )

        humidity = st.number_input(
            "Humidity",
            value=70.0
        )

    with col3:

        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=6.5
        )

        rainfall = st.number_input(
            "Rainfall",
            min_value=0.0,
            value=100.0
        )

    if st.button(
        "🌱 Predict Crop / फसल बताएँ",
        type="primary"
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

        try:

            response = requests.post(
                f"{API_URL}/predict1",
                json=payload,
                timeout=30
            )

            if response.status_code == 200:

                result = response.json()

                st.markdown(
                    f"""
                    <div class="result">
                        <h2>🌾 Prediction Result</h2>
                        <h3>{result.get("predict_crop")}</h3>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            else:

                st.error(
                    f"Crop prediction failed. "
                    f"({response.status_code}) "
                    f"{response.text}"
                )

        except Exception as e:

            st.error(
                f"API request failed: {e}"
            )


# =========================================================
# YIELD PREDICTION
# FastAPI: POST /predict2
# =========================================================

elif page == YIELD:

    st.title("🌾 Yield Prediction / उत्पादन भविष्यवाणी")

    if language == "English":

        st.write(
            "Enter Crop, State, Season and Area "
            "to predict agricultural yield."
        )

    else:

        st.write(
            "Crop, State, Season और Area डालकर "
            "कृषि उत्पादन का अनुमान लगाएँ।"
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
        "Crop, State and Season must match the labels "
        "used during model training."
        if language == "English"
        else
        "Crop, State और Season के नाम model training "
        "में इस्तेमाल किए गए labels से match होने चाहिए।"
    )

    if st.button(
        "🌾 Predict Yield / उत्पादन बताएँ",
        type="primary"
    ):

        if not crop or not state or not season:

            st.warning(
                "Please fill all fields."
                if language == "English"
                else
                "कृपया सभी fields भरें।"
            )

        else:

            payload = {
                "Crop": crop,
                "State": state,
                "Season": season,
                "Area": area
            }

            try:

                response = requests.post(
                    f"{API_URL}/predict2",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    st.markdown(
                        f"""
                        <div class="result">
                            <h2>🌾 Yield Result</h2>
                            <h3>{result.get("predict_yield")}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Yield prediction failed. "
                        f"({response.status_code}) "
                        f"{response.text}"
                    )

            except Exception as e:

                st.error(
                    f"API request failed: {e}"
                )


# =========================================================
# COST PREDICTION
# FastAPI: POST /predict3
# =========================================================

elif page == COST:

    st.title("💰 Cost Prediction / लागत भविष्यवाणी")

    if language == "English":

        st.write(
            "Enter Crop, State and Yield to estimate "
            "agricultural investment cost."
        )

    else:

        st.write(
            "Crop, State और Yield डालकर कृषि निवेश लागत "
            "का अनुमान लगाएँ।"
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
        "💰 Predict Cost / लागत बताएँ",
        type="primary"
    ):

        if not crop or not state:

            st.warning(
                "Please enter Crop and State."
                if language == "English"
                else
                "कृपया Crop और State डालें।"
            )

        else:

            payload = {
                "Crop": crop,
                "State": state,
                "Yield": yield_value
            }

            try:

                response = requests.post(
                    f"{API_URL}/predict3",
                    json=payload,
                    timeout=30
                )

                if response.status_code == 200:

                    result = response.json()

                    st.markdown(
                        f"""
                        <div class="result">
                            <h2>💰 Cost Result</h2>
                            <h3>{result.get("predict_cost")}</h3>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        f"Cost prediction failed. "
                        f"({response.status_code}) "
                        f"{response.text}"
                    )

            except Exception as e:

                st.error(
                    f"API request failed: {e}"
                )


# =========================================================
# ABOUT
# =========================================================

elif page == ABOUT:

    st.title("🌿 About AgriSense AI")

    st.image(
        "https://images.unsplash.com/photo-1495107334309-fcf20504a5ab"
        "?auto=format&fit=crop&w=1600&q=85",
        use_container_width=True
    )

    if language == "English":

        st.markdown("""
        <div class="about">

        <h2>🌱 What is AgriSense AI?</h2>

        <p>
        AgriSense AI is an intelligent agriculture platform
        built to support farmers and agriculture professionals
        with Artificial Intelligence and Machine Learning.
        </p>

        <h3>Our Features</h3>

        <ul>
            <li>🌦️ Weather Information</li>
            <li>🌱 AI Crop Recommendation</li>
            <li>🌾 Yield Prediction</li>
            <li>💰 Agricultural Cost Prediction</li>
            <li>📊 Data-driven Farming Support</li>
        </ul>

        <h3>Our Vision</h3>

        <p>
        Smart Farming → Better Decisions → Better Productivity
        → Sustainable Agriculture
        </p>

        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="about">

        <h2>🌱 AgriSense AI क्या है?</h2>

        <p>
        AgriSense AI एक intelligent agriculture platform है,
        जिसे किसानों और कृषि क्षेत्र से जुड़े लोगों को
        Artificial Intelligence और Machine Learning की मदद
        से बेहतर निर्णय लेने में सहायता करने के लिए बनाया गया है।
        </p>

        <h3>हमारी सुविधाएँ</h3>

        <ul>
            <li>🌦️ मौसम की जानकारी</li>
            <li>🌱 AI फसल सिफारिश</li>
            <li>🌾 उत्पादन भविष्यवाणी</li>
            <li>💰 कृषि लागत भविष्यवाणी</li>
            <li>📊 Data-driven Farming Support</li>
        </ul>

        <h3>हमारा विज़न</h3>

        <p>
        स्मार्ट खेती → बेहतर निर्णय → बेहतर उत्पादकता
        → टिकाऊ कृषि
        </p>

        </div>
        """, unsafe_allow_html=True)


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        🌱 <b>AgriSense AI</b><br>
        Smart Farming • AI • Better Agriculture
    </div>
    """,
    unsafe_allow_html=True
)