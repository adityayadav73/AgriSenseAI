import streamlit as st
import requests

# =========================================================
# CONFIG
# =========================================================

API_URL = "https://agrisense-api.onrender.com"

# Yahan apni OpenWeatherMap API key lagao
WEATHER_API_KEY = "OPENWEATHER_API_KEY"

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide"
)


# =========================================================
# LANGUAGE
# =========================================================

language = st.selectbox(
    "🌐 Language / भाषा",
    ["English", "हिंदी"]
)

if language == "हिंदी":

    TITLE = "🌾 एग्रीसेंस AI"
    SUBTITLE = "कृषि के लिए AI आधारित निर्णय प्रणाली"

    LOCATION = "📍 शहर / जिला"
    GET_WEATHER = "🌦️ मौसम प्राप्त करें"

    SOIL_TITLE = "🧪 मिट्टी की जानकारी"

    N_TEXT = "नाइट्रोजन (N)"
    P_TEXT = "फॉस्फोरस (P)"
    K_TEXT = "पोटैशियम (K)"
    PH_TEXT = "मिट्टी का pH"

    TEMP_TEXT = "तापमान (°C)"
    HUMIDITY_TEXT = "नमी (%)"
    RAINFALL_TEXT = "वर्षा (mm)"

    WEATHER_TITLE = "🌦️ मौसम की जानकारी"

    CROP_TITLE = "🌱 फसल की सिफारिश"
    YIELD_TITLE = "🌾 उत्पादन की भविष्यवाणी"
    COST_TITLE = "💰 लागत की भविष्यवाणी"

    PREDICT_CROP = "🌱 फसल की भविष्यवाणी करें"
    PREDICT_YIELD = "🌾 उत्पादन की भविष्यवाणी करें"
    PREDICT_COST = "💰 लागत की भविष्यवाणी करें"

    DASHBOARD_TITLE = "📊 लाभ / बाजार डैशबोर्ड"

    MARKET_PRICE = "💵 बाजार मूल्य (₹ प्रति यूनिट)"
    CALCULATE_PROFIT = "📈 लाभ की गणना करें"

    SUCCESS_CROP = "फसल की भविष्यवाणी सफल रही! 🌱"
    SUCCESS_YIELD = "उत्पादन की भविष्यवाणी सफल रही! 🌾"
    SUCCESS_COST = "लागत की भविष्यवाणी सफल रही! 💰"

else:

    TITLE = "🌾 AgriSense AI"
    SUBTITLE = "AI-powered decision support for agriculture"

    LOCATION = "📍 City / District"
    GET_WEATHER = "🌦️ Get Weather"

    SOIL_TITLE = "🧪 Soil Information"

    N_TEXT = "Nitrogen (N)"
    P_TEXT = "Phosphorus (P)"
    K_TEXT = "Potassium (K)"
    PH_TEXT = "Soil pH"

    TEMP_TEXT = "Temperature (°C)"
    HUMIDITY_TEXT = "Humidity (%)"
    RAINFALL_TEXT = "Rainfall (mm)"

    WEATHER_TITLE = "🌦️ Weather Information"

    CROP_TITLE = "🌱 Crop Recommendation"
    YIELD_TITLE = "🌾 Yield Prediction"
    COST_TITLE = "💰 Cost Prediction"

    PREDICT_CROP = "🌱 Predict Crop"
    PREDICT_YIELD = "🌾 Predict Yield"
    PREDICT_COST = "💰 Predict Cost"

    DASHBOARD_TITLE = "📊 Profit / Market Dashboard"

    MARKET_PRICE = "💵 Market Price (₹ per unit)"
    CALCULATE_PROFIT = "📈 Calculate Profit"

    SUCCESS_CROP = "Crop Prediction Successful! 🌱"
    SUCCESS_YIELD = "Yield Prediction Successful! 🌾"
    SUCCESS_COST = "Cost Prediction Successful! 💰"


# =========================================================
# HEADER
# =========================================================

st.title(TITLE)
st.write(SUBTITLE)

st.divider()


# =========================================================
# WEATHER
# =========================================================

st.header(WEATHER_TITLE)

city = st.text_input(
    LOCATION,
    placeholder="e.g. Lucknow"
)

