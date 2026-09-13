import os
import requests
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌾",
    layout="wide"
)

# =========================================================
# CONFIG
# =========================================================

API_URL = "https://agrisense-api.onrender.com"
WEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

# =========================================================
# LANGUAGE
# =========================================================

language = st.selectbox(
    "Language / भाषा",
    ["English", "हिंदी"]
)

if language == "English":

    T = {
        "title": "🌾 AgriSense AI",
        "subtitle": "AI-powered agriculture decision support system",

        "weather": "🌦️ Weather Information",
        "city": "City / District",
        "city_placeholder": "Enter city or district",
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

        "weather_success": "Weather data fetched successfully!",
        "weather_error": "Weather data could not be fetched.",
        "weather_key_error": "Weather API key is not configured.",
        "city_error": "Please enter a city or district.",
        "connection_error": "Could not connect to the weather service.",

        "crop_success": "Crop prediction successful!",
        "crop_error": "Crop prediction failed.",
        "yield_success": "Yield prediction successful!",
        "yield_error": "Yield prediction failed.",
        "cost_success": "Cost prediction successful!",
        "cost_error": "Cost prediction failed.",

        "weather_first": "Please get weather data first.",
        "predict_yield_first": "Please predict yield first.",
        "predict_cost_first": "Please predict cost first.",
        "price_error": "Please enter a valid market price.",

        "crop_result": "Recommended Crop",
        "server_error": "Could not connect to prediction server."
    }

else:

    T = {
        "title": "🌾 एग्रीसेंस AI",
        "subtitle": "कृषि के लिए AI आधारित निर्णय प्रणाली",

        "weather": "🌦️ मौसम की जानकारी",
        "city": "शहर / जिला",
        "city_placeholder": "शहर या जिले का नाम दर्ज करें",
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

        "weather_success": "मौसम की जानकारी सफलतापूर्वक प्राप्त हुई!",
        "weather_error": "मौसम की जानकारी प्राप्त नहीं हो सकी।",
        "weather_key_error": "Weather API key सेट नहीं है।",
        "city_error": "कृपया शहर या जिले का नाम दर्ज करें।",
        "connection_error": "Weather service से कनेक्शन नहीं हो सका।",

        "crop_success": "फसल की भविष्यवाणी सफल रही!",
        "crop_error": "फसल की भविष्यवाणी असफल रही।",
        "yield_success": "उत्पादन की भविष्यवाणी सफल रही!",
        "yield_error": "उत्पादन की भविष्यवाणी असफल रही।",
        "cost_success": "लागत की भविष्यवाणी सफल रही!",
        "cost_error": "लागत की भविष्यवाणी असफल रही।",

        "weather_first": "कृपया पहले मौसम की जानकारी प्राप्त करें।",
        "predict_yield_first": "कृपया पहले उत्पादन की भविष्यवाणी करें।",
        "predict_cost_first": "कृपया पहले लागत की भविष्यवाणी करें।",
        "price_error": "कृपया सही बाजार मूल्य दर्ज करें।",

        "crop_result": "सुझाई गई फसल",
        "server_error": "Prediction server से कनेक्शन नहीं हो सका।"
    }


# =========================================================
# HEADER
# =========================================================

st.title(T["title"])
st.caption(T["subtitle"])

st.divider()


# =========================================================
# WEATHER SECTION
# =========================================================

st.header(T["weather"])

city = st.text_input(
    T["city"],
    placeholder=T["city_placeholder"]
)

if st.button(
    T["get_weather"],
    use_container_width=True
):

    if not city.strip():

        st.warning(T["city_error"])

    elif not WEATHER_API_KEY:

        st.error(T["weather_key_error"])

    else:

        weather_url = (
            "https://api.openweathermap.org/data/2.5/weather"
        )

        weather_params = {
            "q": city.strip(),
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }

        try:

            with st.spinner(
                "Fetching weather..."
                if language == "English"
                else
                "मौसम की जानकारी प्राप्त की जा रही है..."
            ):

                weather_response = requests.get(
                    weather_url,
                    params=weather_params,
                    timeout=20
                )

            if weather_response.status_code == 200:

                weather_data = weather_response.json()

                temperature = weather_data["main"]["temp"]
                humidity = weather_data["main"]["humidity"]

                # OpenWeather rain data may not always exist
                rainfall = weather_data.get(
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

                st.session_state["weather_city"] = city.strip()

                st.success(T["weather_success"])

            else:

                # Clean user-facing error
                if weather_response.status_code == 401:
                    st.error(
                        "Invalid Weather API key."
                        if language == "English"
                        else
                        "Weather API key सही नहीं है।"
                    )

                elif weather_response.status_code == 404:
                    st.error(
                        "City not found."
                        if language == "English"
                        else
                        "शहर नहीं मिला।"
                    )

                else:
                    st.error(
                        f"{T['weather_error']} "
                        f"({weather_response.status_code})"
                    )

        except requests.RequestException:

            st.error(T["connection_error"])


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
            f"🌡️ {T['temperature']}",
            f"{st.session_state['temperature']:.1f} °C"
        )

    with col2:
        st.metric(
            f"💧 {T['humidity']}",
            f"{st.session_state['humidity']:.1f} %"
        )

    with col3:
        st.metric(
            f"🌧️ {T['rainfall']}",
            f"{st.session_state['rainfall']:.2f} mm"
        )


