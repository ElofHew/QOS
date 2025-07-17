# QOS Login Module
try:
    # Standard Library Modules
    import os
    import json
    import sys
    import time as tm
    import base64
    import pathlib
    import getpass
    # Third-Party Modules
    from colorama import init as cinit
    from colorama import Fore, Style, Back
    # Core Modules
    import system.core.features as features
    import system.core.cmds as cmds
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

cinit(autoreset=True)

def make_system_name():
    qos_config_path = pathlib.Path("data/config/config.json")
    if not qos_config_path.exists():
        print(f"{Style.BRIGHT}{Fore.RED}config.json not found.{Style.RESET_ALL}")
        return None
    with open(qos_config_path, "r") as qos_config_file:
        config = json.load(qos_config_file)
    while True:
        try:
            system_name = input(Fore.LIGHTMAGENTA_EX + "System Name" + Style.RESET_ALL + " : ")
            if system_name == "":
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a system name.{Style.RESET_ALL}")
                continue
            elif len(system_name) > 20:
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot be longer than 20 characters.{Style.RESET_ALL}")
                continue
            elif " " in system_name:
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot contain spaces. You can use '_' instead.{Style.RESET_ALL}")
                continue
            elif any(char in "!@#$%^&*()[]{};:,./<>?\|`~=+" for char in system_name):
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot contain special characters. You can only use '_' and '-'.{Style.RESET_ALL}")
                continue
            else:
                # Check if system name already exists
                print(f"{Fore.LIGHTGREEN_EX}Your system name is '{system_name}'. Is this correct? (y/n){Style.RESET_ALL}")
                if not str(input("> ")).lower() == "y":
                    continue
                else:
                    break
        except KeyboardInterrupt:
            print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
            return 10
    with open(qos_config_path, "w") as qos_config_file:
        config["system_name"] = system_name
        json.dump(config, qos_config_file, indent=4)
    return system_name

def confirm_username():
    user_file_path = pathlib.Path("data/config/users.json")
    # Make sure users.json exists
    if not user_file_path.exists():
        print(f"{Style.BRIGHT}{Fore.RED}users.json not found.{Style.RESET_ALL}")
        return None
    with open(user_file_path, "r") as qos_user_file:
        config = json.load(qos_user_file)
    while True:
        try:
            username = input(Fore.LIGHTMAGENTA_EX + "UserName" + Style.RESET_ALL + " : ")
            if username == "":
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a default user name.{Style.RESET_ALL}")
                continue
            elif len(username) > 10:
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot be longer than 10 characters.{Style.RESET_ALL}")
                continue
            elif any(char.isupper() for char in username):
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain uppercase letters.{Style.RESET_ALL}")
                continue
            elif " " in username:
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain spaces. You can use '_' instead.{Style.RESET_ALL}")
                continue
            elif any(char in "!@#$%^&*()[]{};:,./<>?\|`~-=+" for char in username):
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain special characters. You can only use '_'.{Style.RESET_ALL}")
                continue
            elif username[0].isdigit():
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot start with a number.{Style.RESET_ALL}")
                continue
            else:
                # Check if username already exists
                existing_usernames = {user_data["username"] for user_data in config.values()}
                if username in ["admin", "root", "guest", "superuser", "su", "exit"]:
                    print(f"{Style.BRIGHT}{Fore.RED}User name cannot be one of the reserved keywords.{Style.RESET_ALL}")
                    continue
                elif username in existing_usernames:
                    print(f"{Style.BRIGHT}{Fore.RED}User '{username}' already exists. Please choose another name.{Style.RESET_ALL}")
                    continue
                else:
                    return username
        except KeyboardInterrupt:
            print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
            return 10

def confirm_password():
    while True:
        try:
            password = input(Fore.LIGHTMAGENTA_EX + "Password" + Style.RESET_ALL + " : ")
            if password == "":
                print(f"{Style.BRIGHT}{Fore.LIGHTGREEN_EX}No password? (y/n){Style.RESET_ALL}")
                if str(input("> ")).lower() == "y":
                    password = None
                    return password
                else:
                    continue
            elif len(password) > 8:
                print(f"{Style.BRIGHT}{Fore.RED}Password cannot be longer than 8 characters.{Style.RESET_ALL}")
                continue
            elif " " in password:
                print(f"{Style.BRIGHT}{Fore.RED}Password cannot contain spaces.{Style.RESET_ALL}")
                continue
            else:
                return password
        except KeyboardInterrupt:
            print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
            return 10