if st.button(GET_WEATHER, use_container_width=True):

    if not city:
        st.warning("Please enter City / District.")

    elif WEATHER_API_KEY == "YOUR_OPENWEATHERMAP_API_KEY":
        st.error(
            "OpenWeatherMap API key add karo."
        )

    else:

        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}"
            f"&appid={WEATHER_API_KEY}"
            f"&units=metric"
        )

        try:

            with st.spinner("Fetching weather..."):

                weather_response = requests.get(
                    weather_url,
                    timeout=20
                )

            if weather_response.status_code == 200:

                weather = weather_response.json()

                temperature = weather["main"]["temp"]
                humidity = weather["main"]["humidity"]

                # 1 hour rainfall
                rainfall = weather.get(
                    "rain",
                    {}
                ).get(
                    "1h",
                    0.0
                )

                # Save weather data
                st.session_state["temperature"] = (
                    float(temperature)
                )

                st.session_state["humidity"] = (
                    float(humidity)
                )

                st.session_state["rainfall"] = (
                    float(rainfall)
                )

                st.session_state["weather_city"] = city

                st.success(
                    "Weather data loaded successfully! 🌦️"
                )

            else:

                st.error(
                    "Weather data fetch nahi ho paya."
                )

        except requests.exceptions.RequestException:

            st.error(
                "Weather API se connection nahi ho paya."
            )


# =========================================================
# WEATHER DISPLAY
# =========================================================

if "temperature" in st.session_state:

    st.subheader(
        f"🌦️ {st.session_state.get('weather_city', city)}"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            TEMP_TEXT,
            f"{st.session_state['temperature']:.1f} °C"
        )

    with col2:

        st.metric(
            HUMIDITY_TEXT,
            f"{st.session_state['humidity']:.1f} %"
        )

    with col3:

        st.metric(
            RAINFALL_TEXT,
            f"{st.session_state['rainfall']:.2f} mm"
        )


# =========================================================
# SOIL INPUT
# =========================================================

st.divider()

st.header(SOIL_TITLE)

col1, col2 = st.columns(2)

