import streamlit as st
import requests
from datetime import datetime
import random

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="🌦️ WORLD Weather App",
    page_icon="🌈",
    layout="centered"
)

# ---------- RANDOM COLOR THEMES ----------
def random_gradient():
    gradients = [
        ("#89f7fe", "#66a6ff"),  # blue sky
        ("#ff9a9e", "#fad0c4"),  # pink-peach
        ("#a1c4fd", "#c2e9fb"),  # soft blue
        ("#fbc2eb", "#a6c1ee"),  # purple-pink
        ("#fddb92", "#d1fdff"),  # sunny yellow
        ("#84fab0", "#8fd3f4"),  # aqua-green
        ("#fccb90", "#d57eeb"),  # sunset
        ("#f6d365", "#fda085"),  # orange-peach
    ]
    return random.choice(gradients)

color1, color2 = random_gradient()

# ---------- GLOBAL STYLE ----------
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

    body {{
        background: linear-gradient(135deg, {color1}, {color2});
        background-attachment: fixed;
        color: #212529;
        font-family: 'Poppins', sans-serif;
        transition: background 1s ease-in-out;
    }}
    .title {{
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        color: #003049;
        text-shadow: 2px 2px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        animation: fadeInDown 1s ease;
    }}
    .subtitle {{
        text-align: center;
        font-size: 1rem;
        color: #333;
        margin-bottom: 20px;
    }}
    .weather-card {{
        background: rgba(255, 255, 255, 0.85);
        border-radius: 25px;
        padding: 35px;
        margin-top: 20px;
        box-shadow: 0 5px 25px rgba(0,0,0,0.1);
        text-align: center;
        backdrop-filter: blur(10px);
        animation: fadeIn 1.2s ease-in-out;
        transition: all 0.4s ease-in-out;
    }}
    .weather-card:hover {{
        transform: scale(1.03);
        box-shadow: 0 10px 35px rgba(0,0,0,0.2);
    }}
    .city {{
        font-size: 1.6rem;
        font-weight: 600;
        color: #004e89;
    }}
    .temp {{
        font-size: 2rem;
        font-weight: 700;
        margin: 10px 0;
        color: #222;
    }}
    .desc {{
        font-size: 1.2rem;
        color: #555;
    }}
    .details {{
        font-size: 1rem;
        color: #444;
        margin-top: 10px;
    }}
    .footer {{
        text-align: center;
        margin-top: 40px;
        color: #333;
        font-size: 14px;
        opacity: 0.7;
    }}
    @keyframes fadeIn {{
        from {{opacity: 0; transform: translateY(10px);}}
        to {{opacity: 1; transform: translateY(0);}}
    }}
    @keyframes fadeInDown {{
        from {{opacity: 0; transform: translateY(-15px);}}
        to {{opacity: 1; transform: translateY(0);}}
    }}
    </style>
""", unsafe_allow_html=True)

# ---------- APP HEADER ----------
st.markdown("<h1 class='title'>🌈 WORLD Weather Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Enter a city name and see real-time weather updates with auto-changing themes 🌦️</p>", unsafe_allow_html=True)

# ---------- INPUT ----------
city_name = st.text_input("🏙️ Enter City Name", placeholder="e.g. Karachi, Lahore, London")

# ---------- WEATHER LOGIC ----------
if city_name:
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city_name}"
    geo_response = requests.get(geo_url).json()

    if "results" in geo_response and len(geo_response["results"]) > 0:
        city_data = geo_response["results"][0]
        lat = city_data["latitude"]
        lon = city_data["longitude"]
        city = city_data["name"]
        country = city_data["country"]

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        weather_response = requests.get(weather_url)

        if weather_response.status_code == 200:
            weather = weather_response.json()["current_weather"]
            temp = weather["temperature"]
            wind = weather["windspeed"]
            code = weather["weathercode"]

            weather_map = {
                0: "Clear sky ☀️", 1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅",
                3: "Overcast ☁️", 45: "Fog 🌫️", 48: "Rime fog 🌫️",
                51: "Light drizzle 🌦️", 61: "Rain 🌧️", 71: "Snow ❄️",
                80: "Rain showers 🌧️", 95: "Thunderstorm ⛈️"
            }
            desc = weather_map.get(code, "Unknown weather 🌈")

            st.markdown(f"""
            <div class='weather-card'>
                <div class='city'>{city}, {country}</div>
                <div class='temp'>{temp}°C</div>
                <div class='desc'>{desc}</div>
                <div class='details'>
                    🌬️ Wind Speed: {wind} km/h<br>
                    🕒 Updated: {datetime.now().strftime('%I:%M %p')}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.error("❌ Unable to fetch weather data.")
    else:
        st.error("⚠️ City not found. Please check spelling.")
else:
    st.info("👉 Please enter a city name to get live weather details.")

# ---------- FOOTER ----------
st.markdown("<p class='footer'>🌍 Powered by Open-Meteo API | Designed by <b>AZHAR ABBASI</b> ✨</p>", unsafe_allow_html=True)
