import os
import requests
import streamlit as st

# =========================================================
# CONFIG
# =========================================================

API_URL = "https://agrisense-api.onrender.com"

# Render Environment Variable:
# OPENWEATHER_API_KEY
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide"
)

# =========================================================
# LANGUAGE
# =========================================================

language = st.selectbox(
    "Language / भाषा",
    ["English", "हिंदी"]
)

if language == "English":

    TEXT = {
        "title": "🌾 AgriSense AI",
        "subtitle": "AI-powered agriculture decision support system",
        "weather": "🌦️ Weather Information",
        "city": "City / District",
        "get_weather": "Get Weather",
        "temperature": "Temperature",
        "humidity": "Humidity",
        "rainfall": "Rainfall",
        "soil": "🧪 Soil Information",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "Soil pH",
        "crop": "🌱 Crop Recommendation",
        "predict_crop": "Predict Crop",
        "yield": "🌾 Yield Prediction",
        "predict_yield": "Predict Yield",
        "cost": "💰 Cost Prediction",
        "predict_cost": "Predict Cost",
        "dashboard": "📊 Profit / Market Dashboard",
        "market_price": "Market Price (₹ per unit)",
        "calculate": "Calculate Profit",
        "revenue": "Estimated Revenue",
        "profit": "Estimated Profit",
        "expected_yield": "Expected Yield",
        "estimated_cost": "Estimated Cost",
        "success_weather": "Weather data fetched successfully!",
        "success_crop": "Crop prediction successful!",
        "success_yield": "Yield prediction successful!",
        "success_cost": "Cost prediction successful!",
        "weather_first": "Please get weather data first.",
        "api_error": "Weather data could not be fetched.",
        "invalid_city": "Please enter a city or district.",
        "invalid_key": "Weather API key is not configured.",
        "connection_error": "Could not connect to the weather API."
    }

else:

    TEXT = {
        "title": "🌾 एग्रीसेंस AI",
        "subtitle": "कृषि के लिए AI आधारित निर्णय प्रणाली",
        "weather": "🌦️ मौसम की जानकारी",
        "city": "शहर / जिला",
        "get_weather": "मौसम प्राप्त करें",
        "temperature": "तापमान",
        "humidity": "नमी",
        "rainfall": "वर्षा",
        "soil": "🧪 मिट्टी की जानकारी",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "ph": "मिट्टी का pH",
        "crop": "🌱 फसल की सिफारिश",
        "predict_crop": "फसल की भविष्यवाणी करें",
        "yield": "🌾 उत्पादन की भविष्यवाणी",
        "predict_yield": "उत्पादन की भविष्यवाणी करें",
        "cost": "💰 लागत की भविष्यवाणी",
        "predict_cost": "लागत की भविष्यवाणी करें",
        "dashboard": "📊 लाभ / बाजार डैशबोर्ड",
        "market_price": "बाजार मूल्य (₹ प्रति यूनिट)",
        "calculate": "लाभ की गणना करें",
        "revenue": "अनुमानित आय",
        "profit": "अनुमानित लाभ",
        "expected_yield": "अनुमानित उत्पादन",
        "estimated_cost": "अनुमानित लागत",
        "success_weather": "मौसम की जानकारी सफलतापूर्वक प्राप्त हुई!",
        "success_crop": "फसल की भविष्यवाणी सफल रही!",
        "success_yield": "उत्पादन की भविष्यवाणी सफल रही!",
        "success_cost": "लागत की भविष्यवाणी सफल रही!",
        "weather_first": "कृपया पहले मौसम की जानकारी प्राप्त करें।",
        "api_error": "मौसम की जानकारी प्राप्त नहीं हो सकी।",
        "invalid_city": "कृपया शहर या जिले का नाम दर्ज करें।",
        "invalid_key": "Weather API key सेट नहीं है।",
        "connection_error": "Weather API से कनेक्शन नहीं हो सका।"
    }


# =========================================================
# HEADER
# =========================================================