with col1:

    N = st.number_input(
        N_TEXT,
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    P = st.number_input(
        P_TEXT,
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    K = st.number_input(
        K_TEXT,
        min_value=0.0,
        value=50.0,
        step=1.0
    )

with col2:

    ph = st.number_input(
        PH_TEXT,
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )


# =========================================================
# CHECK WEATHER
# =========================================================

def get_weather_values():

    if "temperature" not in st.session_state:

        st.warning(
            "Pehle Weather Data fetch karein."
        )

        return None

    return {
        "temperature": st.session_state["temperature"],
        "humidity": st.session_state["humidity"],
        "rainfall": st.session_state["rainfall"]
    }


# =========================================================
# CROP PREDICTION
# =========================================================

st.divider()

st.header(CROP_TITLE)

if st.button(
    PREDICT_CROP,
    use_container_width=True
):

    weather_data = get_weather_values()

    if weather_data is not None:

        payload = {

            "N": N,
            "P": P,
            "K": K,

            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],

            "ph": ph,

            "rainfall": weather_data["rainfall"]
        }

        try:

            with st.spinner("Predicting crop..."):

                response = requests.post(
                    f"{API_URL}/predict1",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:

                result = response.json()

                crop = (
                    result.get("predict_crop")
                    or result.get("crop")
                    or result.get("predicted_crop")
                    or result.get("prediction")
                )

                if crop:

                    # Raw API message ko clean karo
                    crop_name = str(crop)

                    if "Recommended crop is" in crop_name:

                        crop_name = crop_name.split(
                            "Recommended crop is",
                            1
                        )[1]

                        crop_name = crop_name.replace(
                            "successfully",
                            ""
                        ).strip()

                    crop_name = crop_name.replace(
                        "[",
                        ""
                    ).replace(
                        "]",
                        ""
                    ).replace(
                        "'",
                        ""
                    ).strip()

                    st.session_state["crop"] = (
                        crop_name
                    )

                    st.success(
                        SUCCESS_CROP
                    )

                    st.subheader(
                        "🌾 Recommended Crop"
                    )

                    st.markdown(
                        f"""
                        <div style="
                            padding: 25px;
                            border-radius: 15px;
                            text-align: center;
                            border: 1px solid
                            rgba(128,128,128,0.3);
                        ">
                            <h1>🌱 {crop_name.title()}</h1>
                            <p>
                            Based on your soil and
                            weather conditions
                            </p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        "Crop result API response mein nahi mila."
                    )

            else:

                st.error(
                    f"Crop API Error: {response.status_code}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Crop API se connection nahi ho paya."
            )


# =========================================================
# YIELD PREDICTION
# =========================================================

st.divider()

st.header(YIELD_TITLE)

if st.button(
    PREDICT_YIELD,
    use_container_width=True
):

    weather_data = get_weather_values()

    if weather_data is not None:

        payload = {

            "N": N,
            "P": P,
            "K": K,

            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],

            "ph": ph,

            "rainfall": weather_data["rainfall"]
        }

        try:

            with st.spinner("Predicting yield..."):

                response = requests.post(
                    f"{API_URL}/predict2",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:

                result = response.json()

                yield_value = (
                    result.get("yield")
                    or result.get("predicted_yield")
                    or result.get("prediction")
                )

                if yield_value is not None:

                    yield_value = float(
                        yield_value
                    )

                    st.session_state["yield"] = (
                        yield_value
                    )

                    st.success(
                        SUCCESS_YIELD
                    )

                    st.metric(
                        "🌾 Expected Yield",
                        f"{yield_value:,.2f}"
                    )

                else:

                    st.error(
                        "Yield result API response mein nahi mila."
                    )

            else:

                st.error(
                    f"Yield API Error: {response.status_code}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Yield API se connection nahi ho paya."
            )


# =========================================================
# COST PREDICTION
# =========================================================

st.divider()

st.header(COST_TITLE)

if st.button(
    PREDICT_COST,
    use_container_width=True
):

    weather_data = get_weather_values()

    if weather_data is not None:

        payload = {

            "N": N,
            "P": P,
            "K": K,

            "temperature": weather_data["temperature"],
            "humidity": weather_data["humidity"],

            "ph": ph,

            "rainfall": weather_data["rainfall"]
        }

        try:

            with st.spinner("Predicting cost..."):

                response = requests.post(
                    f"{API_URL}/predict3",
                    json=payload,
                    timeout=60
                )

            if response.status_code == 200:

                result = response.json()

                cost_value = (
                    result.get("cost")
                    or result.get("predicted_cost")
                    or result.get("prediction")
                )

                if cost_value is not None:

                    cost_value = float(
                        cost_value
                    )

                    st.session_state["cost"] = (
                        cost_value
                    )

                    st.success(
                        SUCCESS_COST
                    )

                    st.metric(
                        "💰 Estimated Cost",
                        f"₹{cost_value:,.2f}"
                    )

                else:

                    st.error(
                        "Cost result API response mein nahi mila."
                    )

            else:

                st.error(
                    f"Cost API Error: {response.status_code}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Cost API se connection nahi ho paya."
            )


# =========================================================
# PROFIT / MARKET DASHBOARD
# =========================================================

st.divider()

st.header(DASHBOARD_TITLE)

market_price = st.number_input(
    MARKET_PRICE,
    min_value=0.0,
    value=0.0,
    step=100.0
)

if st.button(
    CALCULATE_PROFIT,
    use_container_width=True
):

    yield_value = st.session_state.get(
        "yield"
    )

    cost_value = st.session_state.get(
        "cost"
    )

    if yield_value is None:

        st.warning(
            "Pehle Yield Prediction karein."
        )

    elif cost_value is None:

        st.warning(
            "Pehle Cost Prediction karein."
        )

    elif market_price <= 0:

        st.warning(
            "Valid Market Price enter karein."
        )

    else:

        revenue = (
            yield_value * market_price
        )

        profit = (
            revenue - cost_value
        )

        st.subheader(
            "📊 Farm Summary"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🌱 Crop",
                st.session_state.get(
                    "crop",
                    "Not predicted"
                )
            )

        with col2:

            st.metric(
                "🌾 Yield",
                f"{yield_value:,.2f}"
            )

        with col3:

            st.metric(
                "💵 Revenue",
                f"₹{revenue:,.2f}"
            )

        with col4:

            st.metric(
                "📈 Profit",
                f"₹{profit:,.2f}"
            )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

st.divider()

st.header("📊 Model Performance")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "🌱 Crop Model",
        "Accuracy"
    )

    st.caption(
        "Training script se actual accuracy yahan add karein."
    )

with col2:

    st.metric(
        "🌾 Yield Model",
        "R² Score"
    )

    st.caption(
        "Training script se actual R² yahan add karein."
    )

with col3:

    st.metric(
        "💰 Cost Model",
        "R² Score"
    )

    st.caption(
        "Training script se actual R² yahan add karein."
    )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌾 AgriSense AI | AI Agriculture Assistant"
)