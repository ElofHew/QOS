import os
import sys
import platform
import json
import time
import random
import requests
import pathlib
from colorama import Fore, Style, init

init(autoreset=True)

def get_ads():
    try:
        with open(os.path.join("data", "config", "config.json"), "r") as config_file:
            config_file = json.load(config_file)
            activate_statue = config_file["activate_statue"]
            ad_statue = config_file["ad_statue"]
        if activate_statue == False and ad_statue == True:
            time.sleep(1)
            pass
        if activate_statue == False and ad_statue == False:
            time.sleep(1)
            pass
        if activate_statue == True and ad_statue == True:
            print(f"{Fore.YELLOW}(Tips: You can disable ads in the settings.){Style.RESET_ALL}")
        if activate_statue == True and ad_statue == False:
            return 1
        # Check local template file
        local_ad_path = os.path.join("data", "ads", "ad.data")
        if not os.path.exists(os.path.join("data", "ads")):
            os.makedirs(os.path.join("data", "ads"))
        if not os.path.exists(local_ad_path):
            response = requests.get("https://os.drevan.xyz/qosres/common/adnew.data", timeout=5)
            if response.status_code == 200:  # 检查请求是否成功
                with open(local_ad_path, "wb") as ad_file:
                    ad_file.write(response.content)
            else:
                print(f"{Fore.RED}Error: Failed to retrieve ads. (Status code: {response.status_code}){Style.RESET_ALL}")
                return 0
        # Read ads from local file
        with open(local_ad_path, "r") as ad_file:
            ad_list = ad_file.readlines()
        print(f"{Fore.LIGHTGREEN_EX}AD: {Fore.CYAN}{random.choice(ad_list)}{Style.RESET_ALL}")
        return 1
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}Error: Failed to retrieve ads. (Timeout){Style.RESET_ALL}")
        return 0
    except requests.RequestException as e:
        print(f"{Fore.RED}Error: Failed to retrieve ads. Error message: {e}{Style.RESET_ALL}")
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode ad data. Error message: {e}{Style.RESET_ALL}")
        return 0
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred while retrieving ads. Error message: {e}{Style.RESET_ALL}")
        return 0    

def clear():
    os_type = platform.system()
    if os_type == "Windows":
        os.system("cls")
    elif os_type == "Linux":
        os.system("clear")
    else:
        print(f"{Fore.RED}Error: Unsupported OS type.{Style.RESET_ALL}")

def d_exit():
    sys.exit(0)

def d_restart():
    sys.exit(1)

def cat(file_path):
    txt_path = pathlib.Path(file_path)
    if txt_path.exists():
        try:
            with open(file_path, "r") as f:
                print(f.read())
            f.close()
        except IOError as e:
            print(f"{Fore.RED}Error: Have some problems when reading file {file_path}. Error message: {e}{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}Error: Have some problems when reading file {file_path}. Error message: {e}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: File {file_path} does not exist.{Style.RESET_ALL}")

def jump_print(text, color=None, background=None, style=None):
    # 引用方法：必须字体色在前，背景色在后，样式最后，文本保持最前
    try:
        style_str = ""
        if color:
            style_str += color
        if background:
            style_str += background
        if style:
            style_str += style
        for char in text:
            print(style_str + char + Style.RESET_ALL, end="", flush=True)
            time.sleep(0.1)
        print()
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred while jump printing. Error message: {e}{Style.RESET_ALL}")
        return 1