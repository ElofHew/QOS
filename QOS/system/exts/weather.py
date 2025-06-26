# QOS Weather Application

import requests
import datetime
import json
from colorama import Fore, Style, Back, init

init(autoreset=True)

# Example:
# https://api.seniverse.com/v3/weather/now.json?key=SuxDBDRWbZgAZMUmM&unit=c&start=0&scope=city&language=zh-Hans&location=beijing
"""
// Example Response:
{
  "results": [
    {
      "location": {
        "id": "WX4FBXXFKE4F",
        "name": "北京",
        "country": "CN",
        "path": "北京,北京,中国",
        "timezone": "Asia/Shanghai",
        "timezone_offset": "+08:00"
      },
      "now": {
        "text": "阴",
        "code": "9",
        "temperature": "30"
      },
      "last_update": "2025-06-26T13:32:29+08:00"
    }
  ]
}
"""

api_base_url = "https://api.seniverse.com/v3/weather/now.json"

def api(unit, language, location):
    api_key = "?key=" + "SuxDBDRWbZgAZMUmM"
    api_unit = "&unit=" + str(unit)
    api_language = "&language=" + str(language)
    api_location = "&location=" + str(location)
    http_url = api_base_url + api_key + api_unit + api_language + api_location
    try:
        # Send HTTP request and get JSON data
        weather_get = requests.get(http_url).json()
        # Check if API Key is valid
        if weather_get.get("results"):
            # Extract Weather Data
            weather_dict = weather_get['results'][0]
            # Parse Weather Data
            location_name = weather_dict['location']['name']
            time_zone = weather_dict['location']['timezone']
            weather_text = weather_dict['now']['text']
            temperature = weather_dict['now']['temperature']
            last_update = weather_dict['last_update']
            # Return Weather Data
            return location_name, time_zone, weather_text, temperature, last_update
        else:
            return None
    except requests.exceptions.RequestException as e:
        return None
    except json.JSONDecodeError as e:
        return None
    except Exception as e:
        return None

def get_weather(unit, language, location):
    global c_city, c_unit, c_language
    while True:
        try:
            print("Where do you want to get the weather?")
            c_city = input("City: ")
            s_city = c_city.replace(" ", "") and c_city.lower()
            print("What is your preferred unit? (c/f)")
            c_unit = input("Unit: ")
            print("What is your preferred language? (zh/en)")
            c_language = input("Language: ")
        except KeyboardInterrupt:
            break

def app():
    with open ("../../data/data/weather/weather.json", "r") as f:
        config = json.load(f)
        unit = config["unit"]
        language = config["lang"]
        location = config["city"]
    api_key = "?key=" + "SuxDBDRWbZgAZMUmM"
    api_unit = "&unit=" + unit
    api_language = "&language=" + language
    api_location = "&location=" + location
    http_url = api_base_url + api_key + api_unit + api_language + api_location
    try:
        # Send HTTP request and get JSON data
        weather_get = requests.get(http_url).json()
        # Check if API Key is valid
        if weather_get.get("results"):
            # Extract Weather Data
            weather_dict = weather_get['results'][0]
            # Parse Weather Data
            location_name = weather_dict['location']['name']
            time_zone = weather_dict['location']['timezone']
            weather_text = weather_dict['now']['text']
            temperature = weather_dict['now']['temperature']
            last_update = weather_dict['last_update']
            # Print Weather Data
            print(f'City: {location_name}')
            print(f'Timezone: {time_zone}')
            print(f'Weather: {weather_text}')
            print(f'Temperature: {temperature}')
            print(f'Last Update: {last_update}')
        elif weather_get.status_code == 403:
            print("API Key access failed.")
        elif weather_get.status_code == 404:
            print("API Key not found.")
        elif weather_get.status_code == 500:
            print("Server internal error.")
        else:
            print("Unable to retrieve weather data. Please check API URL and parameters.")
    except requests.exceptions.RequestException as e:
        print(f"HTTP request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
    except Exception as e:
        print(f"Error occurred: {e}")

def main():
    print(Style.DIM + Fore.GREEN + "Quarter OS Weather" + Style.RESET_ALL)