def confirm_user_account(username, password):
    try:
        # Read existing user data from file
        user_file_path = pathlib.Path("data/config/users.json")
        if user_file_path.exists():
            with open(user_file_path, "r") as qos_user_file:
                config = json.load(qos_user_file)
        else:
            config = {}
        # Write new user data to file
        user_index = 1
        while f"user{user_index}" in config:
            user_index += 1
        new_user_key = f"user{user_index}"
        if password is None:
            en_password = None
        else:
            en_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        config[new_user_key] = {
            "username": username,
            "password": en_password
        }
        confirmation = input(f"{Fore.LIGHTCYAN_EX}Are you sure you want to add user '{username}'? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirmation.lower() == 'y':
            with open(user_file_path, "w") as qos_user_file:
                json.dump(config, qos_user_file, indent=4)
            print(f"{Fore.LIGHTGREEN_EX}User {username} added successfully.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.YELLOW}User addition canceled.{Style.RESET_ALL}")
            return False
    except KeyboardInterrupt:
        print(f"{Fore.RED}Operation canceled.{Style.RESET_ALL}")
        return False

def add_user():
    # Set new user name
    print(Fore.LIGHTGREEN_EX + "Enter a new username.\n" + Fore.LIGHTBLUE_EX + "(Enter a user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.)" + Style.RESET_ALL)
    new_username = confirm_username()
    # Set new user password
    print(Fore.LIGHTGREEN_EX + "Enter a new password\n" + Fore.LIGHTBLUE_EX + "(Enter a password in 8 characters or less, and don't use spaces.)" + Style.RESET_ALL)
    new_password = confirm_password()
    # Write new user data to file
    confirm_user_account(new_username, new_password)

def remove_user():
    user_file_path = pathlib.Path("data/config/users.json")
    if user_file_path.exists():
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
    else:
        print("File 'users.json' not found, please check the file path.")
        cmds.clear()
        return
    while True:
        try:
            username_to_remove = input(f"{Fore.LIGHTGREEN_EX}Enter a username to remove: {Style.RESET_ALL}")
            if username_to_remove == "root" or "admin" or "guest" or "superuser" or "su":
                print(f"{Fore.RED}User '{username_to_remove}' cannot be removed.{Style.RESET_ALL}")
                continue
            else:
                break
        except KeyboardInterrupt:
            print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
            return
    user_key_to_remove = None
    for user_key, user_data in config.items():
        if user_data["username"] == username_to_remove:
            user_key_to_remove = user_key
            break
    if user_key_to_remove:
        confirmation = input(f"{Fore.LIGHTMAGENTA_EX}Are you sure you want to remove user '{username_to_remove}'? (y/n): {Style.RESET_ALL}").strip().lower()
        if confirmation == 'y':
            config.pop(user_key_to_remove)
            with open(user_file_path, "w") as qos_user_file:
                json.dump(config, qos_user_file, indent=4)
            print(f"{Fore.LIGHTGREEN_EX}User {username_to_remove} removed successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}User removal canceled.{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}User not found.{Style.RESET_ALL}")

def change_password():
    user_file_path = pathlib.Path("data/config/users.json")
    if user_file_path.exists():
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
    else:
        print(f"{Fore.RED}File 'users.json' not found, please check the file path.{Style.RESET_ALL}")
        cmds.clear()
        return
    username_to_change = input(Fore.LIGHTRED_EX + "Enter the username to change password: " + Style.RESET_ALL)
    user_key_to_change = None
    for user_key, user_data in config.items():
        if user_data["username"] == username_to_change:
            user_key_to_change = user_key
            break
    if user_key_to_change:
        new_password = input(Fore.LIGHTRED_EX + "Enter a new password (leave empty for no password): " + Style.RESET_ALL)
        if new_password:
            en_password = base64.b64encode(new_password.encode('utf-8')).decode('utf-8')
        else:
            en_password = None
        confirm = input(Fore.LIGHTMAGENTA_EX + "Confirm password change? (y/n): " + Style.RESET_ALL).strip().lower()
        if confirm != 'y':
            print(f"{Fore.YELLOW}Password change canceled.{Style.RESET_ALL}")
            return
        config[user_key_to_change]["password"] = en_password if en_password else None
        with open(user_file_path, "w") as qos_user_file:
            json.dump(config, qos_user_file, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}Password for user {username_to_change} changed successfully.{Style.RESET_ALL}")
    else:
        print(Fore.RED + "User not found." + Style.RESET_ALL)