import os
import sys
import json
import time as tm
import datetime as dt
import pathlib
import platform
from colorama import init as cinit
from colorama import Fore, Style, Back
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
with open('data/config/shell.json', 'r') as shell_file:
    shell_config = json.load(shell_file)
    ucp = shell_config["unknown_command_progression"]

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
    elif command == "rmdir":
        print(f"{Fore.YELLOW}Usage: rmdir <directory_path>{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}Error: Unknown command '{command}'.{Style.RESET_ALL}")

# Check Args from user input
def check_args(command, args):
    if command in ("cat", "echo", "ls", "cd", "touch", "edit", "mkdir", "rm"):
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
        with open(os.path.join(work_dir, file_path), "r") as f:
            print(f.read())
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to read file. {e}{Style.RESET_ALL}")

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
                    print(f"{Fore.GREEN}{file}{Style.RESET_ALL}")
                elif os.path.isdir(os.path.join(list_dir, file)):
                    print(f"{Fore.BLUE}{file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{file}{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to list directory. {e}{Style.RESET_ALL}")

def cd(work_dir, change_dir):
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        os_type = config["os_type"]
    if os_type == "windows":
        # 检查 change_dir 是否以盘符开头
        if change_dir.startswith(tuple(f"{chr(x)}:\\" for x in range(67, 91))):
            if os.path.exists(change_dir):
                return os.path.abspath(change_dir)
            else:
                print(f"{Fore.RED}Error: Path '{change_dir}' not found.{Style.RESET_ALL}")
                return work_dir
        # 处理当前目录
        elif change_dir in (".", '"."'):
            return work_dir
        # 展开环境变量
        elif change_dir.startswith("%") or change_dir.startswith('"%'):
            expanded_path = os.path.expandvars(change_dir)
            if os.path.exists(expanded_path):
                return os.path.abspath(expanded_path)
            else:
                print(f"{Fore.RED}Error: Path '{expanded_path}' not found.{Style.RESET_ALL}")
                return work_dir
        else:
            new_path = os.path.join(work_dir, change_dir)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{Fore.RED}Error: Path '{new_path}' not found.{Style.RESET_ALL}")
                return work_dir
    elif os_type in ("linux", "macos"):
        # 检查 change_dir 是否以根路径开头
        if change_dir.startswith("/") or change_dir.startswith('"/'):
            path = change_dir.strip('"')
            if os.path.exists(path):
                return os.path.abspath(path)
            else:
                print(f"{Fore.RED}Error: Path '{path}' not found.{Style.RESET_ALL}")
                return work_dir
        # 处理当前目录
        elif change_dir in (".", '"."'):
            return work_dir
        # 展开用户主目录
        elif change_dir.startswith("~") or change_dir.startswith('"~'):
            path = change_dir.strip('"')
            home_dir = os.path.expanduser("~")
            new_path = os.path.join(home_dir, path[1:] if path.startswith("~") else path)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{Fore.RED}Error: Path '{new_path}' not found.{Style.RESET_ALL}")
                return work_dir
        else:
            new_path = os.path.join(work_dir, change_dir)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{Fore.RED}Error: Path '{new_path}' not found.{Style.RESET_ALL}")
                return work_dir
    else:
        print(f"{Fore.RED}Error: Unsupported OS.{Style.RESET_ALL}")
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
            print(f"{Fore.GREEN}Directory '{work_dir}' created successfully.{Style.RESET_ALL}")
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
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Failed to load commands list.{Style.RESET_ALL}")
        return
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Failed to parse commands list.{Style.RESET_ALL}")
        return
    print(f"{Fore.YELLOW}% Quarter OS - Help Menu %{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=========================={Style.RESET_ALL}")
    for cmd, desc in noargs_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in needargs_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in pm_cmds_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    print(f"{Fore.BLUE}For Third-party commands, please enter 'biscuit list'.{Style.RESET_ALL}")
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
    print(f"{Fore.BLUE}& Quarter OS System Info &{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Operating System: {Fore.CYAN}{platform.system()} {platform.release()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Python Version: {Fore.CYAN}{platform.python_version()}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")
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
                sys.exit()
            elif exit_cfm == "n":
                return 0
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
    print(f"{Fore.CYAN}get <pkg>      - Get package from online repository (Comming Soon){Style.RESET_ALL}")
    print(f"{Fore.CYAN}mirror <url>   - Set a mirror for package repository (Comming Soon){Style.RESET_ALL}")
