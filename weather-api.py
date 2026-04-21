import requests
from datetime import timezone, timedelta
import redis
import time
import json

API_KEY = ''

cache = redis.Redis()

def kelvin_to_(kelvin):
        celsius = kelvin - 273.15
        fahrenheit = (kelvin - 273.15) * 9/5 + 32
        return fahrenheit, celsius

def get_weather(CITY, COUNTRY_CODE, TYPE_OF_TEMP):
    try:
        #Check cache
        cached = cache.get(f"weather:{CITY}")
        if cached:
            #Print for debugging
            print(f"From cache!")
            #Convert string back to dictionary
            data = json.loads(cached.decode())
        else:

            url = f'https://api.openweathermap.org/data/2.5/weather?q={CITY},{COUNTRY_CODE}&APPID={API_KEY}'
            response = requests.get(url)

            if response.status_code == 404:
                raise Exception(f"City: {CITY} or Country Code: {COUNTRY_CODE} does not exist")
        
            if response.status_code != 200:
                raise Exception(f"API error: {response.status_code}")
        
            data = response.json()

            #Store data as JSON string in the cache
            cache.setex(f"weather:{CITY}", 3600, json.dumps(data))
            #Print for debugging
            print("From API!")
    
        kelvin = data['main']['temp']
        tz = data['timezone']

        fahrenheit, celsius = kelvin_to_(kelvin)
        feels_like_f, feels_like_c = kelvin_to_(data['main']['feels_like'])
        temp_min_f, temp_min_c = kelvin_to_(data['main']['temp_min'])
        temp_max_f, temp_max_c = kelvin_to_(data['main']['temp_max'])

        timezoneUtc = timezone(timedelta(seconds=tz))
        
        if TYPE_OF_TEMP == "C":
            print(f"""Temperature in {CITY}, {COUNTRY_CODE}:\n
        Celsius: {celsius:.2f}°C\n
        Feels Like: {feels_like_c:.2f}°C\n
        Minimum Temperature: {temp_min_c:.2f}°C\n
        Maximum Temperature: {temp_max_c:.2f}°C\n
        Timezone: {timezoneUtc}""")
        elif TYPE_OF_TEMP == "F":
            print(f"""Temperature in {CITY}, {COUNTRY_CODE}:\n
        Fahrenheit: {fahrenheit:.2f}°F\n
        Feels Like: {feels_like_f:.2f}°F\n
        Minimum Temperature: {temp_min_f:.2f}°F\n
        Maximum Temperature: {temp_max_f:.2f}°F\n
        Timezone: {timezoneUtc}""")
            
        else:
            raise Exception("Please choose between Celsius or Fahrenheit")
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"Network error: {e}")

try:
    CITY = input("Enter the name of a city: ").upper()
    COUNTRY_CODE = input("Enter the country code: ").upper()
    TYPE_OF_TEMP = input("C or F: ").upper()
    get_weather(CITY,COUNTRY_CODE,TYPE_OF_TEMP)
except Exception as e:
    print(f"Error: {e}")
    
