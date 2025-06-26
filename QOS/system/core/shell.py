# QOS Kom Shell Configure Module

import os
from colorama import init as cinit
from colorama import Fore, Style, Back
import json

cinit(autoreset=True)

with open('data/config/shell.json', 'r') as config_file:
    config = json.load(config_file)
    ucp = config['unknown_command_progression']
    theme = config['theme']

def unknown_command_progression():
    if ucp:
        print(Fore.LIGHTGREEN_EX + "Now when Kom Shell finds an unknown command, it will execute the command with the System." + Style.RESET_ALL)
        print(Fore.GREEN + "If you want Kom Shell to return an Error message, enter 'y', otherwise enter 'n'." + Style.RESET_ALL)
    else:
        print(Fore.LIGHTGREEN_EX + "Now when Kom Shell finds an unknown command, it will return an Error message." + Style.RESET_ALL)
        print(Fore.GREEN + "If you want Kom Shell to execute the command with the System, enter 'y', otherwise enter 'n'." + Style.RESET_ALL)
    while True:
        user_input = input("> ").lower()
        if user_input == 'y':
            config["unknown_command_progression"] = not ucp
            break
        elif user_input == 'n':
            config["unknown_command_progression"] = ucp
            break
        else:
            print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Style.RESET_ALL)
            continue
    with open('data/config/shell.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)
