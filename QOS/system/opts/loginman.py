import os
import json
import sys
import getpass
import base64
import time as tm
import system.core.features as features

from colorama import Fore, Style, init

init(autoreset=True)

def qos_login():
    try:
        with open(os.path.join("data", "config", "users.json"), "r") as qos_user_file:
            config = json.load(qos_user_file)
    except FileNotFoundError:
        print(Fore.RED + "File 'users.json' not found, please check the file path." + Style.RESET_ALL)
        features.clear()
        sys.exit(0)
    except json.JSONDecodeError:
        print(Fore.RED + "File 'users.json' is not a valid JSON file." + Style.RESET_ALL)
        features.clear()
        sys.exit(0)
    while True:
        try:
            print(f"{Fore.LIGHTGREEN_EX}Enter a user name to login: {Style.RESET_ALL}")
            username = input(">>> ").strip().lower().replace(" ", "_")
            if username == "":
                print(f"{Fore.RED}Please enter a user name.{Style.RESET_ALL}")
                continue
            if username == "exit":
                print(f"{Fore.RED}Exiting...{Style.RESET_ALL}")
                features.clear()
                sys.exit(0)
            user_found = False
            login_success = False
            de_password = ""
            for user_data in config.values():
                if user_data.get("username") == username:
                    user_found = True
                    password = user_data.get("password", "")
                    if not password:
                        login_success = True
                        break
                    else:
                        de_password = base64.b64decode(password).decode('utf-8')
                        break
            if not user_found:
                print(f"{Fore.RED}User not found. Please try again.{Style.RESET_ALL}")
                continue
            while True:
                try:
                    if login_success:
                        break
                    print(f"{Fore.LIGHTGREEN_EX}Enter password: {Style.RESET_ALL}")
                    input_password = getpass.getpass(">>> ")
                    if input_password == de_password:
                        login_success = True
                        with open(os.path.join(os.getcwd(), "data", "config", "config.json"), "r") as config_file:
                            config = json.load(config_file)
                        config["last_login"] = username
                        config["last_login_time"] = tm.strftime("%Y-%m-%d %H:%M:%S", tm.localtime())
                        with open(os.path.join(os.getcwd(), "data", "config", "config.json"), "w") as config_file:
                            json.dump(config, config_file, indent=4)
                        break
                    else:
                        print(Fore.RED + "Incorrect password, please try again." + Style.RESET_ALL)
                        continue
                except KeyboardInterrupt:
                    print(f"{Style.DIM}{Fore.GREEN}(Change User Account){Style.RESET_ALL}")
                    break
                except EOFError:
                    print(f"{Style.DIM}{Fore.GREEN}(Change User Account){Style.RESET_ALL}")
                    break
                except Exception as e:
                    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                    break
            if login_success:
                print()
                features.jump_print(" Welcome to QOS ", Fore.MAGENTA, Style.BRIGHT)
                print()
                return username
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            features.clear()
            sys.exit(0)
        except EOFError:
            print(f"{Style.DIM}{Fore.YELLOW}\nEOF detected. Exiting...{Style.RESET_ALL}")
            features.clear()
            sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
            features.clear()
            sys.exit(0)

def main(version, startup_title):
    print(Style.DIM + Fore.YELLOW + "Quarter OS Login Manager - " + version + Style.RESET_ALL + "\n")
    try:
        username = qos_login()
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        sys.exit(0)
    with open(os.path.join("data", "config", "config.json"), "r") as qos_config_file:
        config_data = json.load(qos_config_file)
    config_data["last_login"] = username
    with open(os.path.join("data", "config", "config.json"), "w") as qos_config_file:
        json.dump(config_data, qos_config_file, indent=4)
    print(" " + Fore.LIGHTBLUE_EX + str(startup_title) + Style.RESET_ALL + " ")
    tm.sleep(1)
    print(f"\n{Fore.GREEN}QOS will start in 3 seconds...{Style.RESET_ALL}")
    tm.sleep(3)
    if username:
        return username
    else:
        print(f"{Fore.RED}Error: Some wrong with Login Manager!{Style.RESET_ALL}")
        sys.exit(0)