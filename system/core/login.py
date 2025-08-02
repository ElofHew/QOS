# QOS Login Module
try:
    # Standard Library Modules
    import json
    import sys
    import base64
    from pathlib import Path
    # Third-Party Modules
    from colorama import init as cinit
    from colorama import Fore, Style
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(19)

cinit(autoreset=True)

qos_config_path = Path("data/config/config.json")
user_file_path = Path("data/config/users.json")

def confirm_username(name=None):
    try:
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
        def check_username(username):
            if username == "":
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a default user name.{Style.RESET_ALL}")
                return False
            elif len(username) > 10:
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot be longer than 10 characters.{Style.RESET_ALL}")
                return False
            elif any(char.isupper() for char in username):
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain uppercase letters.{Style.RESET_ALL}")
                return False
            elif " " in username:
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain spaces. You can use '_' instead.{Style.RESET_ALL}")
                return False
            elif any(char in "!@#$%^&*()[]{};:,./<>?\\|`~-=+" for char in username):
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot contain special characters. You can only use '_'.{Style.RESET_ALL}")
                return False
            elif username[0].isdigit():
                print(f"{Style.BRIGHT}{Fore.RED}User name cannot start with a number.{Style.RESET_ALL}")
                return False
            else:
                # Check if username already exists
                existing_usernames = {user_data["username"] for user_data in config.values()}
                if username in ["admin", "root", "guest", "superuser", "su", "exit"]:
                    print(f"{Style.BRIGHT}{Fore.RED}User name cannot be one of the reserved keywords.{Style.RESET_ALL}")
                    return False
                elif username in existing_usernames:
                    print(f"{Style.BRIGHT}{Fore.RED}User '{username}' already exists. Please choose another name.{Style.RESET_ALL}")
                    return False
                else:
                    return username
        if not name:
            while True:
                username = input(Fore.LIGHTMAGENTA_EX + "UserName" + Style.RESET_ALL + " : ").strip()
                cdt = check_username(username)
                if cdt is False:
                    continue
                else:
                    return cdt
        else:
            cdt = check_username(name)
            if cdt is False:
                return False
            return cdt
    except KeyboardInterrupt:
        print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
        return 10
    except FileNotFoundError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json not found.{Style.RESET_ALL}")
        return 1
    except json.JSONDecodeError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json is not valid JSON.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}.{Style.RESET_ALL}")
        return 1

def confirm_password(pword=None):
    try:
        def check_password(password):
            if password == "" or password is None or password.lower() == "none":
                print(f"{Fore.LIGHTGREEN_EX}No password? (y/n){Style.RESET_ALL}")
                response = input("> ").strip().lower()
                if response != "y":
                    password = input(Fore.LIGHTMAGENTA_EX + "Password" + Style.RESET_ALL + " : ").strip()
                    return check_password(password)
                else:
                    return None
            elif len(password) > 8:
                print(f"{Style.BRIGHT}{Fore.RED}Password cannot be longer than 8 characters.{Style.RESET_ALL}")
                return False
            elif " " in password:
                print(f"{Style.BRIGHT}{Fore.RED}Password cannot contain spaces.{Style.RESET_ALL}")
                return False
            else:
                return password
        if not pword:
            while True:
                password = input(Fore.LIGHTMAGENTA_EX + "Password" + Style.RESET_ALL + " : ").strip()
                cdt = check_password(password)
                if cdt is False:
                    continue
                else:
                    return cdt
        else:
            cdt = check_password(pword)
            if cdt is False:
                return False
            return cdt
    except KeyboardInterrupt:
        print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
        return 10
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}.{Style.RESET_ALL}")
        return 1

def confirm_user_account(username, password):
    try:
        # Read existing user data from file
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
    except FileNotFoundError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json not found.{Style.RESET_ALL}")
        return False
    except json.JSONDecodeError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json is not valid JSON.{Style.RESET_ALL}")
        return False
    except KeyboardInterrupt:
        print(f"{Fore.RED}Operation canceled.{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}.{Style.RESET_ALL}")
        return False

def add_user(username=None, password=None):
    if username and password:
        p_username = confirm_username(username)
        if p_username is False:
            return 1
        p_password = confirm_password(password)
        confirm_user_account(p_username, p_password)
    else:
        # Set new user name
        print(Fore.LIGHTGREEN_EX + "Enter a new username.\n" + Fore.LIGHTBLUE_EX + "(Enter a user name in 10 characters or less, and use only lowercase letters, numbers, and '_'.)" + Style.RESET_ALL)
        new_username = confirm_username()
        if new_username is False:
            return 1
        # Set new user password
        print(Fore.LIGHTGREEN_EX + "Enter a new password\n" + Fore.LIGHTBLUE_EX + "(Enter a password in 8 characters or less, and don't use spaces.)" + Style.RESET_ALL)
        new_password = confirm_password()
        # Write new user data to file
        confirm_user_account(new_username, new_password)

