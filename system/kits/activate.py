import re
import sys
import json
from colorama import Fore, Style, init

init(autoreset=True)

try:
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
    activate_code = config.get("activate_code", "")
    qos_edition = config.get("qos_edition", "")
    activate_statue = config.get("activate_statue", False)
except FileNotFoundError:
    print(f"{Fore.RED}Error: Config.json not found. Please run Quarter OS setup first.{Style.RESET_ALL}")   
    sys.exit(1)
except json.JSONDecodeError:
    print(f"{Fore.RED}Error: Config.json is corrupted. Please run Quarter OS setup again.{Style.RESET_ALL}")
    sys.exit(1)
except KeyError:
    print(f"{Fore.RED}Error: Config.json is missing some keys. Please run Quarter OS setup again.{Style.RESET_ALL}")
    sys.exit(1)

__usage__ = """Quarter OS Activate Usage:
-a <activate_code> : Activate Quarter OS
-ck : Check Quarter OS activation status
-d : Deactivate Quarter OS
"""

def activate(code):
    global activate_statue, config
    try:
        if activate_statue:
            while True:
                print(f"{Fore.YELLOW}WARNING: You have already activated Quarter OS. Are you sure to activate again? (y/n){Fore.RESET}")
                cfm = input("> ").strip().lower()
                if cfm == "y":
                    break
                elif cfm == "n":
                    return 0
                else:
                    print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        # Check activate code format
        if len(code) != 5 or not re.match(r'^[SHPUL]\d{4}', code) or not (1000 <= int(code[1:]) <= 9999):
            raise ValueError
        else:
            qos_act_type = {
                "S": "Starter",
                "H": "Home",
                "P": "Professional",
                "U": "Ultimate",
                "L": "LongTermSupport"
            }.get(code[0], "Unknown")
        # Update Config.json
        config["activate_code"] = code
        config["qos_edition"] = qos_act_type
        config["activate_statue"] = True
        with open("data/config/config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        # Reopen Config.json to fetch updated data
        with open("data/config/config.json", "r") as config_file:
            config = json.load(config_file)
            activate_code = config["activate_code"]
            qos_edition = config["qos_edition"]
            activate_statue = config["activate_statue"]
        print(f"{Fore.GREEN}Quarter OS activated successfully.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Your Quarter OS edition is {Fore.LIGHTGREEN_EX}{qos_edition} Edition{Fore.CYAN} and your activate code is {Fore.LIGHTGREEN_EX}{activate_code}{Fore.CYAN}.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}You best restart Quarter OS to take effect. (Except for OOBE){Style.RESET_ALL}")
        sys.exit(0)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Config.json not found. Please run Quarter OS setup first.{Style.RESET_ALL}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Config.json is corrupted. Please run Quarter OS setup again.{Style.RESET_ALL}")
        sys.exit(1)
    except KeyError:
        print(f"{Fore.RED}Error: Config.json is missing some keys. Please run Quarter OS setup again.{Style.RESET_ALL}")
        sys.exit(1)
    except ValueError:
        print(f"{Fore.RED}Error: Invalid activate code. Please enter a valid code.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}You can get the activate code from the Quarter OS website: https://os.drevan.xyz/qos/activate. {Style.RESET_ALL}")
        sys.exit(1)
    except KeyboardInterrupt:
        print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
        sys.exit(1)

def deactivate():
    try:
        config["activate_code"] = ""
        config["qos_edition"] = ""
        config["activate_statue"] = False
        with open("data/config/config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        print(f"{Fore.GREEN}Quarter OS deactivated successfully.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please restart Quarter OS to take effect.{Style.RESET_ALL}")
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Config.json not found. Please run Quarter OS setup first.{Style.RESET_ALL}")
        return 1
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Config.json is corrupted. Please run Quarter OS setup again.{Style.RESET_ALL}")
        return 1
    except KeyError:
        print(f"{Fore.RED}Error: Config.json is missing some keys. Please run Quarter OS setup again.{Style.RESET_ALL}")
        return 1

def check():
    if activate_statue:
        print(f"{Fore.GREEN}Quarter OS is activated.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Your Quarter OS edition is {Fore.LIGHTGREEN_EX}{qos_edition} Edition{Fore.CYAN} and your activate code is {Fore.LIGHTGREEN_EX}{activate_code}{Fore.CYAN}.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Quarter OS is not activated.{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Please activate Quarter OS by {Fore.LIGHTGREEN_EX}activate -a <activate_code>{Fore.CYAN}.\nYou can get the activate code from the Quarter OS website: https://os.drevan.xyz/qos/activate. {Style.RESET_ALL}")
    return 0

if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "-a":
            if sys.argv[2:]:
                activate(sys.argv[2])
            else:
                print(f"{Fore.RED}Error: No activate code provided.{Style.RESET_ALL}")
                sys.exit(1)
        elif sys.argv[1] == "-d":
            deactivate()
        elif sys.argv[1] == "-ck":
            check()
        else:
            print(f"{Fore.RED}Error: Unknown option '{sys.argv[1]}'.{Style.RESET_ALL}")
            print(__usage__)
            sys.exit(1)
    else:
        print(__usage__)
        sys.exit(0)