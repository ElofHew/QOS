import os
import sys
import json
import platform
from colorama import init as cinit
from colorama import Fore, Style, Back
import shutil
import subprocess

cinit(autoreset=True)

pfs = platform.system().lower()

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

def mkdir(work_path):
    try:
        if os.path.exists(work_path):
            print(f"{Fore.YELLOW}Warning: Path '{work_path}' already exists.{Style.RESET_ALL}")
        else:
            os.makedirs(work_path)
            print(f"{Fore.GREEN}Directory '{work_path}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create directory. {e}{Style.RESET_ALL}")

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
                break
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            clear()
            sys.exit(0)