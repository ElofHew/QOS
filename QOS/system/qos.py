import os
import subprocess
import sys
import time
import json
import platform
import getpass
import colorama
from pathlib import Path

colorama.init(autoreset=True)

def qos_check_os():
    with open("config.json", "r") as qos_config_file:
        config = json.load(qos_config_file)
    if platform.system() == "Windows":
        config["os"] = "windows"
    elif platform.system() == "Linux":
        config["os"] = "linux"
    elif platform.system() == "Darwin":
        config["os"] = "macos"
    else:
        config["os"] = "unknown"
    with open("config.json", "w") as qos_config_file:
        json.dump(config, qos_config_file, indent=4)
    global os_type
    os_type = config["os"]

import json
import sys
import getpass

def print1(text, color=None, background=None):
    # 引用方法：必须字体色在前，背景色在后，文本保持最前
    if color and background:
        for words in text:
            print(color + background + words + colorama.Style.RESET_ALL, end="", flush=True)
            time.sleep(0.1)
    elif color:
        for words in text:
            print(color + words + colorama.Style.RESET_ALL, end="", flush=True)
            time.sleep(0.1)
    elif background:
        for words in text:
            print(background + words + colorama.Style.RESET_ALL, end="", flush=True)
            time.sleep(0.1)
    else:
        for words in text:
            print(words, end="", flush=True)
            time.sleep(0.1)
    print()

def qos_login():
    try:
        with open("users.json", "r") as qos_user_file:
            config = json.load(qos_user_file)
    except FileNotFoundError:
        print("File 'users.json' not found, please check the file path.")
        sys.exit(1)
    except json.JSONDecodeError:
        print("File 'users.json' is not a valid JSON file.")
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
                    print(f"{colorama.Fore.LIGHTGREEN_EX}Enter password: {colorama.Style.RESET_ALL}")
                    input_password = getpass.getpass(">>> ")
                    if input_password == password:
                        print1(" Welcome ", colorama.Fore.MAGENTA, colorama.Back.WHITE)
                        login_success = True
                        break
                    else:
                        print("Incorrect password, please try again.")
                        login_success = False
                        break
            if not user_found:
                print("User not found.")
            if login_success:
                break
        except KeyboardInterrupt:
            print("\nDetected KeyboardInterrupt. Exiting...")
            sys.exit(1)

def add_user():
    user_file_path = Path("users.json")
    if user_file_path.exists():
        with open(user_file_path, "r") as qos_user_file:
            config = json.load(qos_user_file)
    else:
        config = {}
    new_username = input("Enter a new username: ")
    new_password = input("Enter a new password (leave empty for no password): ")
    user_index = 1
    while f"user{user_index}" in config:
        user_index += 1
    new_user_key = f"user{user_index}"
    config[new_user_key] = {
        "username": new_username,
        "password": new_password if new_password else None
    }
    confirmation = input(f"Are you sure you want to add user '{new_username}'? (yes/no): ").strip().lower()
    if confirmation == 'yes':
        with open(user_file_path, "w") as qos_user_file:
            json.dump(config, qos_user_file, indent=4)
        print(f"User {new_username} added successfully.")
    else:
        print("User addition canceled.")

def qos_shell():
    while True:
        try:
            shell_command = input(f"{colorama.Back.LIGHTBLUE_EX}[QOS]{colorama.Back.WHITE}{colorama.Fore.BLACK} {time.strftime('%H:%M:%S')} {colorama.Style.RESET_ALL} > ")
            if shell_command == "help":
                print(f"{colorama.Fore.YELLOW}{colorama.Back.BLACK} QOS Help Menu {colorama.Style.RESET_ALL}")
                print("help - Show this help menu")
                print("version - Show the QOS version")
                print("time - Show the current time")
                print("adduser - Add a new user")
                print("whoami - Show the current user")
                print("pwd - Show the current working directory")
                print("clear - Clear the screen")
                print("ls - List the files and directories in the current directory")
                print("cd - Change the current directory")
                print("exit - Exit QOS")
            elif shell_command == "version":
                print(f"{colorama.Fore.MAGENTA}QOS version:{colorama.Style.RESET_ALL} {version}")
            elif shell_command == "time":
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
            elif shell_command == "adduser":
                add_user()
            elif shell_command == "whoami":
                print(getpass.getuser())
            elif shell_command == "pwd":
                print(os.getcwd())
            # Begin of os.system
            elif shell_command == "clear":
                if os_type == "windows":
                    os.system("cls")
                elif os_type == "linux" or os_type == "macos":
                    os.system("clear")
                else:
                    print("We can't know what OS you are using, so this operaton is not supported.")
            elif shell_command == "ls":
                if os_type == "windows":
                    subprocess.call("dir", shell=True)
                elif os_type == "linux" or os_type == "macos":
                    subprocess.call("ls", shell=True)
                else:
                    print("We can't know what OS you are using, so this operaton is not supported.")
            elif shell_command == "cd":
                print("This version of QOS won't support changing directory, because it will make something wrong with QOS.")
            # End of os.system
            elif shell_command == "exit":
                print("Are you sure you want to exit? (y/n)")
                while True:
                    try:
                        exit_cfm = input("> ").strip().lower()
                        if exit_cfm == "y":
                            sys.exit()
                        elif exit_cfm == "n":
                            break
                        else:
                            print("Invalid input. Please enter 'y' or 'n'.")
                    except KeyboardInterrupt:
                        print("\nKeyboardInterrupt detected. Exiting...")
                        sys.exit()
            elif shell_command == "":
                pass
            else:
                if unknown_cmd_sys_use:
                    subprocess.call(shell_command, shell=True)
                else:
                    print(f"{colorama.Fore.RED}Unknown command:{colorama.Style.RESET_ALL} {shell_command}")
        except KeyboardInterrupt:
            print("\nDo you want to exit? (y/n)")
            while True:
                try:
                    exit_cfm = input("> ").strip().lower()
                    if exit_cfm == "y":
                        sys.exit()
                    elif exit_cfm == "n":
                        break
                    else:
                        print("Invalid input. Please enter 'y' or 'n'.")
                except KeyboardInterrupt:
                    print("\nKeyboardInterrupt detected. Exiting...")
                    sys.exit()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit()

def main():
    qos_check_os()
    print("==============================")
    print("   Quarter Operation System   ")
    print("==============================")
    print(f" > Version: {version}")
    print("==============================")
    qos_login()

if __name__ == "__main__":
    with open("config.json", "r") as qos_config_file:
        config = json.load(qos_config_file)
        qos_father_os = config["os"]
        version = config["version"]
        # Additional Settings
        unknown_cmd_sys_use = config["unknown_cmd_sys_use"]
    main()
    qos_shell()