# =========================================================
# SOIL INFORMATION
# =========================================================

st.divider()

st.header(T["soil"])

col1, col2 = st.columns(2)

with col1:

    nitrogen = st.number_input(
        T["nitrogen"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    phosphorus = st.number_input(
        T["phosphorus"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

    potassium = st.number_input(
        T["potassium"],
        min_value=0.0,
        value=50.0,
        step=1.0
    )

with col2:

    soil_ph = st.number_input(
        T["ph"],
        min_value=0.0,
        max_value=14.0,
        value=6.5,
        step=0.1
    )


# =========================================================
# CREATE MODEL PAYLOAD
# =========================================================

def create_payload():

    if "temperature" not in st.session_state:
        return None

    return {
        "N": nitrogen,
        "P": phosphorus,
        "K": potassium,
        "temperature": st.session_state["temperature"],
        "humidity": st.session_state["humidity"],
        "ph": soil_ph,
        "rainfall": st.session_state["rainfall"]
    }


# =========================================================
# CROP PREDICTION
# =========================================================

st.divider()

st.header(T["crop"])

if st.button(
    T["predict_crop"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(T["weather_first"])

    else:

        try:

            with st.spinner(
                "Predicting crop..."
                if language == "English"
                else
                "फसल की भविष्यवाणी की जा रही है..."
            ):

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

                if crop is not None:

                    crop_name = str(crop)

                    st.session_state["crop"] = crop_name

                    st.success(T["crop_success"])

                    st.markdown(
                        f"""
                        <div style="
                            padding: 25px;
                            border-radius: 15px;
                            border: 1px solid
                            rgba(128,128,128,0.3);
                            text-align: center;
                        ">
                            <h2>🌱 {T["crop_result"]}</h2>
                            <h1>{crop_name.title()}</h1>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                else:

                    st.error(T["crop_error"])

            else:

                st.error(
                    f"{T['crop_error']} "
                    f"({response.status_code})"
                )

        except requests.RequestException:

            st.error(T["server_error"])


# =========================================================
# YIELD PREDICTION
# =========================================================

st.divider()

st.header(T["yield"])

if st.button(
    T["predict_yield"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(T["weather_first"])

    else:

        try:

            with st.spinner(
                "Predicting yield..."
                if language == "English"
                else
                "उत्पादन की भविष्यवाणी की जा रही है..."
            ):

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

                    yield_value = float(yield_value)

                    st.session_state["yield"] = yield_value

                    st.success(T["yield_success"])

                    st.metric(
                        f"🌾 {T['expected_yield']}",
                        f"{yield_value:,.2f}"
                    )

                else:

                    st.error(T["yield_error"])

            else:

                st.error(
                    f"{T['yield_error']} "
                    f"({response.status_code})"
                )

        except requests.RequestException:

            st.error(T["server_error"])


# =========================================================
# COST PREDICTION
# =========================================================

st.divider()

st.header(T["cost"])

if st.button(
    T["predict_cost"],
    use_container_width=True
):

    payload = create_payload()

    if payload is None:

        st.warning(T["weather_first"])

    else:

        try:

            with st.spinner(
                "Predicting cost..."
                if language == "English"
                else
                "लागत की भविष्यवाणी की जा रही है..."
            ):

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

                    cost_value = float(cost_value)

                    st.session_state["cost"] = cost_value

                    st.success(T["cost_success"])

                    st.metric(
                        f"💰 {T['estimated_cost']}",
                        f"₹{cost_value:,.2f}"
                    )

                else:

                    st.error(T["cost_error"])

            else:

                st.error(
                    f"{T['cost_error']} "
                    f"({response.status_code})"
                )

        except requests.RequestException:

            st.error(T["server_error"])


# =========================================================
# PROFIT / MARKET DASHBOARD
# =========================================================

st.divider()

st.header(T["dashboard"])

market_price = st.number_input(
    T["market_price"],
    min_value=0.0,
    value=0.0,
    step=100.0
)

if st.button(
    T["calculate"],
    use_container_width=True
):

    yield_value = st.session_state.get("yield")
    cost_value = st.session_state.get("cost")
    crop_name = st.session_state.get("crop")

    if yield_value is None:

        st.warning(T["predict_yield_first"])

    elif cost_value is None:

        st.warning(T["predict_cost_first"])

    elif market_price <= 0:

        st.warning(T["price_error"])

    else:

        revenue = yield_value * market_price
        profit = revenue - cost_value

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(
                "🌱 Crop"
                if language == "English"
                else
                "🌱 फसल",
                crop_name or "N/A"
            )

        with col2:

            st.metric(
                f"🌾 {T['expected_yield']}",
                f"{yield_value:,.2f}"
            )

        with col3:

            st.metric(
                f"💵 {T['revenue']}",
                f"₹{revenue:,.2f}"
            )

        with col4:

            st.metric(
                f"📈 {T['profit']}",
                f"₹{profit:,.2f}"
            )


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🌾 AgriSense AI | AI Agriculture Assistant"
)