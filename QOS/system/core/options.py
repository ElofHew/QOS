# QOS Advanced Options

import os
import json
import sys
import time
from colorama import init as cinit
from colorama import Fore, Style, Back
import pathlib

cinit(autoreset=True)

with open("data/config/config.json", "r") as config_file:
    config_file = json.load(config_file)
    os_type = config_file["os_type"]

def cat(file_path):
    txt_path = pathlib.Path(str(file_path))
    if txt_path.exists():
        try:
            with open(file_path, "r") as f:
                print(f.read())
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
    cat("etc/logo/1.txt")
    print("2.")
    cat("etc/logo/2.txt")
    print("3.")
    cat("etc/logo/3.txt")
    print("4.")
    cat("etc/logo/4.txt")
    while True:
        new_type = input("> ")
        if new_type in ["1", "2", "3", "4"]:
            config_file_old["qos_logo_path"] = f"etc/logo/{new_type}.txt"
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
