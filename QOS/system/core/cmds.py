import os
import re
import sys
import json
import time as tm
import pathlib
import platform
import requests
from colorama import init as cinit
from colorama import Fore, Style
import shutil
import subprocess

import system.core.options as options

cinit(autoreset=True)

# Open config files
with open('data/config/config.json', 'r') as config_file:
    config = json.load(config_file)
    qos_version = config["version"]
    os_type = config["os_type"]
    qos_path = config["qos_path"]
    home_path = config["home_path"]
    data_path = config["data_path"]
    last_login = config["last_login"]

# Tips to use Args
def args_tips(command):
    if command == "cat":
        print(f"{Fore.YELLOW}Usage: cat <file_path>{Style.RESET_ALL}")
    elif command == "echo":
        print(f"{Fore.YELLOW}Usage: echo <text>{Style.RESET_ALL}")
    elif command == "cp":
        print(f"{Fore.YELLOW}Usage: cp <source_path> <destination_path>{Style.RESET_ALL}")
    elif command == "mv":
        print(f"{Fore.YELLOW}Usage: mv <source_path> <destination_path>{Style.RESET_ALL}")
    elif command == "ls":
        print(f"{Fore.YELLOW}Usage: ls <directory_path>{Style.RESET_ALL}")
    elif command == "cd":
        print(f"{Fore.YELLOW}Usage: cd <directory_path>{Style.RESET_ALL}")
    elif command == "touch":
        print(f"{Fore.YELLOW}Usage: touch <file_path>{Style.RESET_ALL}")
    elif command == "edit":
        print(f"{Fore.YELLOW}Usage: edit <file_path>{Style.RESET_ALL}")
    elif command == "mkdir":
        print(f"{Fore.YELLOW}Usage: mkdir <directory_path>{Style.RESET_ALL}")
    elif command == "rm":
        print(f"{Fore.YELLOW}Usage: rm <file_path>{Style.RESET_ALL}")
    elif command == "rename":
        print(f"{Fore.YELLOW}Usage: rename <old_name> <new_name>{Style.RESET_ALL}")
    elif command == "activate":
        print(f"{Fore.YELLOW}Usage: activate <activate_code>{Style.RESET_ALL}")
    elif command == "ping":
        print(f"{Fore.YELLOW}Usage: ping <host>{Style.RESET_ALL}")
    elif command == "down":
        print(f"{Fore.YELLOW}Usage: down <url>{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Unknown command '{command}'.{Style.RESET_ALL}")

# Check Args from user input
def check_args(command, args):
    if command in ("cat", "echo", "ls", "cd", "touch", "edit", "mkdir", "rm", "activate", "ping", "down"):
        if len(args) == 1:
            return True
        else:
            return False
    elif command in ("cp", "mv", "rename"):
        if len(args) == 2:
            return True
        else:
            return False
    else:
        return False

