import requests
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, World!"}

@app.get("/weather/{city}")
def get_weather(city: str):
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": city, "count": 1, "language": "en", "format": "json"}

    response = requests.get(base_url, params=params)
    data = response.json()

    if not data.get("results"):
        return {"error": f"City '{city}' not found"}
    
    location = data["results"][0]
    latitude = location["latitude"]
    longitude = location["longitude"]

    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(weather_url, params=weather_params)
    weather_data = weather_response.json()
    current = weather_data["current"]

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current["temperature_2m"],
        "wind_speed": current["wind_speed_10m"]
    }