st.title(TEXT["title"])
st.caption(TEXT["subtitle"])

st.divider()


# =========================================================
# WEATHER
# =========================================================

st.header(TEXT["weather"])

city = st.text_input(
    TEXT["city"],
    placeholder="Lucknow"
)

if st.button(
    TEXT["get_weather"],
    use_container_width=True
):

    if not city:
        st.warning(TEXT["invalid_city"])

    elif not WEATHER_API_KEY:
        st.error(TEXT["invalid_key"])

    else:

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        try:

            with st.spinner("Fetching weather..."):

                response = requests.get(
                    url,
                    params=params,
                    timeout=20
                )

            if response.status_code == 200:

                weather = response.json()

                temperature = weather["main"]["temp"]
                humidity = weather["main"]["humidity"]

                rainfall = weather.get(
                    "rain",
                    {}
                ).get(
                    "1h",
                    0.0
                )

                st.session_state["temperature"] = float(
                    temperature
                )

                st.session_state["humidity"] = float(
                    humidity
                )

                st.session_state["rainfall"] = float(
                    rainfall
                )

                st.session_state["weather_city"] = city

                st.success(TEXT["success_weather"])

            else:

                # User ko technical/raw API response nahi dikhayenge
                st.error(
                    TEXT["api_error"]
                )

        except requests.RequestException:

            st.error(
                TEXT["connection_error"]
            )


# =========================================================
# WEATHER DISPLAY
# =========================================================

