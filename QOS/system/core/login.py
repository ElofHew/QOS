# QOS Login Module
try:
    # Standard Library Modules
    import json
    import sys
    import base64
    import pathlib
    import getpass
    # Third-Party Modules
    import colorama
    # Core Modules
    import system.core.options as options
    import system.core.cmds as cmds
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

colorama.init(autoreset=True)

def confirm_username():
    while True:
        try:
            username = input(colorama.Fore.LIGHTMAGENTA_EX + "UserName" + colorama.Style.RESET_ALL + " : ")
            if username == "":
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Please enter a default user name.{colorama.Style.RESET_ALL}")
                continue
            elif len(username) > 10:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}User name cannot be longer than 10 characters.{colorama.Style.RESET_ALL}")
                continue
            elif any(char.isupper() for char in username):
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}User name cannot contain uppercase letters.{colorama.Style.RESET_ALL}")
                continue
            elif " " in username:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}User name cannot contain spaces. You can use '_' instead.{colorama.Style.RESET_ALL}")
                continue
            elif any(char in "!@#$%^&*()[]{};:,./<>?\|`~-=+" for char in username):
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}User name cannot contain special characters. You can only use '_'.{colorama.Style.RESET_ALL}")
                continue
            elif username[0].isdigit():
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}User name cannot start with a number.{colorama.Style.RESET_ALL}")
                continue
            else:
                return username
        except KeyboardInterrupt:
            print(f"{colorama.Fore.RED}(KeyboardInterrupt Exit){colorama.Style.RESET_ALL}")
            return None

def confirm_password():
    while True:
        try:
            password = getpass.getpass(colorama.Fore.LIGHTMAGENTA_EX + "Password" + colorama.Style.RESET_ALL + " : ")
            if password == "":
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.LIGHTGREEN_EX}No password? (y/n){colorama.Style.RESET_ALL}")
                if str(input("> ")).lower() == "y":
                    password = None
                    return password
                else:
                    continue
            elif len(password) > 8:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Password cannot be longer than 8 characters.{colorama.Style.RESET_ALL}")
                continue
            elif " " in password:
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.RED}Password cannot contain spaces.{colorama.Style.RESET_ALL}")
                continue
            else:
                return password
        except KeyboardInterrupt:
            print(f"{colorama.Fore.RED}(KeyboardInterrupt Exit){colorama.Style.RESET_ALL}")
            return None

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
        en_password = base64.b64encode(password.encode('utf-8')).decode('utf-8')
        config[new_user_key] = {
            "username": username,
            "password": en_password if en_password else None
        }
        confirmation = input(f"{colorama.Fore.LIGHTCYAN_EX}Are you sure you want to add user '{username}'? (y/n): {colorama.Style.RESET_ALL}").strip().lower()
        if confirmation.lower() == 'y':
            with open(user_file_path, "w") as qos_user_file:
                json.dump(config, qos_user_file, indent=4)
            print(f"{colorama.Fore.LIGHTGREEN_EX}User {username} added successfully.{colorama.Style.RESET_ALL}")
            return True
        else:
            print(f"{colorama.Fore.YELLOW}User addition canceled.{colorama.Style.RESET_ALL}")
            return False
    except KeyboardInterrupt:
        print(f"{colorama.Fore.RED}Operation canceled.{colorama.Style.RESET_ALL}")
        return False

