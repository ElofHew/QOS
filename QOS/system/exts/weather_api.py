# QOS Weather API
import requests
import json

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