if "temperature" in st.session_state:

    st.subheader(
        st.session_state.get(
            "weather_city",
            city
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            f"🌡️ {TEXT['temperature']}",
            f"{st.session_state['temperature']:.1f} °C"
        )

    with col2:
        st.metric(
            f"💧 {TEXT['humidity']}",
            f"{st.session_state['humidity']:.1f} %"
        )

    with col3:
        st.metric(
            f"🌧️ {TEXT['rainfall']}",
            f"{st.session_state['rainfall']:.2f} mm"
        )


# =========================================================
# SOIL INPUT
# =========================================================

st.divider()

st.header(TEXT["soil"])

col1, col2 = st.columns(2)

with col1:

    N = st.number_input(
        TEXT["nitrogen"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    P = st.number_input(
        TEXT["phosphorus"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    K = st.number_input(
        TEXT["potassium"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

with col2:

    ph = st.number_input(
        TEXT["ph"],
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )


# =========================================================
# COMMON PAYLOAD
# =========================================================

def create_payload():

    if "temperature" not in st.session_state:
        return None

    return {
        "N": N,
        "P": P,
        "K": K,
        "temperature": st.session_state["temperature"],
        "humidity": st.session_state["humidity"],
        "ph": ph,
        "rainfall": st.session_state["rainfall"]
    }


# =========================================================
# CROP PREDICTION
# =========================================================

st.divider()

st.header(TEXT["crop"])

if st.button(
    TEXT["predict_crop"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(TEXT["weather_first"])

    else:

        try:

            with st.spinner("Predicting..."):

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

                    crop_name = str(crop)

                    # API ke message ko clean karna
                    crop_name = crop_name.replace(
                        "Recommended crop is",
                        ""
                    )

                    crop_name = crop_name.replace(
                        "successfully",
                        ""
                    )

                    crop_name = crop_name.replace(
                        "[",
                        ""
                    )

                    crop_name = crop_name.replace(
                        "]",
                        ""
                    )

                    crop_name = crop_name.replace(
                        "'",
                        ""
                    )

                    crop_name = crop_name.strip()

                    st.session_state["crop"] = crop_name

                    st.success(
                        TEXT["success_crop"]
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
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(
                        "Crop prediction result was not received."
                        if language == "English"
                        else
                        "फसल की भविष्यवाणी का परिणाम प्राप्त नहीं हुआ।"
                    )

            else:

                st.error(
                    "Crop prediction failed."
                    if language == "English"
                    else
                    "फसल की भविष्यवाणी असफल रही।"
                )

        except requests.RequestException:

            st.error(
                "Could not connect to prediction server."
                if language == "English"
                else
                "Prediction server से कनेक्शन नहीं हो सका।"
            )


# =========================================================
# YIELD PREDICTION
# =========================================================

st.divider()

st.header(TEXT["yield"])

if st.button(
    TEXT["predict_yield"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(TEXT["weather_first"])

    else:

        try:

            with st.spinner("Predicting..."):

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

                    st.session_state["yield"] = yield_value

                    st.success(
                        TEXT["success_yield"]
                    )

                    st.metric(
                        f"🌾 {TEXT['expected_yield']}",
                        f"{yield_value:,.2f}"
                    )

                else:

                    st.error(
                        "Yield prediction result was not received."
                        if language == "English"
                        else
                        "उत्पादन की भविष्यवाणी का परिणाम प्राप्त नहीं हुआ।"
                    )

            else:

                st.error(
                    "Yield prediction failed."
                    if language == "English"
                    else
                    "उत्पादन की भविष्यवाणी असफल रही।"
                )

        except requests.RequestException:

            st.error(
                "Could not connect to prediction server."
                if language == "English"
                else
                "Prediction server से कनेक्शन नहीं हो सका।"
            )


# =========================================================
# COST PREDICTION
# =========================================================

st.divider()

st.header(TEXT["cost"])

if st.button(
    TEXT["predict_cost"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(TEXT["weather_first"])

    else:

        try:

            with st.spinner("Predicting..."):

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

                    st.session_state["cost"] = cost_value

                    st.success(
                        TEXT["success_cost"]
                    )

                    st.metric(
                        f"💰 {TEXT['estimated_cost']}",
                        f"₹{cost_value:,.2f}"
                    )

                else:

                    st.error(
                        "Cost prediction result was not received."
                        if language == "English"
                        else
                        "लागत की भविष्यवाणी का परिणाम प्राप्त नहीं हुआ।"
                    )

            else:

                st.error(
                    "Cost prediction failed."
                    if language == "English"
                    else
                    "लागत की भविष्यवाणी असफल रही।"
                )

        except requests.RequestException:

            st.error(
                "Could not connect to prediction server."
                if language == "English"
                else
                "Prediction server से कनेक्शन नहीं हो सका।"
            )


# =========================================================
# PROFIT DASHBOARD
# =========================================================

st.divider()

st.header(TEXT["dashboard"])

market_price = st.number_input(
    TEXT["market_price"],
    min_value=0.0,
    value=0.0,
    step=100.0
)

if st.button(
    TEXT["calculate"],
    use_container_width=True
):

    yield_value = st.session_state.get("yield")
    cost_value = st.session_state.get("cost")
    crop_name = st.session_state.get("crop")

    if yield_value is None:

        st.warning(
            "Please predict yield first."
            if language == "English"
            else
            "कृपया पहले उत्पादन की भविष्यवाणी करें।"
        )

    elif cost_value is None:

        st.warning(
            "Please predict cost first."
            if language == "English"
            else
            "कृपया पहले लागत की भविष्यवाणी करें।"
        )

    elif market_price <= 0:

        st.warning(
            "Please enter a valid market price."
            if language == "English"
            else
            "कृपया सही बाजार मूल्य दर्ज करें।"
        )

    else:

        revenue = yield_value * market_price
        profit = revenue - cost_value

        st.subheader(
            "Farm Summary"
            if language == "English"
            else
            "कृषि सारांश"
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🌱 Crop" if language == "English"
                else "🌱 फसल",
                crop_name or "N/A"
            )

        with col2:

            st.metric(
                f"🌾 {TEXT['expected_yield']}",
                f"{yield_value:,.2f}"
            )

        with col3:

            st.metric(
                f"💵 {TEXT['revenue']}",
                f"₹{revenue:,.2f}"
            )

        with col4:

            st.metric(
                f"📈 {TEXT['profit']}",
                f"₹{profit:,.2f}"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌾 AgriSense AI | AI Agriculture Assistant"
)