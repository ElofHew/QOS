# QOS Advanced Options

import os
import json
from colorama import init as cinit
from colorama import Fore, Style
from system.core.features import cat

cinit(autoreset=True)

config_path = os.path.join("data", "config", "config.json")

def change_startup_title(string):
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
        new_title = string.strip()
        if any(char in new_title for char in "[]{}"):
            print(f"{Fore.RED}Error: Some characters are not allowed in the title.{Style.RESET_ALL}")
            return 1
        config_file_old["startup_title"] = new_title
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}Title changed successfully.{Style.RESET_ALL}")
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1

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
                return 0
            else:
                print(f"{Fore.RED}Error: Invalid input.{Style.RESET_ALL}")
                continue
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}Logo type changed successfully.{Style.RESET_ALL}")
        return 0
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1

def manage_ads(condition):
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
            activate_statue = config_file_old["activate_statue"]
            ad_statue = config_file_old["ad_statue"]
        if activate_statue == False:
            print(f"{Fore.YELLOW}You have not activated QOS Advanced Options yet! Please activate Quarter to disable ads.{Style.RESET_ALL}")
            return 0
        if condition == "check":
            if ad_statue:
                print(f"{Fore.LIGHTGREEN_EX}Ads are enabled.{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Ads are disabled.{Style.RESET_ALL}")
            return 0
        elif condition == "enable":
            ad_statue = True
            print(f"{Fore.LIGHTGREEN_EX}Ads are enabled.{Style.RESET_ALL}")
        elif condition == "disable":
            ad_statue = False
            print(f"{Fore.LIGHTGREEN_EX}Ads are disabled.{Style.RESET_ALL}")
        else:
            return 1
        config_file_old["ad_statue"] = ad_statue
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1

def unknown_command_progression(condition):
    try:
        with open(config_path, 'r') as shell_file:
            shell_data = json.load(shell_file)
        ucp = shell_data.get("unknown_command_progression", False)
        if condition == "check":
            if ucp:
                print(f"{Fore.LIGHTGREEN_EX}Unknown command progression is enabled.{Style.RESET_ALL}")
            else:
                print(f"{Fore.LIGHTGREEN_EX}Unknown command progression is disabled.{Style.RESET_ALL}")
            return 0
        elif condition == "enable":
            ucp = True
            print(f"{Fore.LIGHTGREEN_EX}Unknown command progression is enabled.{Style.RESET_ALL}")
        elif condition == "disable":
            ucp = False
            print(f"{Fore.LIGHTGREEN_EX}Unknown command progression is disabled.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Invalid input. {Style.RESET_ALL}Please enter 'check', 'enable', or 'disable'.")
            return 1
        shell_data['unknown_command_progression'] = ucp
        with open(config_path, 'w') as new_shell_file:
            json.dump(shell_data, new_shell_file, indent=4)
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1

def set_startup_timeout(timeout):
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
        if timeout == "default":
            sto = 3
        else:
            timeout = float(timeout)  # 假设 timeout 是字符串，需要转换为浮点数
            if 0 <= timeout <= 10:
                sto = round(timeout, 1)
            else:
                print(f"{Fore.RED}Error: You must enter a number between 0 and 10.{Style.RESET_ALL}")
                return 1
        config_file_old["startup_timeout"] = sto
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}Startup timeout changed to {sto} successfully.{Style.RESET_ALL}")
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1

def set_theme(theme):
    try:
        with open(config_path, "r") as config_file_old:
            config_file_old = json.load(config_file_old)
        if theme == "help":
            print(f"{Fore.LIGHTBLUE_EX}Available themes: {Fore.RESET}\ndefault\nlight\ndark")
            return 0
        elif theme == "default":
            config_file_old["theme"] = "default"
        elif theme == "light":
            config_file_old["theme"] = "light"
        elif theme == "dark":
            config_file_old["theme"] = "dark"
        else:
            print(f"{Fore.RED}Error: Invalid input. {Style.RESET_ALL}Please use 'help' to see available options.")
            return 1
        with open(config_path, "w") as config_file_new:
            json.dump(config_file_old, config_file_new, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}Theme changed successfully.{Style.RESET_ALL}")
        return 0
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode JSON data. Error message: {e}{Style.RESET_ALL}")
        return 1
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to write to config file. Error message: {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: An unexpected error occurred. Error message: {e}{Style.RESET_ALL}")
        return 1