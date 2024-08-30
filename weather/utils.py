import requests
from django.conf import settings

def fetch_weather_data(city):
    url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_KEY}&q={city}'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {
            'city': city,
            'temperature': data['current']['temp_c'],
            'humidity': data['current']['humidity'],
            'condition': data['current']['condition']['text'],
            'wind_speed': data['current']['wind_kph'],  # Wind speed in kph
            'pressure': data['current']['pressure_mb'],  # Pressure in mb
            'visibility': data['current']['vis_km'],  # Visibility in km
            'uv_index': data['current']['uv'],  # UV index
            'feels_like': data['current']['feelslike_c']  # Feels like temperature in Celsius
        }
    return None

