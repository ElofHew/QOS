# QOS OOBE Module

import os
import sys
import time
import json
import subprocess
from colorama import init as cinit
from colorama import Fore, Style

import system.core.features as features
import system.core.login as login
from system.core.runs import run_system_kits as rsk

cinit(autoreset=True)

class OOBE:
    # init method
    def __init__(self):
        pass

    # Ask to activate QOS
    def activate_qos(self):
        while True:
            features.clear()
            print(f"{Fore.LIGHTGREEN_EX}Please enter the activation code to activate QOS.{Style.RESET_ALL}")
            print(f"{Fore.LIGHTBLUE_EX}(If you don't have an activation code, please go to https://os.drevan.xyz/qos/activate/ to get one){Style.RESET_ALL}")
            print(f"{Fore.LIGHTMAGENTA_EX}(Or you can skip this step (Input pass to skip), activate QOS later.){Style.RESET_ALL}")
            code = input("> ")
            if code == "pass":
                print(f"{Fore.LIGHTGREEN_EX}Skip activation, Please activate QOS later.{Style.RESET_ALL}")
                break
            activate_condition = rsk("activate", ["-a", code])
            if activate_condition == 0:
                print(f"\n{Fore.LIGHTGREEN_EX}Congratulations! QOS has been activated successfully!{Style.RESET_ALL}")
                break
            else:
                input("(Press any key to try again.)")
                continue
        input("(Press any key to continue.)")

    # Create System Name
    def create_system_name(self, username):
        features.clear()
        print(f"{Fore.LIGHTGREEN_EX}Please enter a system name.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTBLUE_EX}Example: {Fore.LIGHTGREEN_EX}{username}-qos{Fore.RESET}")
        system_name = login.make_system_name()
        if system_name == 10:
            print(f"{Fore.RED}Error: Keyboard interrupt detected.{Style.RESET_ALL}")
            sys.exit(17)
        if system_name:
            print(f"{Fore.LIGHTGREEN_EX}Your system name is {Fore.LIGHTBLUE_EX}{system_name}{Style.RESET_ALL}")

    # Add User Account
    def add_user_account(self):
        user_data = {
            "user1": {
                "username": "root",
                "password": "MTIzNDU2"
            },
            "user2": {
                "username": "admin",
                "password": "MTIzNDU2"
            },
            "user3": {
                "username": "guest",
                "password": None
            }
        }
        try:
            with open('data/config/users.json', 'r') as user_file:
                user_data_old = json.load(user_file)
            # 检查 user_data_old 是否包含预期的键和用户名
            if len(user_data_old) <= 3 and \
               user_data_old.get("user1", {}).get("username") != "root" or \
               user_data_old.get("user2", {}).get("username") != "admin" or \
               user_data_old.get("user3", {}).get("username") != "guest":
                with open('data/config/users.json', 'w') as user_file:
                    json.dump(user_data, user_file, indent=4)
            else:
                # 如果不符合预期格式，直接覆盖
                with open('data/config/users.json', 'w') as user_file:
                    json.dump(user_data, user_file, indent=4)
        except (FileNotFoundError, json.JSONDecodeError):
            # 如果文件不存在或内容不是有效的 JSON，创建新文件
            with open('data/config/users.json', 'w') as user_file:
                json.dump(user_data, user_file, indent=4)
        # Set Default User Account
        print(f"{Fore.LIGHTGREEN_EX}Who will use QOS? \n{Fore.LIGHTBLUE_EX}(Enter a default user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.){Style.RESET_ALL}")
        default_user = login.confirm_username()
        if default_user == 10:
            print(f"{Fore.RED}Error: Keyboard interrupt detected.{Style.RESET_ALL}")
            sys.exit(17)
        # Set New User Account
        print(f"{Fore.LIGHTGREEN_EX}Please set a password for your account.\n{Fore.LIGHTBLUE_EX}(Enter a password in 8 characters or less, and don't use spaces.){Style.RESET_ALL}")
        user_password = login.confirm_password()
        if user_password == 10:
            print(f"{Fore.RED}Error: Keyboard interrupt detected.{Style.RESET_ALL}")
            sys.exit(17)
        # Write User Account to users.json
        print(f"{Fore.LIGHTGREEN_EX}Creating user account...\n{Style.RESET_ALL}")
        create_condition = login.confirm_user_account(default_user, user_password)
        if create_condition:
            print(f"{Fore.LIGHTGREEN_EX}Great! Your user account has been created successfully!\n{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Failed to create user account, please try again.{Style.RESET_ALL}")
            self.add_user_account()
        return default_user

    # EULA Module
    def eula(self):
        print(f"{Style.BRIGHT}{Fore.CYAN}Please read the EULA of QOS and accept it to continue.{Style.RESET_ALL}\n")
        features.cat("system/etc/eula.txt")
        input("\n(Press any key to continue.)")
        print(f"\n{Style.BRIGHT}{Fore.CYAN}Do you accept the EULA? (y/n){Style.RESET_ALL}")
        while True:
            choice = input("> ").lower()
            if choice == "y":
                break
            elif choice == "n":
                print(f"{Style.BRIGHT}{Fore.RED}You can't use QOS without accepting the EULA.{Style.RESET_ALL}")
                sys.exit(0)
            else:
                print(f"{Style.BRIGHT}{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")

    # OOBE Main Method
    def main(self):
        with open('data/config/config.json', 'r') as config_file:
            config_data = json.load(config_file)
        oobe_condition = config_data.get("oobe", True)
        if not oobe_condition:
            print(f"{Fore.RED}You have already set up QOS.{Style.RESET_ALL}")
            sys.exit(0)
        # Start
        features.clear()
        print(f"{Style.DIM}{Fore.YELLOW}Quarter OS OOBE - Alpha 0.2{Style.RESET_ALL}\n")
        time.sleep(1)
        self.eula()
        features.clear()
        features.jump_print("Welcome to QOS!", Fore.GREEN, Style.BRIGHT)
        time.sleep(1)
        print(f"{Style.BRIGHT}{Fore.MAGENTA}This is the Quarter OS Out-of-Box-Experience (OOBE).\n{Style.RESET_ALL}")
        username = self.add_user_account()
        time.sleep(1)
        self.create_system_name(username)
        time.sleep(1)
        self.activate_qos()
        features.clear()
        # Write OOBE condition to config.json
        with open('data/config/config.json', 'r+') as config_file:
            config_data = json.load(config_file)
            config_data["oobe"] = False
            config_file.seek(0)
            json.dump(config_data, config_file, indent=4)
            config_file.truncate()
        print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}QOS has been set up successfully!\nWish you can enjoy QOS!{Style.RESET_ALL}")
        input("(Press any key to continue.)")
        time.sleep(1)
        features.clear()
        return 1
