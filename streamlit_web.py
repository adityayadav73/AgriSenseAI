import os
import re
import requests
import streamlit as st

# =========================================================
# AGRISENSE AI - STREAMLIT FRONTEND
# =========================================================

st.set_page_config(
    page_title="AgriSense AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "https://agrisenseai-n621.onrender.com"
).rstrip("/")

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")


# =========================================================
# SESSION STATE
# =========================================================

if "language" not in st.session_state:
    st.session_state.language = "English"

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "weather_data" not in st.session_state:
    st.session_state.weather_data = {
        "temperature": 25.0,
        "humidity": 70.0,
        "rainfall": 0.0,
        "village": "",
        "district": "",
        "state": "",
        "city": "",
    }


# =========================================================
# TRANSLATIONS
# =========================================================

T = {
    "English": {
        "home": "Home",
        "weather": "Weather",
        "crop": "Crop Suggestion",
        "yield": "Yield Estimate",
        "cost": "Cost Estimate",
        "profit": "Profit Estimate",
        "about": "About",
        "language": "Language",

        "welcome": "Welcome to",
        "tagline":
            "Get the best crop suggestions, weather insights and "
            "financial estimates for a more profitable farming future.",

        "better": "Better Decisions",
        "productivity": "Higher Productivity",
        "profitability": "More Profitability",

        "crop_desc":
            "Get the best crop for your land and weather conditions.",
        "weather_desc":
            "Get weather data for your location or enter manually.",
        "yield_desc":
            "Estimate your expected crop yield.",
        "cost_desc":
            "Know your cultivation cost per hectare.",
        "profit_desc":
            "Calculate your expected profit.",

        "location": "Location Details",
        "village": "Village",
        "district": "District",
        "state": "State",
        "get_weather": "Get Weather",

        "automatic": "Automatic Weather",
        "manual": "Manual Weather",

        "soil": "Soil Information",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "ph": "pH",

        "temperature": "Temperature",
        "humidity": "Humidity",
        "rainfall": "Rainfall",

        "current_weather": "Current Weather",
        "crop_button": "Get Crop Suggestion",
        "crop_result": "Recommended Crop",

        "season": "Season",
        "area": "Area (Hectare)",
        "yield_input": "Yield (Quintal/Hectare)",
        "estimate_yield": "Estimate Yield",
        "yield_result": "Estimated Yield",

        "estimate_cost": "Estimate Cost",
        "cost_result": "Estimated Cultivation Cost",

        "cultivation_cost": "Cultivation Cost (₹/Hectare)",
        "selling_price": "Selling Price (₹/Quintal)",
        "calculate_profit": "Calculate Profit",
        "revenue": "Total Revenue (₹/Hectare)",
        "profit_result": "Estimated Profit (₹/Hectare)",

        "why": "Why it works?",
        "why_text":
            "Weather, soil and nutrient data help us find the "
            "most suitable crop for your farm.",

        "about_title": "About AgriSense AI",
        "about_text":
            "AgriSense AI is an agriculture decision-support platform "
            "that combines machine learning, weather information and "
            "financial estimates to help farmers make better decisions.",
    },

    "Hindi": {
        "home": "होम",
        "weather": "मौसम",
        "crop": "फसल सुझाव",
        "yield": "उत्पादन अनुमान",
        "cost": "लागत अनुमान",
        "profit": "लाभ अनुमान",
        "about": "हमारे बारे में",
        "language": "भाषा",

        "welcome": "AgriSense AI में आपका स्वागत है",
        "tagline":
            "बेहतर और लाभदायक खेती के लिए फसल सुझाव, मौसम जानकारी "
            "और वित्तीय अनुमान प्राप्त करें।",

        "better": "बेहतर निर्णय",
        "productivity": "अधिक उत्पादन",
        "profitability": "अधिक लाभ",

        "crop_desc":
            "आपकी जमीन और मौसम के अनुसार सबसे उपयुक्त फसल चुनें।",
        "weather_desc":
            "अपने स्थान का मौसम प्राप्त करें या मौसम की जानकारी स्वयं भरें।",
        "yield_desc":
            "अपेक्षित फसल उत्पादन का अनुमान लगाएं।",
        "cost_desc":
            "प्रति हेक्टेयर खेती की लागत जानें।",
        "profit_desc":
            "अपेक्षित लाभ की गणना करें।",

        "location": "स्थान की जानकारी",
        "village": "गाँव",
        "district": "जिला",
        "state": "राज्य",
        "get_weather": "मौसम प्राप्त करें",

        "automatic": "स्वचालित मौसम",
        "manual": "मैनुअल मौसम",

        "soil": "मिट्टी की जानकारी",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फॉस्फोरस (P)",
        "potassium": "पोटैशियम (K)",
        "ph": "pH",

        "temperature": "तापमान",
        "humidity": "नमी",
        "rainfall": "वर्षा",

        "current_weather": "वर्तमान मौसम",
        "crop_button": "फसल सुझाव प्राप्त करें",
        "crop_result": "सुझाई गई फसल",

        "season": "सीजन",
        "area": "क्षेत्रफल (हेक्टेयर)",
        "yield_input": "उत्पादन (क्विंटल/हेक्टेयर)",
        "estimate_yield": "उत्पादन अनुमान करें",
        "yield_result": "अनुमानित उत्पादन",

        "estimate_cost": "लागत अनुमान करें",
        "cost_result": "अनुमानित खेती लागत",

        "cultivation_cost": "खेती लागत (₹/हेक्टेयर)",
        "selling_price": "बिक्री मूल्य (₹/क्विंटल)",
        "calculate_profit": "लाभ की गणना करें",
        "revenue": "कुल आय (₹/हेक्टेयर)",
        "profit_result": "अनुमानित लाभ (₹/हेक्टेयर)",

        "why": "यह कैसे काम करता है?",
        "why_text":
            "मौसम, मिट्टी और पोषक तत्वों की जानकारी आपकी खेती "
            "के लिए सबसे उपयुक्त फसल खोजने में मदद करती है।",

        "about_title": "AgriSense AI के बारे में",
        "about_text":
            "AgriSense AI एक कृषि निर्णय-सहायता प्लेटफॉर्म है जो "
            "मशीन लर्निंग, मौसम की जानकारी और वित्तीय अनुमान को "
            "जोड़कर बेहतर कृषि निर्णय लेने में मदद करता है।",
    }
}

