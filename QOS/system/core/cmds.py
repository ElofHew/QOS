import os
import sys
import json
import time
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
def cat(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}Error: File '{file_path}' does not exist.{Style.RESET_ALL}")
            return
        with open(file_path, "r") as f:
            print(f.read())
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to read file. {e}{Style.RESET_ALL}")

def echo(text):
    if all(char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;':\",./<>?" for char in text):
        print(text)
    else:
        print(f"{Fore.RED}Error: Invalid characters in text.{Style.RESET_ALL}")

def cp(src, dst):
    if not os.path.exists(src):
        print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
        return
    if os.path.exists(dst):
        print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
    try:
        shutil.copy(src, dst)
        print(f"{Fore.GREEN}File copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to copy file. {e}{Style.RESET_ALL}")

def mv(src, dst):
    if not os.path.exists(src):
        print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
        return
    if os.path.exists(dst):
        print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
    try:
        shutil.move(src, dst)
        print(f"{Fore.GREEN}File moved successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except IOError as e:
        print(f"{Fore.RED}Error: Failed to move file. {e}{Style.RESET_ALL}")

def ls(work_path):
    try:
        if not os.path.exists(work_path):
            print(f"{Fore.RED}Error: Path '{work_path}' does not exist.{Style.RESET_ALL}")
            return
        elif os.listdir(work_path) == []:
            print(f"{Fore.YELLOW}(This is an empty directory.){Style.RESET_ALL}")
        else:
            for file in os.listdir(work_path):
                if os.path.isfile(os.path.join(work_path, file)):
                    print(f"{Fore.GREEN}{file}{Style.RESET_ALL}")
                elif os.path.isdir(os.path.join(work_path, file)):
                    print(f"{Fore.BLUE}{file}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.WHITE}{file}{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to list directory. {e}{Style.RESET_ALL}")

def cd(change_dir, work_dir):
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

def touch(file_path):
    try:
        if os.path.exists(file_path):
            print(f"{Fore.YELLOW}Warning: File '{file_path}' already exists.{Style.RESET_ALL}")
        else:
            with open(file_path, "w") as f:
                f.write("")
            print(f"{Fore.GREEN}File '{file_path}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create file. {e}{Style.RESET_ALL}")

def edit(file_path):
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}Error: File '{file_path}' does not exist.{Style.RESET_ALL}")
            return
        if os_type == "windows":
            os.startfile(file_path)
        elif os_type == "linux" or os_type == "macos":
            subprocess.call(["xdg-open", file_path])
        else:
            print(f"{Fore.RED}Error: Unsupported OS.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to open file. {e}{Style.RESET_ALL}")

def mkdir(work_path):
    try:
        if os.path.exists(work_path):
            print(f"{Fore.YELLOW}Warning: Path '{work_path}' already exists.{Style.RESET_ALL}")
        else:
            os.makedirs(work_path)
            print(f"{Fore.GREEN}Directory '{work_path}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create directory. {e}{Style.RESET_ALL}")

def rename(src, dst):
    try:
        if not os.path.exists(src):
            print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
            return
        if os.path.exists(dst):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
        os.rename(src, dst)
        print(f"{Fore.GREEN}File renamed successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to rename file. {e}{Style.RESET_ALL}")

def rm(work_path):
    try:
        if not os.path.exists(work_path):
            print(f"{Fore.RED}Error: Path '{work_path}' does not exist.{Style.RESET_ALL}")
            return
        if os.path.isfile(work_path):
            os.remove(work_path)
            print(f"{Fore.GREEN}File '{work_path}' removed successfully.{Style.RESET_ALL}")
        elif os.path.isdir(work_path):
            shutil.rmtree(work_path)
            print(f"{Fore.GREEN}Directory '{work_path}' removed successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to remove file or directory. {e}{Style.RESET_ALL}")

def pwd(working_path):
    print(pathlib.Path(working_path))

def cwd():
    print(os.getcwd())

# No Args
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
    print(f"{Fore.GREEN}Current time: {Fore.CYAN}{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}{Style.RESET_ALL}")

def date():
    print(f"{Fore.GREEN}Current date: {Fore.CYAN}{time.strftime('%Y-%m-%d', time.localtime())}{Style.RESET_ALL}")

def sysinfo():
    print(f"{Fore.BLUE}& Quarter OS System Info &{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Operating System: {Fore.CYAN}{platform.system()} {platform.release()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Current User: {Fore.CYAN}{last_login}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Python Version: {Fore.CYAN}{platform.python_version()}{Style.RESET_ALL}")
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
