# QOS Kom Shell Settings

import sys
from os import system as oss
from os import path as osp
from platform import system as pf
from colorama import init as cinit
from colorama import Fore

sys.path.insert(0, osp.abspath(osp.join(osp.dirname(__file__), '..')))

try:
    import system.core.login as login
    import system.core.shell as shell
    import system.core.options as options
except ImportError as e:
    print(f"Error: {e}")
    input("(Press enter to continue...)")
    exit()

cinit(autoreset=True)

pfs = pf().lower()

def account_settings():
    while True:
        if pfs == "windows":
            oss("cls")
        else:
            oss("clear")
        print(Fore.GREEN + "# Account Settings #")
        print(Fore.CYAN + "1 - Add User")
        print(Fore.CYAN + "2 - Remove User")
        print(Fore.CYAN + "3 - Change Password")
        print(Fore.CYAN + "4 - Change System Name" + Fore.RESET)
        print(Fore.CYAN + "5 - Back" + Fore.RESET)
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
            login.make_system_name()
            continue
        elif settings2_choice == "5":
            return
        else:
            print("Invalid choice. Please try again.")
            input("(Press enter to continue...)")
            continue

def shell_settings():
    while True:
        if pfs == "windows":
            oss("cls")
        else:
            oss("clear")
        print(Fore.GREEN + "# Shell Settings #")
        print(Fore.CYAN + "1 - Change Shell Theme")
        print(Fore.CYAN + "2 - Unknown Command Progression")
        print(Fore.CYAN + "3 - Back" + Fore.RESET)
        settings2_choice = input("> ")
        if settings2_choice == "1":
            print("Coming soon.")
            continue
        elif settings2_choice == "2":
            shell.unknown_command_progression()
            continue
        elif settings2_choice == "3":
            return
        else:
            print("Invalid choice. Please try again.")
            input("(Press enter to continue...)")
            continue

def general_settings():
    while True:
        if pfs == "windows":
            oss("cls")
        else:
            oss("clear")
        print(Fore.GREEN + "# General Settings #")
        print(Fore.CYAN + "1 - Change Startup Title")
        print(Fore.CYAN + "2 - Change QOS Logo Text")
        print(Fore.CYAN + "3 - Manage ADs")
        print(Fore.CYAN + "4 - Back" + Fore.RESET)
        settings2_choice = input("> ")
        if settings2_choice == "1":
            options.change_startup_title()
            continue
        elif settings2_choice == "2":
            options.change_qos_logo_text()
            continue
        elif settings2_choice == "3":
            options.manage_ads()
            continue
        elif settings2_choice == "4":
            return
        else:
            print("Invalid choice. Please try again.")
            input("(Press enter to continue...)")
            continue

def main():
    while True:
        if pfs == "windows":
            oss("cls")
        else:
            oss("clear")
        print(Fore.GREEN + "$ Quarter OS Settings $")
        print(Fore.CYAN + "1 - Account Settings")
        print(Fore.CYAN + "2 - Shell Settings")
        print(Fore.CYAN + "3 - General Settings")
        print(Fore.CYAN + "4 - Exit" + Fore.RESET)
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
            input("(Press enter to continue...)")
            continue