def make_system_name(sysname=None):
    try:
        def check_system_name(name):
            if name == "":
                print(f"{Style.BRIGHT}{Fore.RED}Please enter a system name.{Style.RESET_ALL}")
                return False
            elif len(name) > 20:
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot be longer than 20 characters.{Style.RESET_ALL}")
                return False
            elif " " in name:
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot contain spaces. You can use '_' instead.{Style.RESET_ALL}")
                return False
            elif any(char in "!@#$%^&*()[]{};:,./<>?\\|`~=+" for char in name):
                print(f"{Style.BRIGHT}{Fore.RED}System name cannot contain special characters. You can only use '_' and '-'.{Style.RESET_ALL}")
                return False
            else:
                # Check if system name already exists
                print(f"{Fore.LIGHTGREEN_EX}Your system name is '{name}'. Is this correct? (y/n){Style.RESET_ALL}")
                if not str(input("> ")).lower() == "y":
                    return False
                return name.strip()
        if not sysname:
            while True:
                system_name = input(Fore.LIGHTMAGENTA_EX + "System Name" + Style.RESET_ALL + " : ").strip()
                cdf = check_system_name(system_name)
                if cdf is False:
                    continue
                else:
                    system_name = cdf
                    break
        else:
            cdf = check_system_name(sysname)
            if cdf is False:
                return 1
            else:
                system_name = cdf
        with open(qos_config_path, "r") as qos_config_file:
            config = json.load(qos_config_file)
        config["system_name"] = system_name
        with open(qos_config_path, "w") as qos_config_file:
            json.dump(config, qos_config_file, indent=4)
        print(f"{Fore.LIGHTGREEN_EX}System name changed successfully.{Style.RESET_ALL}")
        return system_name
    except KeyboardInterrupt:
        print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
        return 10
    except FileNotFoundError:
        print(f"{Style.BRIGHT}{Fore.RED}config.json not found.{Style.RESET_ALL}")
        return 1
    except json.JSONDecodeError:
        print(f"{Style.BRIGHT}{Fore.RED}config.json is not valid JSON.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        return 1


def remove_user(username):
    try:
        username_to_remove = username.strip()
        if username_to_remove in ["admin", "root", "guest", "superuser", "su"]:
            print(f"{Fore.RED}User '{username_to_remove}' cannot be removed.{Style.RESET_ALL}")
            return 1
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
        user_key_to_remove = None
        for user_key, user_data in config.items():
            if user_data["username"] == username_to_remove:
                user_key_to_remove = user_key
                break
        if user_key_to_remove:
            confirmation = input(f"{Fore.LIGHTMAGENTA_EX}Are you sure you want to remove user '{username_to_remove}'? (y/n): {Style.RESET_ALL}").strip().lower()
            if confirmation == 'y':
                if config[user_key_to_remove]["password"]:
                    compare_password = input(f"{Fore.LIGHTMAGENTA_EX}Please enter the password for user '{username_to_remove}': {Style.RESET_ALL}").strip()
                    if base64.b64encode(compare_password.encode('utf-8')).decode('utf-8') != config[user_key_to_remove]["password"]:
                        print(f"{Fore.RED}Incorrect password. User removal canceled.{Style.RESET_ALL}")
                        return 1
                config.pop(user_key_to_remove)
                with open(user_file_path, "w") as qos_user_file:
                    json.dump(config, qos_user_file, indent=4)
                print(f"{Fore.LIGHTGREEN_EX}User {username_to_remove} removed successfully.{Style.RESET_ALL}")
                return 0
            else:
                print(f"{Fore.YELLOW}User removal canceled.{Style.RESET_ALL}")
                return 0
        else:
            print(f"{Fore.RED}User not found.{Style.RESET_ALL}")
            return 1
    except KeyboardInterrupt:
        print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
        return 10
    except FileNotFoundError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json not found.{Style.RESET_ALL}")
        return 1
    except json.JSONDecodeError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json is not valid JSON.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        return 1

def change_password(username, password):
    try:
        username_to_change = username
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
        user_key_to_change = None
        for user_key, user_data in config.items():
            if user_data["username"] == username_to_change:
                user_key_to_change = user_key
                break
        if user_key_to_change:
            new_password = password
            if new_password == "none":
                en_password = None
            else:
                en_password = base64.b64encode(new_password.encode('utf-8')).decode('utf-8')
            confirm = input(Fore.LIGHTMAGENTA_EX + "Confirm password change? (y/n): " + Style.RESET_ALL).strip().lower()
            if not confirm == 'y':
                print(f"{Fore.YELLOW}Password change canceled.{Style.RESET_ALL}")
                return 0
            # Confirm old password
            if config[user_key_to_change]["password"]:
                old_pw = input(Fore.LIGHTMAGENTA_EX + "Enter old password: " + Style.RESET_ALL).strip()
                if base64.b64encode(old_pw.encode('utf-8')).decode('utf-8') != config[user_key_to_change]["password"]:
                    print(f"{Fore.RED}Incorrect password. Password change canceled.{Style.RESET_ALL}")
                    return 1
            # Write into config file
            config[user_key_to_change]["password"] = en_password if en_password else None
            with open(user_file_path, "w") as qos_user_file:
                json.dump(config, qos_user_file, indent=4)
            print(f"{Fore.LIGHTGREEN_EX}Password for user {username_to_change} changed successfully.{Style.RESET_ALL}")
            return 0
        else:
            print(Fore.RED + "User not found." + Style.RESET_ALL)
            return 1
    except KeyboardInterrupt:
        print(f"{Fore.RED}(KeyboardInterrupt Exit){Style.RESET_ALL}")
        return 10
    except FileNotFoundError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json not found.{Style.RESET_ALL}")
        return 1
    except json.JSONDecodeError:
        print(f"{Style.BRIGHT}{Fore.RED}users.json is not valid JSON.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Style.BRIGHT}{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")
        return 1