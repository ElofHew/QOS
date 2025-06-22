# QOS Kom Shell Settings

import json
import colorama

import core.options as options
import core.login as login
import core.shell as shell

colorama.init(autoreset=True)

def account_settings():
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "# Account Settings #")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "1 - Add User")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "2 - Remove User")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "3 - Change Password")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "4 - Back" + colorama.Style.RESET_ALL)
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
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "# Shell Settings #")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "1 - Change Shell Theme")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "2 - Unknown Command Progression")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "3 - Back" + colorama.Style.RESET_ALL)
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
    print(colorama.Style.BRIGHT + colorama.Fore.GREEN + "# General Settings #")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "1 - Change Startup Title")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "2 - Change QOS Logo Text")
    print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "3 - Back" + colorama.Style.RESET_ALL)
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
        with open("config/config.json", "r") as qos_config_file:
            config = json.load(qos_config_file)
        print(colorama.Style.BRIGHT + colorama.Fore.BLUE + "$ QOS Settings $")
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "1 - Account Settings")
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "2 - Shell Settings")
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "3 - General Settings")
        print(colorama.Style.BRIGHT + colorama.Fore.CYAN + "4 - Exit" + colorama.Style.RESET_ALL)
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