# Need Args
def cat(work_dir, file_path):
    try:
        if not os.path.exists(os.path.join(work_dir, file_path)):
            print(f"{Fore.RED}Error: File '{file_path}' does not exist.{Style.RESET_ALL}")
            return
        with open(os.path.join(work_dir, file_path), "r", encoding="utf-8") as f:
            print(f.read())
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to read file. {e}{Style.RESET_ALL}")
        return
    except UnicodeDecodeError:
        print(f"{Fore.RED}Error: File '{file_path}' is not a text file or is encoded in an unsupported format.{Style.RESET_ALL}")
        return
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File '{file_path}' not found.{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return

def echo(work_dir, text):
    print(text)

def cp(work_dir, src, dst):
    if not os.path.exists(os.path.join(work_dir, src)):
        print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
        return
    if os.path.exists(os.path.join(work_dir, dst)):
        print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
    try:
        shutil.copy(os.path.join(work_dir, src), os.path.join(work_dir, dst))
        print(f"{Fore.GREEN}File copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to copy file. {e}{Style.RESET_ALL}")

def mv(work_dir, src, dst):
    if not os.path.exists(os.path.join(work_dir, src)):
        print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
        return
    if os.path.exists(os.path.join(work_dir, dst)):
        print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
    try:
        shutil.move(os.path.join(work_dir, src), os.path.join(work_dir, dst))
        print(f"{Fore.GREEN}File moved successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to move file. {e}{Style.RESET_ALL}")

def ls(work_dir, list_path):
    if list_path == ".":
        list_dir = work_dir
    else:
        try:
            list_dir = os.path.join(work_dir, list_path)
        except OSError:
            print(f"{Fore.RED}Error: Invalid path '{list_path}'.{Style.RESET_ALL}")
            return
    try:
        if not os.path.exists(list_dir):
            print(f"{Fore.RED}Error: Path '{list_path}' does not exist.{Style.RESET_ALL}")
            return
        elif os.listdir(list_dir) == []:
            print(f"{Fore.YELLOW}(This is an empty directory.){Style.RESET_ALL}")
        else:
            for file in os.listdir(list_dir):
                if os.path.isfile(os.path.join(list_dir, file)):
                    print(f"{Fore.LIGHTGREEN_EX}{file}{Style.RESET_ALL}")
                elif os.path.isdir(os.path.join(list_dir, file)):
                    print(f"{Fore.LIGHTBLUE_EX}{file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{file}{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to list directory. {e}{Style.RESET_ALL}")

def cd(work_dir, change_dir):
    try:
        # 处理当前目录
        if change_dir in (".", '"."'):
            return work_dir
        elif change_dir == "~":
            with open("data/config/config.json", "r", encoding="utf-8") as config_file:
                config = json.load(config_file)
                last_login = config.get("last_login", "")
            user_dir = os.path.join(home_path, last_login)
            if os.path.exists(user_dir):
                return os.path.abspath(user_dir)
            else:
                print(f"{Fore.RED}Error: Home directory for user '{last_login}' not found.{Style.RESET_ALL}")
                return work_dir
        else:
            # 处理驱动器根目录
            if len(change_dir) == 2 and change_dir[1] == ':':
                drive = change_dir.upper() + '\\'
                if os.path.exists(drive):
                    return drive
                else:
                    print(f"{Fore.RED}Error: Drive '{drive}' not found.{Style.RESET_ALL}")
                    return work_dir
            
            # 处理相对路径
            new_path = os.path.join(work_dir, change_dir)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                # 处理绝对路径
                new_path = os.path.abspath(change_dir)
                if os.path.exists(new_path):
                    return new_path
                else:
                    print(f"{Fore.RED}Error: Path '{change_dir}' not found.{Style.RESET_ALL}")
                    return work_dir
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Configuration file 'data/config/config.json' not found.{Style.RESET_ALL}")
        return work_dir
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to change directory. {e}{Style.RESET_ALL}")
        return work_dir
    except json.JSONDecodeError as e:
        print(f"{Fore.RED}Error: Failed to decode configuration file. {e}{Style.RESET_ALL}")
        return work_dir
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return work_dir

def touch(work_dir, file_path):
    try:
        if os.path.exists(os.path.join(work_dir, file_path)):
            print(f"{Fore.YELLOW}Warning: File '{file_path}' already exists.{Style.RESET_ALL}")
        else:
            with open(os.path.join(work_dir, file_path), "w") as f:
                f.write("")
            print(f"{Fore.GREEN}File '{file_path}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create file. {e}{Style.RESET_ALL}")

def edit(work_dir, file_path):
    try:
        if not os.path.exists(os.path.join(work_dir, file_path)):
            print(f"{Fore.RED}Error: File '{file_path}' does not exist.{Style.RESET_ALL}")
            return
        else:
            if not file_path.endswith(".txt"):
                print(f"{Fore.YELLOW}Warning: This file is not a text file. Please make sure you can read and write it directly.{Style.RESET_ALL}")
            if os_type == "windows":
                os.startfile(os.path.join(work_dir, file_path))
            elif os_type == "linux" or os_type == "macos":
                subprocess.call(["xdg-open", os.path.join(work_dir, file_path)])
            else:
                print(f"{Fore.RED}Error: Unsupported OS.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to open file. {e}{Style.RESET_ALL}")

def mkdir(work_dir, new_dir):
    try:
        if os.path.exists(os.path.join(work_dir, new_dir)):
            print(f"{Fore.YELLOW}Warning: Path '{work_dir}' already exists.{Style.RESET_ALL}")
        else:
            os.makedirs(os.path.join(work_dir, new_dir))
            print(f"{Fore.GREEN}Directory '{new_dir}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create directory. {e}{Style.RESET_ALL}")

def rename(work_dir, src, dst):
    try:
        if not os.path.exists(os.path.join(work_dir, src)):
            print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
            return
        if os.path.exists(os.path.join(work_dir, dst)):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
        os.rename(os.path.join(work_dir, src), os.path.join(work_dir, dst))
        print(f"{Fore.GREEN}File renamed successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to rename file. {e}{Style.RESET_ALL}")

def rm(work_dir, rm_path):
    try:
        if not os.path.exists(os.path.join(work_dir, rm_path)):
            print(f"{Fore.RED}Error: Path '{rm_path}' does not exist.{Style.RESET_ALL}")
            return
        if os.path.isfile(os.path.join(work_dir, rm_path)):
            os.remove(os.path.join(work_dir, rm_path))
            print(f"{Fore.GREEN}File '{rm_path}' removed successfully.{Style.RESET_ALL}")
        elif os.path.isdir(os.path.join(work_dir, rm_path)):
            shutil.rmtree(os.path.join(work_dir, rm_path))
            print(f"{Fore.GREEN}Directory '{rm_path}' removed successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to remove file or directory. {e}{Style.RESET_ALL}")

def activate(work_dir, code):
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
    activate_code = config["activate_code"]
    qos_edition = config["qos_edition"]
    activate_statue = config["activate_statue"]
    if code == "check":
        if activate_statue:
            print(f"{Fore.GREEN}Quarter OS is activated.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Your Quarter OS edition is {Fore.LIGHTGREEN_EX}{qos_edition} Edition{Fore.CYAN} and your activate code is {Fore.LIGHTGREEN_EX}{activate_code}{Fore.CYAN}.{Style.RESET_ALL}")
            return True
        else:
            print(f"{Fore.RED}Quarter OS is not activated.{Style.RESET_ALL}")
            print(f"{Fore.CYAN}Please activate Quarter OS by {Fore.LIGHTGREEN_EX}activate <activate_code>{Fore.CYAN}.\nYou can get the activate code from the Quarter OS website: https://os.drevan.xyz/qos/activate. {Style.RESET_ALL}")
            return False
    if code == "deactivate":
        with open("data/config/config.json", "r") as config_file:
            config = json.load(config_file)
        config["activate_code"] = ""
        config["qos_edition"] = ""
        config["activate_statue"] = False
        with open("data/config/config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        print(f"{Fore.GREEN}Quarter OS deactivated successfully.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Please restart Quarter OS to take effect.{Style.RESET_ALL}")
        return True
    if activate_statue:
        while True:
            try:
                print(f"{Fore.YELLOW}WARNING: You have already activated Quarter OS. Are you sure to activate again? (y/n){Fore.RESET}")
                cfm = input("> ").strip().lower()
                if cfm == "y":
                    break
                elif cfm == "n":
                    return 0
                else:
                    print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
            except KeyboardInterrupt:
                print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
                sys.exit(0)
    try:
        if not len(code) == 5:
            raise ValueError
        if not re.match(r'^[SHPUL]\d{4}', code):
            raise ValueError
        if not 1000 <= int(code[1:]) <= 9999:
            raise ValueError
    except ValueError:
        print(f"{Fore.RED}Error: Invalid activate code. Please enter a valid code.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTCYAN_EX}You can get the activate code from the Quarter OS website: https://os.drevan.xyz/qos/activate. {Style.RESET_ALL}")
        return 1
    if code.startswith("S"):
        qos_act_type = "Starter"
    elif code.startswith("H"):
        qos_act_type = "Home"
    elif code.startswith("P"):
        qos_act_type = "Professional"
    elif code.startswith("U"):
        qos_act_type = "Ultimate"
    elif code.startswith("L"):
        qos_act_type = "LongTermSupport"
    else:
        qos_act_type = "Unknown"
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
    config_file.close()
    print(f"{Fore.GREEN}Quarter OS activated successfully.{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Your Quarter OS edition is {Fore.LIGHTGREEN_EX}{qos_edition} Edition{Fore.CYAN} and your activate code is {Fore.LIGHTGREEN_EX}{activate_code}{Fore.CYAN}.{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}You best restart Quarter OS to take effect. (Except for OOBE){Style.RESET_ALL}")
    return True

def ping(working_dir, host):
    try:
        if os_type == "windows":
            ping_result = subprocess.run(["ping", "-n", "4", host])
        elif os_type == "linux":
            ping_result = subprocess.run(["ping", "-c", "4", host])
        if ping_result.returncode == 0:
            print(f"{Fore.GREEN}Ping to {host} successful.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Ping to {host} failed.{Style.RESET_ALL}")
            print(f"{Fore.RED}Error message: {ping_result.stderr}{Style.RESET_ALL}")
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run ping command. {e}{Style.RESET_ALL}")
        return
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Ping command not found. Please check your system configuration.{Style.RESET_ALL}")
        return

def down(working_dir, url):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            file_name = url.split("/")[-1]
            down_path = os.path.join(home_path, last_login, "downloads")
            file_path = os.path.join(down_path, file_name)
            if not os.path.exists(down_path):
                os.makedirs(down_path)
            if os.path.exists(file_path):
                print(f"{Fore.YELLOW}Warning: File '{file_name}' already exists in '{down_path}'. It will be overwritten.{Style.RESET_ALL}")
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"{Fore.LIGHTGREEN_EX}Download file successfully.{Fore.RESET}")
            print(f"{Fore.CYAN}Path: {file_path}{Fore.RESET}")
        else:
            print(f"{Fore.RED}Download file failed. Code: {response.status_code}{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}Download file failed. Error: {e}{Fore.RESET}")

# No Args
def pwd(work_dir):
    print(pathlib.Path(work_dir))

def cwd():
    print(os.getcwd())

def help():
    try:
        with open(os.path.join(qos_path, "system", "shell", "cmds.json"), "r") as cmds_file:
            cmds_list = json.load(cmds_file)
            noargs_list = cmds_list["NoArgs"]
            needargs_list = cmds_list["NeedArgs"]
            pm_cmds_list = cmds_list["PackageManager"]
            szk_cmds_list = cmds_list["ShizukuCompat"]
            sysapp_list = cmds_list["SystemApps"]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Failed to load commands list.{Style.RESET_ALL}")
        return
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Failed to parse commands list.{Style.RESET_ALL}")
        return
    print(f"{Fore.YELLOW}% Quarter OS - Help Menu %{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=========================={Style.RESET_ALL}")
    print(f"{Fore.GREEN}settings{Style.RESET_ALL}: Quarter OS Settings App")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in noargs_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in needargs_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in pm_cmds_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in szk_cmds_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in sysapp_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    print(f"{Fore.BLUE}For Third-party Apps, please enter 'biscuit list'.{Style.RESET_ALL}")
    with open(os.path.join(data_path, "config", "shell.json"), "r") as apps_file:
        apps_config = json.load(apps_file)
        ucp = apps_config["unknown_command_progression"]
    if ucp:
        print(f"{Fore.LIGHTGREEN_EX}Tips: Unknown command progression is enabled. Unknown commands will be executed as system commands.{Style.RESET_ALL}")
    else:
        print(f"{Fore.LIGHTGREEN_EX}Tips: Unknown command progression is disabled. Unknown commands will not be executed.{Style.RESET_ALL}")

def about():
    print(f"{Fore.LIGHTBLUE_EX}% Quarter OS - About %{Style.RESET_ALL}")
    options.cat("system/etc/about.txt")

def version():
    print(f"{Fore.GREEN}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")

def whoami(username):
    print(f"{Fore.GREEN}Current user: {Fore.CYAN}{username}{Style.RESET_ALL}")

def time():
    print(f"{Fore.GREEN}Current time: {Fore.CYAN}{tm.strftime('%H:%M:%S', tm.localtime())}{Style.RESET_ALL}")

def date():
    print(f"{Fore.GREEN}Current date: {Fore.CYAN}{tm.strftime('%Y-%m-%d', tm.localtime())}{Style.RESET_ALL}")

def sysinfo():
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        last_login = config["last_login"]
        activate_statue = config["activate_statue"]
        qos_edition = config["qos_edition"]
    print(f"{Fore.BLUE}& Quarter OS System Info &{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Operating System: {Fore.CYAN}{platform.system()} {platform.release()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Python Version: {Fore.CYAN}{platform.python_version()}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Activate Condition: {Fore.CYAN}{str(activate_statue)}{Style.RESET_ALL}")
    if activate_statue:
        print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Edition: {Fore.CYAN}{qos_edition}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Current User: {Fore.CYAN}{last_login}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}QOS Path: {Fore.CYAN}{qos_path}{Style.RESET_ALL}")