L = T[st.session_state.language]


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: #f5faf7;
    }

    [data-testid="stAppViewContainer"] {
        background:
        radial-gradient(
            circle at 85% 5%,
            rgba(70,180,110,0.10),
            transparent 25%
        ),
        #f5faf7;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 1rem;
    }

    /* SIDEBAR */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #064638 0%,
            #022f28 100%
        );
        min-width: 270px;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    .brand {
        text-align: center;
        padding: 10px 5px 25px 5px;
    }

    .brand-icon {
        font-size: 45px;
    }

    .brand-title {
        font-size: 27px;
        font-weight: 800;
    }

    .brand-title span {
        color: #72db42;
    }

    .brand-subtitle {
        font-size: 11px;
        opacity: 0.8;
    }

    section[data-testid="stSidebar"] .stButton button {
        background: transparent;
        border: none;
        color: white;
        text-align: left;
        border-radius: 12px;
        font-weight: 650;
        margin: 3px 0;
        min-height: 45px;
    }

    section[data-testid="stSidebar"] .stButton button:hover {
        background: rgba(255,255,255,0.12);
        color: white;
    }

    .sidebar-note {
        text-align: center;
        margin-top: 70px;
        font-size: 18px;
        font-style: italic;
        line-height: 1.5;
        opacity: 0.85;
    }

    /* HERO */

    .hero {
        min-height: 245px;
        border-radius: 22px;
        padding: 35px 40px;
        margin-bottom: 22px;

        background:
        linear-gradient(
            90deg,
            rgba(235,252,243,0.98) 0%,
            rgba(235,252,243,0.90) 38%,
            rgba(235,252,243,0.30) 70%,
            rgba(235,252,243,0.03) 100%
        ),
        url(
            "https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=1600&q=85"
        );

        background-size: cover;
        background-position: center;

        box-shadow:
            0 10px 35px rgba(12,72,52,0.10);
    }

    .hero h1 {
        font-size: 38px;
        color: #073d32;
        font-weight: 800;
        margin: 0;
    }

    .hero h1 span {
        color: #15934d;
    }

    .hero p {
        max-width: 560px;
        color: #20594a;
        font-size: 16px;
        line-height: 1.55;
    }

    .hero-pills {
        display: flex;
        gap: 25px;
        flex-wrap: wrap;
    }

    .hero-pill {
        display: flex;
        align-items: center;
        gap: 8px;
        color: #145340;
        font-weight: 700;
    }

    .hero-pill-icon {
        width: 36px;
        height: 36px;
        border-radius: 10px;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* FEATURE CARDS */

    .feature-card {
        min-height: 140px;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid rgba(0,0,0,0.06);
        box-shadow: 0 7px 22px rgba(22,73,56,0.06);
    }

    .green {
        background: #f1fff5;
        border-color: #9ddcb2;
    }

    .blue {
        background: #eff9ff;
        border-color: #c2e7fb;
    }

    .yellow {
        background: #fffaf0;
        border-color: #f3dfae;
    }

    .pink {
        background: #fff4f9;
        border-color: #f1c8da;
    }

    .purple {
        background: #f8f3ff;
        border-color: #dfccfa;
    }

    .feature-title {
        color: #173f34;
        font-size: 16px;
        font-weight: 800;
    }

    .feature-text {
        color: #5b716a;
        font-size: 13px;
        line-height: 1.5;
        margin-top: 15px;
    }

    /* SECTION */

    .section-card {
        background: rgba(255,255,255,0.95);
        border: 1px solid #dcece5;
        border-radius: 20px;
        padding: 22px;
        box-shadow: 0 7px 24px rgba(16,78,55,0.055);
        margin-bottom: 20px;
    }

    .page-title {
        font-size: 34px;
        font-weight: 800;
        color: #083c32;
        margin-bottom: 0;
    }

    .page-description {
        color: #58736a;
        font-size: 15px;
        margin-bottom: 20px;
    }

    .section-heading {
        font-size: 23px;
        font-weight: 800;
        color: #0a4637;
    }

    .mini-heading {
        font-size: 16px;
        font-weight: 800;
        color: #0a4c3a;
        margin: 8px 0 10px 0;
    }

    /* WEATHER */

    .weather-card {
        border-radius: 17px;
        padding: 20px;
        background:
        linear-gradient(
            rgba(222,245,255,0.91),
            rgba(222,245,255,0.84)
        ),
        url(
            "https://images.unsplash.com/photo-1501691223387-dd0500403074?auto=format&fit=crop&w=900&q=80"
        );

        background-size: cover;
        background-position: center;

        border: 1px solid #c8e8f3;
        margin-bottom: 10px;
    }

    .weather-title {
        font-size: 18px;
        font-weight: 800;
        color: #073e36;
        margin-bottom: 15px;
    }

    .weather-value {
        background: rgba(255,255,255,0.84);
        border-radius: 12px;
        padding: 12px 5px;
        text-align: center;
    }

    .weather-number {
        font-size: 20px;
        font-weight: 800;
        color: #0c3442;
    }

    .weather-label {
        font-size: 11px;
        color: #50717c;
    }

    /* INFO */

    .info-box {
        border-radius: 16px;
        background: #effbf5;
        border: 1px solid #c9ead9;
        padding: 18px;
        margin-top: 15px;
    }

    .info-title {
        color: #0a5b42;
        font-weight: 800;
        font-size: 16px;
    }

    .info-text {
        color: #235746;
        font-size: 13px;
        line-height: 1.55;
        margin-top: 5px;
    }

    /* RESULT */

    .result-box {
        border-radius: 17px;
        padding: 20px;
        background: linear-gradient(
            135deg,
            #eafbf1,
            #f7fff9
        );
        border: 1px solid #a9dfbf;
        margin-top: 18px;
        text-align: center;
    }

    .result-label {
        color: #54786b;
        font-size: 13px;
        font-weight: 700;
    }

    .result-value {
        color: #087943;
        font-size: 30px;
        font-weight: 850;
        margin-top: 4px;
    }

    .negative {
        color: #c33c3c;
    }

    /* INPUTS */

    div[data-baseweb="input"] > div,
    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
        border-color: #cbded6 !important;
    }

    .stTextInput label,
    .stNumberInput label,
    .stSelectbox label {
        color: #164f40 !important;
        font-weight: 650 !important;
    }

    /* BUTTON */

    .stButton button {
        border-radius: 11px;
        min-height: 43px;
        font-weight: 750;
        border: 1px solid #13945b;
        background: linear-gradient(
            135deg,
            #07965a,
            #08784d
        );
        color: white;
        box-shadow: 0 5px 15px rgba(8,122,77,0.15);
    }

    .stButton button:hover {
        color: white;
        border-color: #08784d;
        background: linear-gradient(
            135deg,
            #078750,
            #066b45
        );
    }

    .footer {
        text-align: center;
        color: #769188;
        font-size: 12px;
        padding: 25px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# FUNCTIONS
# =========================================================

def clean_crop_name(value):
    if value is None:
        return "Unknown"

    text = str(value).strip()

    text = re.sub(
        r"(?i).*?predict[_ ]*crop\s*(?:is|:)?\s*",
        "",
        text
    )

    text = text.replace("_", " ").replace("-", " ").strip()
    text = re.sub(r"\s+", " ", text)

    known = {
        "ispigeonpeas": "Pigeon Peas",
        "pigeonpeas": "Pigeon Peas",
        "pigeon peas": "Pigeon Peas",
        "isrice": "Rice",
        "rice": "Rice",
        "ismaize": "Maize",
        "maize": "Maize",
        "iscotton": "Cotton",
        "cotton": "Cotton",
        "iswheat": "Wheat",
        "wheat": "Wheat",
        "isgroundnut": "Groundnut",
        "groundnut": "Groundnut",
        "ischickpea": "Chickpea",
        "chickpea": "Chickpea",
        "chickpeas": "Chickpea",
    }

    key = text.lower().replace(" ", "")

    if key in known:
        return known[key]

    return text.title()


def hindi_crop_name(crop):
    mapping = {
        "Pigeon Peas": "अरहर",
        "Rice": "धान",
        "Maize": "मक्का",
        "Cotton": "कपास",
        "Wheat": "गेहूँ",
        "Groundnut": "मूंगफली",
        "Chickpea": "चना",
        "Sugarcane": "गन्ना",
        "Soybean": "सोयाबीन",
        "Bajra": "बाजरा",
        "Barley": "जौ",
        "Mustard": "सरसों",
        "Potato": "आलू",
        "Tomato": "टमाटर",
    }

    return mapping.get(crop, crop)


def extract_number(value):
    if isinstance(value, (int, float)):
        return float(value)

    text = str(value).replace(",", "")

    numbers = re.findall(
        r"-?\d+(?:\.\d+)?",
        text
    )

    if not numbers:
        raise ValueError("Number not found")

    return float(numbers[-1])


def post_api(endpoint, payload):
    try:
        response = requests.post(
            f"{FASTAPI_URL}{endpoint}",
            json=payload,
            timeout=90,
        )

        if response.status_code != 200:
            return None, f"Backend Error: {response.status_code}"

        return response.json(), None

    except requests.exceptions.Timeout:
        return None, "Backend timeout. Render may be waking up."

    except requests.exceptions.ConnectionError:
        return None, "Could not connect to FastAPI backend."

    except Exception as e:
        return None, str(e)


def get_weather(village, district, state):

    if not OPENWEATHER_API_KEY:
        return None, "OPENWEATHER_API_KEY is not configured."

    queries = []

    q1 = ", ".join(
        x for x in [
            village.strip(),
            district.strip(),
            state.strip(),
            "India"
        ] if x
    )

    q2 = ", ".join(
        x for x in [
            district.strip(),
            state.strip(),
            "India"
        ] if x
    )

    q3 = ", ".join(
        x for x in [
            state.strip(),
            "India"
        ] if x
    )

    for q in [q1, q2, q3]:
        if q and q not in queries:
            queries.append(q)

    url = "https://api.openweathermap.org/data/2.5/weather"

    for query in queries:
        try:

            response = requests.get(
                url,
                params={
                    "q": query,
                    "appid": OPENWEATHER_API_KEY,
                    "units": "metric",
                },
                timeout=15,
            )

            if response.status_code != 200:
                continue

            data = response.json()

            rainfall = 0.0

            if isinstance(data.get("rain"), dict):
                rainfall = float(
                    data["rain"].get(
                        "1h",
                        data["rain"].get("3h", 0)
                    ) or 0
                )

            return {
                "temperature": float(
                    data["main"]["temp"]
                ),
                "humidity": float(
                    data["main"]["humidity"]
                ),
                "rainfall": rainfall,
                "village": village,
                "district": district,
                "state": state,
                "city": data.get("name", ""),
            }, None

        except Exception:
            continue

    return None, L.get(
        "weather_error",
        "Could not fetch weather."
    )


def weather_card():

    w = st.session_state.weather_data

    st.markdown(
        f"""
        <div class="weather-card">
            <div class="weather-title">
                ☀️ {L["current_weather"]}
            </div>

            <div style="display:flex; gap:10px;">
                <div class="weather-value" style="flex:1;">
                    <div class="weather-number">
                        🌡️ {w["temperature"]:.1f}°C
                    </div>
                    <div class="weather-label">
                        {L["temperature"]}
                    </div>
                </div>

                <div class="weather-value" style="flex:1;">
                    <div class="weather-number">
                        💧 {w["humidity"]:.0f}%
                    </div>
                    <div class="weather-label">
                        {L["humidity"]}
                    </div>
                </div>

                <div class="weather-value" style="flex:1;">
                    <div class="weather-number">
                        🌧️ {w["rainfall"]:.1f} mm
                    </div>
                    <div class="weather-label">
                        {L["rainfall"]}
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-icon">🌱</div>

            <div class="brand-title">
                AgriSense <span>AI</span>
            </div>

            <div class="brand-subtitle">
                Smart Agriculture Decision Support
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    navigation = [
        ("🏠", "home", "Home"),
        ("☁️", "weather", "Weather"),
        ("🌱", "crop", "Crop Suggestion"),
        ("📊", "yield", "Yield Estimate"),
        ("💰", "cost", "Cost Estimate"),
        ("📈", "profit", "Profit Estimate"),
        ("ℹ️", "about", "About"),
    ]

    for icon, key, page in navigation:

        if st.button(
            f"{icon}   {L[key]}",
            key=f"nav_{key}",
            use_container_width=True,
        ):
            st.session_state.page = page
            st.rerun()

    st.markdown(
        """
        <div class="sidebar-note">
            🌿<br>
            Better Farming<br>
            Brighter Future
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# LANGUAGE
# =========================================================

_, language_col = st.columns([7, 1])

with language_col:

    language = st.selectbox(
        "Language",
        ["English", "Hindi"],
        index=(
            0
            if st.session_state.language == "English"
            else 1
        ),
        label_visibility="collapsed",
        key="language_selector",
    )

    if language != st.session_state.language:
        st.session_state.language = language
        st.rerun()


# =========================================================
# HOME
# =========================================================

if st.session_state.page == "Home":

    st.markdown(
        f"""
        <div class="hero">

            <h1>
                {L["welcome"]}
                <span></span>
            </h1>

            <p>
                {L["tagline"]}
            </p>

            <div class="hero-pills">

                <div class="hero-pill">
                    <div class="hero-pill-icon">🌱</div>
                    {L["better"]}
                </div>

                <div class="hero-pill">
                    <div class="hero-pill-icon">📈</div>
                    {L["productivity"]}
                </div>

                <div class="hero-pill">
                    <div class="hero-pill-icon">₹</div>
                    {L["profitability"]}
                </div>

            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    cards = [
        (
            "green",
            "🌱",
            L["crop"],
            L["crop_desc"]
        ),
        (
            "blue",
            "☁️",
            L["weather"],
            L["weather_desc"]
        ),
        (
            "yellow",
            "🌾",
            L["yield"],
            L["yield_desc"]
        ),
        (
            "pink",
            "💰",
            L["cost"],
            L["cost_desc"]
        ),
        (
            "purple",
            "📈",
            L["profit"],
            L["profit_desc"]
        ),
    ]

    columns = st.columns(5)

    for col, card in zip(columns, cards):

        color, icon, title, description = card

        with col:

            st.markdown(
                f"""
                <div class="feature-card {color}">

                    <div>
                        <span style="font-size:23px;">
                            {icon}
                        </span>

                        <span class="feature-title">
                            {title}
                        </span>
                    </div>

                    <div class="feature-text">
                        {description}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        f"""
        <div class="section-card">

            <div class="section-heading">
                🌱 {L["crop"]}
            </div>

            <div class="page-description">
                {L["crop_desc"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    if st.button(
        f"🌱 {L['crop_button']}",
        key="home_crop",
    ):
        st.session_state.page = "Crop Suggestion"
        st.rerun()


# =========================================================
# WEATHER
# =========================================================

elif st.session_state.page == "Weather":

    st.markdown(
        f'<div class="page-title">☁️ {L["weather"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">{L["weather_desc"]}</div>',
        unsafe_allow_html=True
    )

    automatic, manual = st.tabs(
        [
            f"☁️ {L['automatic']}",
            f"✏️ {L['manual']}"
        ]
    )

    with automatic:

        st.markdown(
            f'<div class="mini-heading">📍 {L["location"]}</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            village = st.text_input(
                L["village"],
                key="weather_village"
            )

        with c2:
            district = st.text_input(
                L["district"],
                key="weather_district"
            )

        with c3:
            state = st.text_input(
                L["state"],
                key="weather_state"
            )

        if st.button(
            f"☁️ {L['get_weather']}",
            key="weather_get",
        ):

            if not state:
                st.warning("Please enter State.")

            else:

                with st.spinner("Getting weather..."):

                    data, error = get_weather(
                        village,
                        district,
                        state
                    )

                if error:
                    st.error(error)

                else:
                    st.session_state.weather_data = data
                    st.success("Weather updated successfully.")

        weather_card()

    with manual:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.text_input(
                L["village"],
                key="manual_village"
            )

        with c2:
            st.text_input(
                L["district"],
                key="manual_district"
            )

        with c3:
            st.text_input(
                L["state"],
                key="manual_state"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            temp = st.number_input(
                f"{L['temperature']} (°C)",
                -50.0,
                70.0,
                25.0,
                0.1,
                key="manual_temperature"
            )

        with c2:
            humidity = st.number_input(
                f"{L['humidity']} (%)",
                0.0,
                100.0,
                70.0,
                0.1,
                key="manual_humidity"
            )

        with c3:
            rainfall = st.number_input(
                f"{L['rainfall']} (mm)",
                0.0,
                1000.0,
                0.0,
                0.1,
                key="manual_rainfall"
            )

        if st.button(
            f"💾 {L['manual']}",
            key="save_manual_weather"
        ):

            st.session_state.weather_data = {
                "temperature": temp,
                "humidity": humidity,
                "rainfall": rainfall,
                "village": st.session_state.manual_village,
                "district": st.session_state.manual_district,
                "state": st.session_state.manual_state,
                "city": "",
            }

            st.success("Weather updated successfully.")

        weather_card()


# =========================================================
# CROP SUGGESTION
# =========================================================

elif st.session_state.page == "Crop Suggestion":

    st.markdown(
        f'<div class="page-title">🌱 {L["crop"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">{L["crop_desc"]}</div>',
        unsafe_allow_html=True
    )

    automatic, manual = st.tabs(
        [
            f"☁️ {L['automatic']}",
            f"✏️ {L['manual']}"
        ]
    )

    # -----------------------------------------------------
    # AUTOMATIC WEATHER
    # -----------------------------------------------------

    with automatic:

        st.markdown(
            f"""
            <div class="section-card">
                <div class="mini-heading">
                    📍 1. {L["location"]}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            village = st.text_input(
                L["village"],
                key="crop_village"
            )

        with c2:
            district = st.text_input(
                L["district"],
                key="crop_district"
            )

        with c3:
            state = st.text_input(
                L["state"],
                key="crop_state"
            )

        if st.button(
            f"☁️ {L['get_weather']}",
            key="crop_weather_button"
        ):

            if not state:

                st.warning("Please enter State.")

            else:

                with st.spinner("Getting weather..."):

                    data, error = get_weather(
                        village,
                        district,
                        state
                    )

                if error:
                    st.error(error)

                else:
                    st.session_state.weather_data = data
                    st.success("Weather updated successfully.")

        left, right = st.columns([1.7, 1])

        with left:

            st.markdown(
                f"""
                <div class="section-card">
                    <div class="mini-heading">
                        🌱 2. {L["soil"]}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            n, p, k, ph = st.columns(4)

            with n:
                nitrogen = st.number_input(
                    L["nitrogen"],
                    0.0,
                    200.0,
                    50.0,
                    1.0,
                    key="crop_n"
                )

            with p:
                phosphorus = st.number_input(
                    L["phosphorus"],
                    0.0,
                    200.0,
                    50.0,
                    1.0,
                    key="crop_p"
                )

            with k:
                potassium = st.number_input(
                    L["potassium"],
                    0.0,
                    250.0,
                    50.0,
                    1.0,
                    key="crop_k"
                )

            with ph:
                ph_value = st.number_input(
                    L["ph"],
                    0.0,
                    14.0,
                    6.5,
                    0.1,
                    key="crop_ph"
                )

            w = st.session_state.weather_data

            st.markdown(
                '<div class="mini-heading">☁️ Weather Data</div>',
                unsafe_allow_html=True
            )

            wc1, wc2, wc3 = st.columns(3)

            with wc1:
                st.number_input(
                    f"{L['temperature']} (°C)",
                    value=float(w["temperature"]),
                    disabled=True,
                    key="crop_temp_display"
                )

            with wc2:
                st.number_input(
                    f"{L['humidity']} (%)",
                    value=float(w["humidity"]),
                    disabled=True,
                    key="crop_humidity_display"
                )

            with wc3:
                st.number_input(
                    f"{L['rainfall']} (mm)",
                    value=float(w["rainfall"]),
                    disabled=True,
                    key="crop_rain_display"
                )

            if st.button(
                f"🌱 {L['crop_button']}",
                key="crop_predict_auto"
            ):

                payload = {
                    "N": float(nitrogen),
                    "P": float(phosphorus),
                    "K": float(potassium),
                    "temperature": float(w["temperature"]),
                    "humidity": float(w["humidity"]),
                    "ph": float(ph_value),
                    "rainfall": float(w["rainfall"]),
                }

                with st.spinner("Finding the best crop..."):

                    result, error = post_api(
                        "/predict1",
                        payload
                    )

                if error:

                    st.error(error)

                else:

                    raw = result.get(
                        "predict_crop",
                        result
                    )

                    crop_name = clean_crop_name(raw)

                    if st.session_state.language == "Hindi":
                        crop_name = hindi_crop_name(crop_name)

                    st.markdown(
                        f"""
                        <div class="result-box">

                            <div class="result-label">
                                {L["crop_result"]}
                            </div>

                            <div class="result-value">
                                🌾 {crop_name}
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

        with right:

            weather_card()

            st.markdown(
                f"""
                <div class="info-box">

                    <div class="info-title">
                        🌿 {L["why"]}
                    </div>

                    <div class="info-text">
                        {L["why_text"]}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

    # -----------------------------------------------------
    # MANUAL WEATHER
    # -----------------------------------------------------

    with manual:

        st.markdown(
            f'<div class="mini-heading">📍 1. {L["location"]}</div>',
            unsafe_allow_html=True
        )

        c1, c2, c3 = st.columns(3)

        with c1:
            st.text_input(
                L["village"],
                key="manual_crop_village"
            )

        with c2:
            st.text_input(
                L["district"],
                key="manual_crop_district"
            )

        with c3:
            st.text_input(
                L["state"],
                key="manual_crop_state"
            )

        c1, c2, c3 = st.columns(3)

        with c1:
            temp = st.number_input(
                f"{L['temperature']} (°C)",
                -50.0,
                70.0,
                25.0,
                0.1,
                key="manual_crop_temp"
            )

        with c2:
            humidity = st.number_input(
                f"{L['humidity']} (%)",
                0.0,
                100.0,
                70.0,
                0.1,
                key="manual_crop_humidity"
            )

        with c3:
            rainfall = st.number_input(
                f"{L['rainfall']} (mm)",
                0.0,
                1000.0,
                0.0,
                0.1,
                key="manual_crop_rainfall"
            )

        st.markdown(
            f'<div class="mini-heading">🌱 2. {L["soil"]}</div>',
            unsafe_allow_html=True
        )

        n, p, k, ph = st.columns(4)

        with n:
            nitrogen = st.number_input(
                L["nitrogen"],
                0.0,
                200.0,
                50.0,
                1.0,
                key="manual_crop_n"
            )

        with p:
            phosphorus = st.number_input(
                L["phosphorus"],
                0.0,
                200.0,
                50.0,
                1.0,
                key="manual_crop_p"
            )

        with k:
            potassium = st.number_input(
                L["potassium"],
                0.0,
                250.0,
                50.0,
                1.0,
                key="manual_crop_k"
            )

        with ph:
            ph_value = st.number_input(
                L["ph"],
                0.0,
                14.0,
                6.5,
                0.1,
                key="manual_crop_ph"
            )

        if st.button(
            f"🌱 {L['crop_button']}",
            key="crop_predict_manual"
        ):

            payload = {
                "N": float(nitrogen),
                "P": float(phosphorus),
                "K": float(potassium),
                "temperature": float(temp),
                "humidity": float(humidity),
                "ph": float(ph_value),
                "rainfall": float(rainfall),
            }

            with st.spinner("Finding the best crop..."):

                result, error = post_api(
                    "/predict1",
                    payload
                )

            if error:

                st.error(error)

            else:

                raw = result.get(
                    "predict_crop",
                    result
                )

                crop_name = clean_crop_name(raw)

                if st.session_state.language == "Hindi":
                    crop_name = hindi_crop_name(crop_name)

                st.markdown(
                    f"""
                    <div class="result-box">

                        <div class="result-label">
                            {L["crop_result"]}
                        </div>

                        <div class="result-value">
                            🌾 {crop_name}
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


# =========================================================
# YIELD ESTIMATE
# =========================================================

elif st.session_state.page == "Yield Estimate":

    st.markdown(
        f'<div class="page-title">🌾 {L["yield"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">{L["yield_desc"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        crop = st.text_input(
            "Crop",
            key="yield_crop"
        )

        state = st.text_input(
            L["state"],
            key="yield_state"
        )

    with c2:

        season = st.selectbox(
            L["season"],
            [
                "Kharif",
                "Rabi",
                "Summer",
                "Whole Year",
                "Winter"
            ],
            key="yield_season"
        )

        area = st.number_input(
            L["area"],
            min_value=0.01,
            value=1.0,
            step=0.1,
            key="yield_area"
        )

    if st.button(
        f"🌾 {L['estimate_yield']}",
        key="yield_button"
    ):

        if not crop.strip() or not state.strip():

            st.warning("Please enter Crop and State.")

        else:

            payload = {
                "Crop": crop.strip(),
                "State": state.strip(),
                "Season": season.strip(),
                "Area": float(area)
            }

            with st.spinner("Estimating production..."):

                result, error = post_api(
                    "/predict2",
                    payload
                )

            if error:

                st.error(error)

            else:

                try:

                    raw = result.get(
                        "predict_yield",
                        result
                    )

                    value = extract_number(raw)

                    st.markdown(
                        f"""
                        <div class="result-box">

                            <div class="result-label">
                                {L["yield_result"]}
                            </div>

                            <div class="result-value">
                                🌾 {value:.2f} Quintal/Hectare
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception:

                    st.success(str(result))

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# COST ESTIMATE
# =========================================================

elif st.session_state.page == "Cost Estimate":

    st.markdown(
        f'<div class="page-title">💰 {L["cost"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">{L["cost_desc"]}</div>',
        unsafe_allow_html=True
    )

    st.info(
        "Enter Cost Estimate inputs separately. "
        "Yield Estimate data is not copied automatically."
    )

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    crop = st.text_input(
        "Crop",
        key="cost_crop"
    )

    state = st.text_input(
        L["state"],
        key="cost_state"
    )

    yield_value = st.number_input(
        L["yield_input"],
        min_value=0.0,
        value=1.0,
        step=0.1,
        key="cost_yield"
    )

    if st.button(
        f"💰 {L['estimate_cost']}",
        key="cost_button"
    ):

        if not crop.strip() or not state.strip():

            st.warning("Please enter Crop and State.")

        else:

            payload = {
                "Crop": crop.strip(),
                "State": state.strip(),
                "Yield": float(yield_value)
            }

            with st.spinner("Estimating cultivation cost..."):

                result, error = post_api(
                    "/predict3",
                    payload
                )

            if error:

                st.error(error)

            else:

                try:

                    raw = result.get(
                        "predict_cost",
                        result
                    )

                    value = extract_number(raw)

                    st.markdown(
                        f"""
                        <div class="result-box">

                            <div class="result-label">
                                {L["cost_result"]}
                            </div>

                            <div class="result-value">
                                ₹ {value:,.2f} / Hectare
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                except Exception:

                    st.success(str(result))

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# PROFIT ESTIMATE
# =========================================================

elif st.session_state.page == "Profit Estimate":

    st.markdown(
        f'<div class="page-title">📈 {L["profit"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="page-description">{L["profit_desc"]}</div>',
        unsafe_allow_html=True
    )

    st.info(
        "This module is independent. Enter all values manually."
    )

    st.markdown(
        '<div class="section-card">',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2)

    with c1:

        crop = st.text_input(
            "Crop",
            key="profit_crop"
        )

        state = st.text_input(
            L["state"],
            key="profit_state"
        )

        yield_value = st.number_input(
            L["yield_input"],
            min_value=0.0,
            value=1.0,
            step=0.1,
            key="profit_yield"
        )

    with c2:

        cultivation_cost = st.number_input(
            L["cultivation_cost"],
            min_value=0.0,
            value=12000.0,
            step=100.0,
            key="profit_cost"
        )

        selling_price = st.number_input(
            L["selling_price"],
            min_value=0.0,
            value=2500.0,
            step=50.0,
            key="profit_selling_price"
        )

    if st.button(
        f"📈 {L['calculate_profit']}",
        key="profit_button"
    ):

        if not crop.strip() or not state.strip():

            st.warning("Please enter Crop and State.")

        else:

            # Revenue for 1 hectare
            total_revenue = (
                float(yield_value)
                * float(selling_price)
            )

            # Profit for 1 hectare
            profit = (
                total_revenue
                - float(cultivation_cost)
            )

            result_class = (
                "result-value"
                if profit >= 0
                else "result-value negative"
            )

            st.markdown(
                f"""
                <div class="result-box">

                    <div class="result-label">
                        {L["revenue"]}
                    </div>

                    <div class="result-value">
                        ₹ {total_revenue:,.2f}
                    </div>

                    <br>

                    <div class="result-label">
                        {L["profit_result"]}
                    </div>

                    <div class="{result_class}">
                        ₹ {profit:,.2f}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if profit >= 0:
                st.success(
                    "Estimated profit is positive."
                )
            else:
                st.warning(
                    "Estimated profit is negative."
                )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# =========================================================
# ABOUT
# =========================================================

elif st.session_state.page == "About":

    st.markdown(
        f'<div class="page-title">🌱 {L["about_title"]}</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="section-card">

            <div class="section-heading">
                AgriSense AI
            </div>

            <div class="page-description">
                Smart Agriculture Decision Support
            </div>

            <div class="feature-text">
                {L["about_text"]}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.markdown(
            """
            <div class="feature-card green">

                <div class="feature-title">
                    🌱 Crop Suggestion
                </div>

                <div class="feature-text">
                    ML-based crop recommendation using
                    soil and weather inputs.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="feature-card blue">

                <div class="feature-title">
                    ☁️ Weather
                </div>

                <div class="feature-text">
                    Automatic OpenWeather data or
                    manual weather entry.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:

        st.markdown(
            """
            <div class="feature-card purple">

                <div class="feature-title">
                    📈 Financial Estimates
                </div>

                <div class="feature-text">
                    Yield, cultivation cost and profit
                    estimates for farming decisions.
                </div>

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
        AgriSense AI • Smart Agriculture Decision Support
    </div>
    """,
    unsafe_allow_html=True
)