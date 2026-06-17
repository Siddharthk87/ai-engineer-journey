import requests

def get_weather(city):
    base_url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise an error for bad responses
        data = response.json()

        if not data.get("results"):
            print(f"No results found for city: {city}")
            return None
        
        # Extract latitude and longitude from the first result
        location = data["results"][0]
        latitude = location["latitude"]
        longitude = location["longitude"]   
        name = location["name"]
        country = location["country"]

        print(f"City: {name}, Country: {country}, Latitude: {latitude}, Longitude: {longitude}")

        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "auto"
        }
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        current = weather_data["current"]
        temperature = current["temperature_2m"]
        wind_speed = current["wind_speed_10m"]

        return {
            "city": name,
            "country": country,
            "temperature": temperature,
            "wind_speed": wind_speed
        }
    
    except requests.exceptions.ConnectionError:
        print("Network error: Unable to connect to the weather service.")
        return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    
def display_weather_info(weather_info):
    if not weather_info:
        print("No weather information available.")
        return
    print(f"Weather in {weather_info['city']}, {weather_info['country']}:")
    print(f"Temperature: {weather_info['temperature']}°C")
    print(f"Wind Speed: {weather_info['wind_speed']} km/h")

city_name = input("Enter a city name to get the current weather: ")
weather_info = get_weather(city_name)
display_weather_info(weather_info)
print("Weather information retrieval complete.")    