def clear():
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        os_type = config["os_type"]
    if os_type == "windows":
        os.system("cls")
    elif os_type == "linux":
        os.system("clear")
    else:
        print(f"{Fore.RED}Error: Unsupported OS.{Style.RESET_ALL}")

def exit():
    print(f"{Fore.CYAN}Are you sure you want to exit? (y/n){Style.RESET_ALL}")
    while True:
        try:
            exit_cfm = input("> ").strip().lower()
            if exit_cfm == "y":
                clear()
                return True
            elif exit_cfm == "n":
                return False
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            clear()
            sys.exit(0)

def reboot():
    print(f"{Fore.CYAN}Are you sure you want to reboot? (y/n){Style.RESET_ALL}")
    while True:
        try:
            reboot_cfm = input("> ").strip().lower()
            if reboot_cfm == "y":
                clear()
                return True
            elif reboot_cfm == "n":
                return False
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            clear()
            sys.exit(0)

# PackageManager
def pm_tips():
    print(f"{Fore.LIGHTGREEN_EX}% Biscuit Package Manager %{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}==========================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}install <path> - Install a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}remove <pkg>   - Remove a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}list           - List all installed packages{Style.RESET_ALL}")
    print(f"{Fore.CYAN}search <query> - Search a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}get <pkg> (V)  - Get package from online repository{Style.RESET_ALL}")
    print(f"{Fore.CYAN}mirror <url>   - Set a mirror for package repository{Style.RESET_ALL}")

