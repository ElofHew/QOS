# QOS Advanced Options

import os
import json
from platform import system as pfs
from colorama import init as cinit
from colorama import Fore, Style
from system.core.features import cat

cinit(autoreset=True)

if pfs() == "Windows":
    os_type = "windows"
elif pfs() == "Darwin":
    os_type = "macos"
else:
    os_type = "linux"

config_path = os.path.join("data", "config", "config.json")

def change_startup_title():
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
        while True:
            print(f"{Fore.LIGHTGREEN_EX}Enter a new title for the Startup UI: {Fore.RESET}")
            new_title = str(input("> "))
            if new_title in "[]{}":
                print(f"{Fore.RED}Error: Some characters are not allowed in the title.{Style.RESET_ALL}")
                continue
            else:
                break
        config_file_old["startup_title"] = new_title
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.GREEN}Title changed successfully.{Style.RESET_ALL}")
        input("(Press Enter to continue)")
        return 1
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

def change_qos_logo_text():
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
        print(f"{Fore.LIGHTBLUE_EX}Choose a new type for the QOS logo: {Fore.RESET}\n(Enter directly to cancel the change)")
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
                break
            else:
                print(f"{Fore.RED}Error: Invalid input.{Style.RESET_ALL}")
                continue
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.GREEN}Logo type changed successfully.{Style.RESET_ALL}")
        input("(Press Enter to continue)")
        return 1
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

def manage_ads():
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
            activate_statue = config_file_old["activate_statue"]
            ad_statue = config_file_old["ad_statue"]
        if activate_statue == False:
            print(f"{Fore.YELLOW}You have not activated QOS Advanced Options yet! Please activate Quarter to disable ads.{Style.RESET_ALL}")
            return 0
        while True:
            print(f"{Fore.GREEN}# Manage ADs #{Style.RESET_ALL}")
            print(f"{Fore.CYAN}1. Enable ADs{Style.RESET_ALL}")
            print(f"{Fore.CYAN}2. Disable ADs{Style.RESET_ALL}")
            choice = input(f"{Fore.YELLOW}Choose an option (1/2): {Style.RESET_ALL}")
            if choice == "1":
                config_file_old["ad_statue"] = True
                print(f"{Fore.LIGHTGREEN_EX}ADs enabled successfully.{Style.RESET_ALL}")
                break
            elif choice == "2":
                config_file_old["ad_statue"] = False
                print(f"{Fore.LIGHTGREEN_EX}ADs disabled successfully.{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Error: Invalid choice. Please enter 1 or 2.{Style.RESET_ALL}")
                continue
        input("(Press Enter to continue)")
        with open(config_path, "w") as config_file_new:
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

def unknown_command_progression():
    try:
        with open(config_path, 'r') as shell_file:
            shell_data = json.load(shell_file)
        ucp = shell_data['unknown_command_progression']
        if ucp:
            print(Fore.LIGHTGREEN_EX + "Now when Kom Shell finds an unknown command, it will execute the command with the System." + Style.RESET_ALL)
            print(Fore.GREEN + "If you want Kom Shell to return an Error message, enter 'y', otherwise enter 'n'." + Style.RESET_ALL)
        else:
            print(Fore.LIGHTGREEN_EX + "Now when Kom Shell finds an unknown command, it will return an Error message." + Style.RESET_ALL)
            print(Fore.GREEN + "If you want Kom Shell to execute the command with the System, enter 'y', otherwise enter 'n'." + Style.RESET_ALL)
        while True:
            user_input = input("> ").lower()
            if user_input == 'y':
                shell_data["unknown_command_progression"] = not ucp
                break
            elif user_input == 'n':
                shell_data["unknown_command_progression"] = ucp
                break
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Style.RESET_ALL)
                continue
        with open(config_path, 'w') as new_shell_file:
            json.dump(shell_data, new_shell_file, indent=4)
        return 1
    except KeyboardInterrupt:
        print(Fore.YELLOW + "(KeyboardInterrupt)" + Style.RESET_ALL)
        return 0
    except json.JSONDecodeError as e:
        print(Fore.RED + "Error: Failed to decode JSON data. Error message: " + str(e) + Style.RESET_ALL)
        return 0
    except IOError as e:
        print(Fore.RED + "Error: Failed to write to config file. Error message: " + str(e) + Style.RESET_ALL)
        return 0
    except Exception as e:
        print(Fore.RED + "Error: An unexpected error occurred. Error message: " + str(e) + Style.RESET_ALL)
        return 0