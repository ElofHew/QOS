# QOS Advanced Options

import os
import json
import time
import random
import platform
import requests
from colorama import init as cinit
from colorama import Fore, Style, Back
import pathlib

cinit(autoreset=True)

with open("data/config/config.json", "r") as config_file:
    config_file = json.load(config_file)
    os_type = config_file["os_type"]

def get_ads():
    try:
        with open("data/config/config.json", "r") as config_file:
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
        response = requests.get("https://os.drevan.xyz/qosres/common/ad.data", timeout=5)
        if response.status_code == 200:  # 检查请求是否成功
            ad_list = response.json()  # 假设ad.data是JSON格式的数据
            print(f"{Fore.LIGHTGREEN_EX}AD: {Fore.CYAN}{random.choice(ad_list)}{Style.RESET_ALL}")
            print()
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

def change_startup_title():
    with open("data/config/config.json", "r") as config_file_old:
        config_file_old = json.load(config_file_old)
    print("Enter a new title for the startup UI: ")
    new_title = input("> ")
    config_file_old["startup_title"] = new_title
    with open("data/config/config.json", "w") as config_file_new:
        json.dump(config_file_old, config_file_new, indent=4)
    print(f"{Fore.GREEN}Title changed successfully.{Style.RESET_ALL}")
    print()

def change_qos_logo_text():
    with open("data/config/config.json", "r") as config_file_old:
        config_file_old = json.load(config_file_old)
    print("Choose a new type for the QOS logo: ")
    print("1.")
    cat("system/etc/logo/1.txt")
    print("2.")
    cat("system/etc/logo/2.txt")
    print("3.")
    cat("system/etc/logo/3.txt")
    print("4.")
    cat("system/etc/logo/4.txt")
    while True:
        new_type = input("> ")
        if new_type in ["1", "2", "3", "4"]:
            config_file_old["qos_startup_logo"] = f"{new_type}"
            break
        elif new_type == "":
            print(f"{Fore.YELLOW}No changes made.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Invalid input.{Style.RESET_ALL}")
            continue
    with open("data/config/config.json", "w") as config_file_new:
        json.dump(config_file_old, config_file_new, indent=4)
    print(f"{Fore.GREEN}Logo type changed successfully.{Style.RESET_ALL}")
    print()

def manage_ads():
    with open("data/config/config.json", "r") as config_file_old:
        config_file_old = json.load(config_file_old)
        activate_statue = config_file_old["activate_statue"]
        ad_statue = config_file_old["ad_statue"]
    if activate_statue == False:
        print(f"{Fore.YELLOW}You have not activated QOS Advanced Options yet! Please activate Quarter to disable ads.{Style.RESET_ALL}")
        return 0
    while True:
        try:
            print(f"{Fore.GREEN}# Manage ADs #{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Enable ADs{Style.RESET_ALL}")
            print(f"{Fore.CYAN}2. Disable ADs{Style.RESET_ALL}")
            choice = input(f"{Fore.YELLOW}Choose an option (1/2): {Style.RESET_ALL}")
            if choice == "1":
                config_file_old["ad_statue"] = True
                print(f"{Fore.LIGHTGREEN_EX}ADs enabled successfully.{Style.RESET_ALL}")
                input("(Press Enter to continue...)")
            elif choice == "2":
                config_file_old["ad_statue"] = False
                print(f"{Fore.LIGHTGREEN_EX}ADs disabled successfully.{Style.RESET_ALL}")
                input("(Press Enter to continue...)")
            else:
                print(f"{Fore.RED}Error: Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
                continue
            with open("data/config/config.json", "w") as config_file_new:
                json.dump(config_file_old, config_file_new, indent=4)
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
            return 0
        except json.JSONDecodeError as e:
            print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
            return 0
        except IOError as e:
            print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
            return 0
        except Exception as e:
            print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
            return 0
        break
    return 1
    