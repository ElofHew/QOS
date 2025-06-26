# QOS Kom Shell Settings

import json
from colorama import init as cinit
from colorama import Fore, Style, Back

import system.core.options as options
import system.core.login as login
import system.core.shell as shell

cinit(autoreset=True)

def account_settings():
    print(Style.BRIGHT + Fore.GREEN + "# Account Settings #")
    print(Style.BRIGHT + Fore.CYAN + "1 - Add User")
    print(Style.BRIGHT + Fore.CYAN + "2 - Remove User")
    print(Style.BRIGHT + Fore.CYAN + "3 - Change Password")
    print(Style.BRIGHT + Fore.CYAN + "4 - Back" + Style.RESET_ALL)
    while True:
        settings2_choice = input("> ")
        if settings2_choice == "1":
            login.add_user()
            continue
        elif settings2_choice == "2":
            login.remove_user()
            continue
        elif settings2_choice == "3":
            login.change_password()
            continue
        elif settings2_choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

def shell_settings():
    print(Style.BRIGHT + Fore.GREEN + "# Shell Settings #")
    print(Style.BRIGHT + Fore.CYAN + "1 - Change Shell Theme")
    print(Style.BRIGHT + Fore.CYAN + "2 - Unknown Command Progression")
    print(Style.BRIGHT + Fore.CYAN + "3 - Back" + Style.RESET_ALL)
    while True:
        settings2_choice = input("> ")
        if settings2_choice == "1":
            # shell.change_theme()
            print("Coming soon.")
            continue
        elif settings2_choice == "2":
            shell.unknown_command_progression()
            continue
        elif settings2_choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

def general_settings():
    print(Style.BRIGHT + Fore.GREEN + "# General Settings #")
    print(Style.BRIGHT + Fore.CYAN + "1 - Change Startup Title")
    print(Style.BRIGHT + Fore.CYAN + "2 - Change QOS Logo Text")
    print(Style.BRIGHT + Fore.CYAN + "3 - Back" + Style.RESET_ALL)
    while True:
        settings2_choice = input("> ")
        if settings2_choice == "1":
            options.change_startup_title()
            continue
        elif settings2_choice == "2":
            options.change_qos_logo_text()
            continue
        elif settings2_choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            continue

def main():
    while True:
        with open("data/config/config.json", "r") as qos_config_file:
            config = json.load(qos_config_file)
        print(Style.BRIGHT + Fore.BLUE + "$ QOS Settings $")
        print(Style.BRIGHT + Fore.CYAN + "1 - Account Settings")
        print(Style.BRIGHT + Fore.CYAN + "2 - Shell Settings")
        print(Style.BRIGHT + Fore.CYAN + "3 - General Settings")
        print(Style.BRIGHT + Fore.CYAN + "4 - Exit" + Style.RESET_ALL)
        settings1_choice = input("> ")
        if settings1_choice == "1":
            account_settings()
        elif settings1_choice == "2":
            shell_settings()
        elif settings1_choice == "3":
            general_settings()
        elif settings1_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")
            continue
