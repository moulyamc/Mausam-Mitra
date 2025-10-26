import requests
from dataclasses import dataclass

API_Key = 'e28b4ac1714ca57754ecf7195fec4898'

@dataclass
class WeatherInfo:
    main: str
    description: str
    icon: str
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    humidity: int
    pressure: int
    visibility: int
    speed: float
    deg: int
    timezone: int
    

def get_lan_long(city_name, state_code, country_code, API_Key):
    resp = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city_name},{state_code},{country_code}&appid={API_Key}').json()
    data = resp[0]
    lat, lon = data.get('lat'), data.get('lon')
    return lat, lon

def get_current_weather(lat,lon,API_Key):
    resp = requests.get(f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_Key}&units=metric').json()
    data = WeatherInfo(
        main = resp.get('weather')[0].get('main'),
        description = resp.get('weather')[0].get('description'),
        icon = resp.get('weather')[0].get('icon'),
        temp = resp.get('main').get('temp'),
        feels_like = resp.get('main').get('feels_like'),
        temp_min = resp.get('main').get('temp_min'),
        temp_max = resp.get('main').get('temp_max'),
        humidity = resp.get('main').get('humidity'),
        pressure = resp.get('main').get('pressure'),
        visibility = resp.get('visibility'),
        speed = resp.get('wind').get('speed'),
        deg = resp.get('wind').get('deg'),
        timezone = resp.get('timezone')
        
    )
    
    return data

def main(city_name, state_code, country_code):
    lat, lon = get_lan_long(city_name, state_code, country_code, API_Key)
    weather_data = get_current_weather(lat,lon,API_Key)
    return weather_data




if __name__ == "__main__":
    lat, lon = get_lan_long('Bengaluru', 'Karnataka', 'India', API_Key)
    print(get_current_weather(lat,lon,API_Key))