def pm_check_args(args, working_path):
    import system.core.biscuit as biscuit
    if args[0] == "list":
        biscuit.list()
        return 0
    if args[0] == "install":
        if len(args) == 2:
            biscuit.install(working_path, args[1])
            return 0
    if args[0] == "remove":
        if len(args) == 2:
            biscuit.remove(args[1])
            return 0
    if args[0] == "search":
        if len(args) == 2:
            biscuit.search(args[1])
            return 0
    if args[0] == "get":
        if len(args) == 2:
            biscuit.get(args[1], None)
            return 0
        if len(args) == 3:
            biscuit.get(args[1], args[2])
            return 0
    if args[0] == "mirror":
        if len(args) == 2:
            biscuit.mirror(args[1])
            return 0
    pm_tips()
    del biscuit

# Run more commands

def ucprogress(shell_command, working_path):
    with open(os.path.join(data_path, "config", "shell.json"), "r") as apps_file:
        apps_config = json.load(apps_file)
        ucp = apps_config["unknown_command_progression"]
    try:
        if ucp:
            os.chdir(working_path)
            process = subprocess.Popen(shell_command, shell=True)
        else:
            print(f"{Fore.RED}Unknown command:{Style.RESET_ALL} {shell_command}")
            return
        process.wait()
        process.kill()
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run command '{shell_command}'. {e}{Style.RESET_ALL}")
        return False
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run command '{shell_command}'. {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return False
    finally:
        os.chdir(qos_path)

def run_3rd_party_apps(shell_command, working_path):
    try:
        if os.path.isfile(os.path.join("data", "shell", "apps.json")):
            with open(os.path.join("data", "shell", "apps.json"), "r") as apps_file:
                apps_list = json.load(apps_file)
            if shell_command in apps_list:
                app_path = apps_list[shell_command]["path"]
            else:
                ucprogress(shell_command, working_path)
                return
        else:
            ucprogress(shell_command, working_path)
            return
        third_party_script_path = os.path.join(qos_path, "data", "apps", shell_command, "main.py")
        if third_party_script_path == os.path.join(app_path, "main.py"):
            if os.path.isfile(third_party_script_path):
                os.chdir(os.path.join(qos_path, "data", "apps", shell_command))
                if os_type == "windows":
                    process = subprocess.Popen(["python", third_party_script_path])
                else:
                    process = subprocess.Popen(["python3", third_party_script_path])
                process.wait()
                process.kill()
                os.chdir(qos_path)
            else:
                ucprogress(shell_command, working_path)
        else:
            ucprogress(shell_command, working_path)
            return
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return False
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return False
    finally:
        os.chdir(qos_path)

def run_sys_apps(shell_command, working_path):
    try:
        system_app_path = os.path.join(qos_path, "system", "apps", shell_command + ".py")
        if os.path.isfile(system_app_path):
            if os_type == "windows":
                process = subprocess.Popen(["python", system_app_path])
            else:
                process = subprocess.Popen(["python3", system_app_path])
            process.wait()
            process.kill()
        else:
            run_3rd_party_apps(shell_command, working_path)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return False
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return False
    finally:
        os.chdir(qos_path)

def run_local_prog(working_path, current_script_path):
    try:
        os.chdir(working_path)
        if os_type == "windows":
            process = subprocess.Popen(["python", current_script_path])
        else:
            process = subprocess.Popen(["python3", current_script_path])
        process.wait()
        process.kill()
        os.chdir(qos_path)
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {current_script_path}. {e}{Style.RESET_ALL}")
        return False
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {current_script_path}. {e}{Style.RESET_ALL}")
        return False
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return False
    finally:
        os.chdir(qos_path)
