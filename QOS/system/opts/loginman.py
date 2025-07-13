import os
import json
import sys
import time
import system.core.login as login

from colorama import Fore, Style, init

init(autoreset=True)

def main(version, startup_title):
    print(Style.DIM + Fore.YELLOW + "Quarter OS Login Manager - " + version + Style.RESET_ALL + "\n")
    try:
        username = login.qos_login()
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        sys.exit(0)
    with open(os.path.join("data", "config", "config.json"), "r") as qos_config_file:
        config_data = json.load(qos_config_file)
    config_data["last_login"] = username
    with open(os.path.join("data", "config", "config.json"), "w") as qos_config_file:
        json.dump(config_data, qos_config_file, indent=4)
    print(" " + Fore.LIGHTBLUE_EX + str(startup_title) + Style.RESET_ALL + " ")
    time.sleep(1)
    print(f"\n{Fore.GREEN}QOS will start in 3 seconds...{Style.RESET_ALL}")
    time.sleep(3)
    if username:
        return username
    else:
        print(f"{Fore.RED}Error: Some wrong with Login Manager!{Style.RESET_ALL}")
        sys.exit(0)