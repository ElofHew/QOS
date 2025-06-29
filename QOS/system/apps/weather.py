# QOS Weather Application

import os
import requests
import datetime
import json
import platform
from colorama import Fore, Style, init

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

weather_config_path = os.path.join(os.getcwd(), "data", "data", "weather")
weather_config_file = os.path.join(weather_config_path, "weather.json")

def get_weather_settings():
    global c_city, c_unit, c_language
    try:
        if not os.path.exists(weather_config_path):
            os.makedirs(weather_config_path)
        if os.path.exists(weather_config_file):
            with open(weather_config_file, "r") as f:
                config = json.load(f)
                c_city = config["city"]
                c_unit = config["unit"]
                c_language = config["lang"]
            # Print Current Weather Settings
            print(f"{Fore.GREEN}Current Weather Settings{Style.RESET_ALL}")
            print(f"{Fore.CYAN}City: {Fore.LIGHTGREEN_EX}{c_city}{Fore.RESET}")
            print(f"{Fore.CYAN}Unit: {Fore.LIGHTGREEN_EX}{c_unit}{Fore.RESET}")
            print(f"{Fore.CYAN}Language: {Fore.LIGHTGREEN_EX}{c_language}{Fore.RESET}")
            input("(Press Enter to edit...)")
        city = input(f"{Fore.GREEN}Please enter your preferred city: {Fore.RESET}")
        city = city.replace(" ", "").lower()
        while True:
            unit = input(f"{Fore.GREEN}Please enter your preferred unit (c/f): {Fore.RESET}")
            if unit.lower() == "c" or unit.lower() == "f":
                unit = unit.lower()
                break
            else:
                print(f"{Fore.RED}Invalid unit. Please try again.{Fore.RESET}")
                continue
        while True:
            language = input(f"{Fore.GREEN}Please enter your preferred language (zh/en): {Fore.RESET}")
            if language.lower() == "zh" or language.lower() == "en":
                language = language.lower()
                break
            else:
                print(f"{Fore.RED}Invalid language. Please try again.{Fore.RESET}")
                continue
        weather_config = {
            "city": city,
            "unit": unit,
            "lang": language
        }
        with open(weather_config_file, "w") as f:
            json.dump(weather_config, f)
        c_city = city
        c_unit = unit
        c_language = language
        print(f"{Fore.GREEN}Weather Settings Updated{Style.RESET_ALL}")
        print(f"{Fore.CYAN}City: {Fore.LIGHTGREEN_EX}{c_city}{Fore.RESET}")
        print(f"{Fore.CYAN}Unit: {Fore.LIGHTGREEN_EX}{c_unit}{Fore.RESET}")
        print(f"{Fore.CYAN}Language: {Fore.LIGHTGREEN_EX}{c_language}{Fore.RESET}")
        return 0
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}{Fore.RESET}")
        return 1

def get_weather(city, unit, language):
    # Set API URL and parameters
    if language == "zh":
        language = "zh-Hans"
    else:
        language = "en-US"
    api_key = "?key=" + "SuxDBDRWbZgAZMUmM"
    api_unit = "&unit=" + unit
    api_language = "&language=" + language
    api_location = "&location=" + city
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
            print(f'{Fore.BLUE}Weather Report for {Fore.LIGHTBLUE_EX}{location_name}{Fore.RESET}')
            print(f'{Fore.GREEN}City: {Fore.CYAN}{location_name}{Fore.RESET}')
            print(f'{Fore.GREEN}Timezone: {Fore.CYAN}{time_zone}{Fore.RESET}')
            print(f'{Fore.GREEN}Weather: {Fore.CYAN}{weather_text}{Fore.RESET}')
            print(f'{Fore.GREEN}Temperature: {Fore.CYAN}{temperature}{Fore.RESET}')
            print(f'{Fore.GREEN}Last Update: {Fore.CYAN}{last_update}{Fore.RESET}')
            print(Fore.LIGHTMAGENTA_EX + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + Fore.RESET)
            input(f"{Fore.LIGHTGREEN_EX}(Press Enter to continue...){Fore.RESET}")
        elif weather_get.status_code == 403:
            print(Fore.RED + "API Key access failed." + Fore.RESET)
        elif weather_get.status_code == 404:
            print(Fore.RED + "API Key not found." + Fore.RESET)
        elif weather_get.status_code == 500:
            print(Fore.RED + "Server internal error." + Fore.RESET)
        else:
            print(Fore.YELLOW + "Unable to retrieve weather data. Please check API URL and parameters." + Fore.RESET)
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}HTTP request error: {e}{Fore.RESET}")
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}JSON decode error: {e}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}{Fore.RESET}")

def app_once():
    city = input(f"{Fore.GREEN}Please enter your preferred city: {Fore.RESET}")
    city = city.replace(" ", "").lower()
    while True:
        unit = input(f"{Fore.GREEN}Please enter your preferred unit (c/f): {Fore.RESET}")
        if unit.lower() == "c" or unit.lower() == "f":
            unit = unit.lower()
            break
        else:
            print(f"{Fore.RED}Invalid unit. Please try again.{Fore.RESET}")
            continue
    while True:
        language = input(f"{Fore.GREEN}Please enter your preferred language (zh/en): {Fore.RESET}")
        if language.lower() == "zh" or language.lower() == "en":
            language = language.lower()
            break
        else:
            print(f"{Fore.RED}Invalid language. Please try again.{Fore.RESET}")
            continue
    get_weather(city, unit, language)

def app():
    try:
        with open (weather_config_file, "r") as f:
            config = json.load(f)
            unit = config["unit"]
            language = config["lang"]
            location = config["city"]
        get_weather(location, unit, language)
    except FileNotFoundError:
        print(f"{Fore.YELLOW}WARNING: Weather settings file not found. Please set up first.{Fore.RESET}")
        get_weather_settings()
    except Exception as e:
        print(f"{Fore.RED}Error occurred: {e}{Fore.RESET}")

def main():
    while True:
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")
        print(Fore.GREEN + "Quarter OS Weather App" + Style.RESET_ALL)
        print(Fore.CYAN + "1. Get Weather" + Fore.RESET)
        print(Fore.CYAN + "2. Get Weather in Once" + Fore.RESET)
        print(Fore.CYAN + "3. Settings" + Fore.RESET)
        print(Fore.CYAN + "4. Exit" + Fore.RESET)
        try:
            choice = int(input("> "))
            if choice == 1:
                app()
            elif choice == 2:
                app_once()
            elif choice == 3:
                get_weather_settings()
            elif choice == 4:
                break
            else:
                print(f"{Fore.RED}Invalid choice. Please try again.{Fore.RESET}")
                continue
        except ValueError:
            print(f"{Fore.RED}Invalid choice. Please try again.{Fore.RESET}")
            continue
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()