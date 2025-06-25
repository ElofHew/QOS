# QOS OOBE模块
import colorama
import sys
import time
import json

import system.core.options as options
import system.core.qoscore as qoscore
import system.core.login as login
import system.core.cmds as cmds

colorama.init(autoreset=True)

with open('data/config/config.json', 'r') as config_file:
    config = json.load(config_file)

os_type = qoscore.check_os()
os_path = qoscore.check_path()

class OOBE:
    # init method
    def __init__(self):
        pass

    # Configure "data" directory
    def set_more_dir(self):
        print(f"{colorama.Fore.BLUE}We are setting up QOS directories.{colorama.Style.RESET_ALL}")
        dir_cdt = qoscore.check_more_dir()
        if not dir_cdt:
            print(f"{colorama.Fore.GREEN}Directories have been set up successfully.{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.RED}Error: Failed to set up directories.{colorama.Style.RESET_ALL}")
            sys.exit(1)
    
    # Add User Account
    def add_user_account(self):
        # Set Default User Account
        print(colorama.Fore.LIGHTGREEN_EX + "Who will use QOS? \n" + colorama.Fore.LIGHTBLUE_EX + "(Enter a default user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.)" + colorama.Style.RESET_ALL)
        default_user = login.confirm_username()
        # Set New User Account
        print(colorama.Fore.LIGHTGREEN_EX + "Please set a password for your account.\n" + colorama.Fore.LIGHTBLUE_EX + "(Enter a password in 8 characters or less, and don't use spaces.)" + colorama.Style.RESET_ALL)
        user_password = login.confirm_password()
        # Write User Account to users.json
        print(colorama.Fore.LIGHTGREEN_EX + "Creating user account...\n" + colorama.Style.RESET_ALL)
        create_condition = login.confirm_user_account(default_user, user_password)
        if create_condition:
            print(colorama.Fore.LIGHTGREEN_EX + "Great! Your user account has been created successfully!\n" + colorama.Style.RESET_ALL)
        else:
            print(colorama.Fore.RED + "Error: Failed to create user account, please try again." + colorama.Style.RESET_ALL)
            self.add_user_account()

    # EULA Module
    def eula(self):
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Please read the EULA of QOS and accept it to continue.{colorama.Style.RESET_ALL}\n")
        options.cat("system/etc/eula.txt")
        input("")
        cmds.clear()
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.CYAN}Do you accept the EULA? (y/n){colorama.Style.RESET_ALL}")
        while True:
            choice = input("> ").lower()
            if choice == "y":
                break
            elif choice == "n":
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}You can't use QOS without accepting the EULA.{colorama.Style.RESET_ALL}")
                sys.exit(1)
            else:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Invalid input. Please enter 'y' or 'n'.{colorama.Style.RESET_ALL}")

    # OOBE Main Method
    def main(self):
        cmds.clear()
        print(f"{colorama.Style.DIM}{colorama.Fore.YELLOW}QuarterOS OOBE - Alpha 0.2{colorama.Style.RESET_ALL}\n")
        time.sleep(1)
        self.eula()
        cmds.clear()
        options.jump_print("Welcome to QOS!", colorama.Fore.GREEN, colorama.Style.BRIGHT)
        time.sleep(1)
        print(colorama.Style.BRIGHT + colorama.Fore.MAGENTA + "This is the Quarter OS Out-of-Box-Experience (OOBE).\n" + colorama.Style.RESET_ALL)
        self.add_user_account()
        self.set_more_dir()
        time.sleep(1)
        cmds.clear()
        print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTGREEN_EX}QOS has been set up successfully!\nWish you can enjoy QOS!{colorama.Style.RESET_ALL}")
        input("(Press any key to continue.)")
        time.sleep(1)
        cmds.clear()