def qos_login():
    try:
        with open("data/config/users.json", "r") as qos_user_file:
            config = json.load(qos_user_file)
    except FileNotFoundError:
        print(colorama.Fore.RED + "File 'users.json' not found, please check the file path." + colorama.Style.RESET_ALL)
        cmds.clear()
        sys.exit(1)
    except json.JSONDecodeError:
        print(colorama.Fore.RED + "File 'users.json' is not a valid JSON file." + colorama.Style.RESET_ALL)
        cmds.clear()
        sys.exit(1)
    while True:
        try:
            print(f"{colorama.Fore.LIGHTGREEN_EX}Enter a user name to login: {colorama.Style.RESET_ALL}")
            username = input(">>> ")
            user_found = False
            login_success = False
            for user_data in config.values():
                if user_data["username"] == username:
                    user_found = True
                    password = user_data.get("password", "")
                    if not password:
                        login_success = True
                        break
                    else:
                        de_password = base64.b64decode(password).decode('utf-8')
                        while True:
                            try:
                                print(f"{colorama.Fore.LIGHTGREEN_EX}Enter password: {colorama.Style.RESET_ALL}")
                                input_password = getpass.getpass(">>> ")
                                if input_password == de_password:
                                    login_success = True
                                    break
                                else:
                                    print(colorama.Fore.RED + "Incorrect password, please try again." + colorama.Style.RESET_ALL)
                                    login_success = False
                                    continue
                            except KeyboardInterrupt:
                                print(f"{colorama.Style.DIM}{colorama.Fore.GREEN}(Change User Account){colorama.Style.RESET_ALL}")
                                break
                    break
            if not user_found:
                print(f"{colorama.Fore.RED}User not found.{colorama.Style.RESET_ALL}")
            if login_success:
                print()
                options.jump_print(" Welcome to QOS ", colorama.Fore.MAGENTA, colorama.Style.BRIGHT)
                print()
                return username
        except KeyboardInterrupt:
            print(f"{colorama.Fore.DIM}{colorama.Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{colorama.Style.RESET_ALL}")
            cmds.clear()
            sys.exit(1)

def add_user():
    # Set new user name
    print(colorama.Fore.LIGHTGREEN_EX + "Enter a new username.\n" + colorama.Fore.LIGHTBLUE_EX + "(Enter a user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.)" + colorama.Style.RESET_ALL)
    new_username = confirm_username()
    # Set new user password
    print(colorama.Fore.LIGHTGREEN_EX + "Enter a new password\n" + colorama.Fore.LIGHTBLUE_EX + "(Enter a password in 8 characters or less, and don't use spaces.)" + colorama.Style.RESET_ALL)
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
    username_to_remove = input(f"{colorama.Fore.LIGHTRED_EX}Enter the username to remove: {colorama.Style.RESET_ALL}")
    user_key_to_remove = None
    for user_key, user_data in config.items():
        if user_data["username"] == username_to_remove:
            user_key_to_remove = user_key
            break
    if user_key_to_remove:
        confirmation = input(f"{colorama.Fore.LIGHTMAGENTA_EX}Are you sure you want to remove user '{username_to_remove}'? (y/n): {colorama.Style.RESET_ALL}").strip().lower()
        if confirmation == 'y':
            config.pop(user_key_to_remove)
            with open(user_file_path, "w") as qos_user_file:
                json.dump(config, qos_user_file, indent=4)
            print(f"{colorama.Fore.LIGHTGREEN_EX}User {username_to_remove} removed successfully.{colorama.Style.RESET_ALL}")
        else:
            print(f"{colorama.Fore.YELLOW}User removal canceled.{colorama.Style.RESET_ALL}")
    else:
        print(f"{colorama.Fore.RED}User not found.{colorama.Style.RESET_ALL}")

def change_password():
    user_file_path = pathlib.Path("data/config/users.json")
    if user_file_path.exists():
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
    else:
        print(f"{colorama.Fore.RED}File 'users.json' not found, please check the file path.{colorama.Style.RESET_ALL}")
        cmds.clear()
        return
    username_to_change = input(colorama.Fore.LIGHTRED_EX + "Enter the username to change password: " + colorama.Style.RESET_ALL)
    user_key_to_change = None
    for user_key, user_data in config.items():
        if user_data["username"] == username_to_change:
            user_key_to_change = user_key
            break
    if user_key_to_change:
        new_password = input(colorama.Fore.LIGHTRED_EX + "Enter a new password (leave empty for no password): " + colorama.Style.RESET_ALL)
        if new_password:
            en_password = base64.b64encode(new_password.encode('utf-8')).decode('utf-8')
        else:
            en_password = None
        confirm = input(colorama.Fore.LIGHTMAGENTA_EX + "Confirm password change? (y/n): " + colorama.Style.RESET_ALL).strip().lower()
        if confirm != 'y':
            print(f"{colorama.Fore.YELLOW}Password change canceled.{colorama.Style.RESET_ALL}")
            return
        config[user_key_to_change]["password"] = en_password if en_password else None
        with open(user_file_path, "w") as qos_user_file:
            json.dump(config, qos_user_file, indent=4)
        print(f"{colorama.Fore.LIGHTGREEN_EX}Password for user {username_to_change} changed successfully.{colorama.Style.RESET_ALL}")
    else:
        print(colorama.Fore.RED + "User not found." + colorama.Style.RESET_ALL)