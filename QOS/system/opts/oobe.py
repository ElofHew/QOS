# QOS OOBE模块
import sys
import time
import json
from colorama import init as cinit
from colorama import Fore, Style, Back

import system.core.options as options
import system.core.qoscore as qoscore
import system.core.login as login
import system.core.cmds as cmds

cinit(autoreset=True)

os_type = qoscore.check_os()
os_path = qoscore.check_path()

class OOBE:
    # init method
    def __init__(self):
        pass
    
    # Ask to activate QOS
    def activate_qos(self):
        while True:
            print(f"{Fore.LIGHTGREEN_EX}Please enter the activation code to activate QOS.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLUE_EX}(If you don't have an activation code, please go to https://os.drevan.xyz/qos/activate/ to get one){Style.RESET_ALL}")
            print(f"{Fore.LIGHTMAGENTA_EX}(Or you can skip this step (Input pass to skip), activate QOS later.){Style.RESET_ALL}")
            code = input("> ")
            if code == "pass":
                print(f"{Fore.LIGHTGREEN_EX}Skip activation, Please activate QOS later.{Style.RESET_ALL}")
                break
            activate_condition = cmds.activate(None, code)
            if activate_condition:
                print(f"\n{Fore.LIGHTGREEN_EX}Congratulations! QOS has been activated successfully!{Style.RESET_ALL}")
                break
            else:
                print(f"\n{Fore.RED}Invalid activation code. Please try again.{Style.RESET_ALL}")
                time.sleep(1)
                continue
        input("(Press any key to continue.)")

    # Add User Account
    def add_user_account(self):
        # Set Default User Account
        print(Fore.LIGHTGREEN_EX + "Who will use QOS? \n" + Fore.LIGHTBLUE_EX + "(Enter a default user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.)" + Style.RESET_ALL)
        default_user = login.confirm_username()
        if default_user == 10:
            print(Fore.RED + "Error: Keyboard interrupt detected." + Style.RESET_ALL)
            sys.exit(1)
        # Set New User Account
        print(Fore.LIGHTGREEN_EX + "Please set a password for your account.\n" + Fore.LIGHTBLUE_EX + "(Enter a password in 8 characters or less, and don't use spaces.)" + Style.RESET_ALL)
        user_password = login.confirm_password()
        if user_password == 10:
            print(Fore.RED + "Error: Keyboard interrupt detected." + Style.RESET_ALL)
            sys.exit(1)
        # Write User Account to users.json
        print(Fore.LIGHTGREEN_EX + "Creating user account...\n" + Style.RESET_ALL)
        create_condition = login.confirm_user_account(default_user, user_password)
        if create_condition:
            print(Fore.LIGHTGREEN_EX + "Great! Your user account has been created successfully!\n" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Error: Failed to create user account, please try again." + Style.RESET_ALL)
            self.add_user_account()

    # EULA Module
    def eula(self):
        print(f"{Style.BRIGHT}{Fore.CYAN}Please read the EULA of QOS and accept it to continue.{Style.RESET_ALL}\n")
        options.cat("system/etc/eula.txt")
        input("\n(Press any key to continue.)")
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Do you accept the EULA? (y/n){Style.RESET_ALL}")
        while True:
            choice = input("> ").lower()
            if choice == "y":
                break
            elif choice == "n":
                print(f"{Style.BRIGHT}{Fore.RED}You can't use QOS without accepting the EULA.{Style.RESET_ALL}")
                sys.exit(1)
            else:
                print(f"{Style.BRIGHT}{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")

    # OOBE Main Method
    def main(self):
        with open('data/config/config.json', 'r') as config_file:
            config_data = json.load(config_file)
        oobe_condition = config_data.get("oobe", True)
        cmds.clear()
        if oobe_condition:
            pass
        else:
            print(f"{Fore.RED}You have already set up QOS.{Style.RESET_ALL}")
            sys.exit(0)
        config_file.close()
        print(f"{Style.DIM}{Fore.YELLOW}Quarter OS OOBE - Alpha 0.2{Style.RESET_ALL}\n")
        time.sleep(1)
        self.eula()
        cmds.clear()
        options.jump_print("Welcome to QOS!", Fore.GREEN, Style.BRIGHT)
        time.sleep(1)
        print(Style.BRIGHT + Fore.MAGENTA + "This is the Quarter OS Out-of-Box-Experience (OOBE).\n" + Style.RESET_ALL)
        self.add_user_account()
        time.sleep(1)
        cmds.clear()
        self.activate_qos()
        cmds.clear()
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}QOS has been set up successfully!\nWish you can enjoy QOS!{Style.RESET_ALL}")
        input("(Press any key to continue.)")
        # Write OOBE condition to config.json
        with open('data/config/config.json', 'r') as old_config_file:
            old_config = json.load(old_config_file)
        old_config["oobe"] = False
        with open('data/config/config.json', 'w') as new_config_file:
            json.dump(old_config, new_config_file, indent=4)
        time.sleep(1)
        cmds.clear()