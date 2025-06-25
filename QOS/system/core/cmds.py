import os
import sys
import json
import platform
import colorama
import shutil

colorama.init(autoreset=True)

def cp(src, dst):
    if not os.path.exists(src):
        print(f"{colorama.Fore.RED}Error: Source path '{src}' does not exist.{colorama.Style.RESET_ALL}")
        return
    if os.path.exists(dst):
        print(f"{colorama.Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{colorama.Style.RESET_ALL}")
    try:
        shutil.copy(src, dst)
        print(f"{colorama.Fore.GREEN}File copied successfully from '{src}' to '{dst}'.{colorama.Style.RESET_ALL}")
    except IOError as e:
        print(f"{colorama.Fore.RED}Error: Failed to copy file. {e}{colorama.Style.RESET_ALL}")

def ls(work_path):
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        os_type = config["os_type"]
    if os_type == "windows":
        if not os.path.exists(work_path):
            print(f"{colorama.Fore.RED}Error: Path '{work_path}' does not exist.{colorama.Style.RESET_ALL}")
            return
        for file in os.listdir(work_path):
            print(file)
    elif os_type in ("linux", "macos"):
        if not os.path.exists(work_path):
            print(f"{colorama.Fore.RED}Error: Path '{work_path}' does not exist.{colorama.Style.RESET_ALL}")
            return
        for file in os.listdir(work_path):
            print(file)
    else:
        print(f"{colorama.Fore.RED}Error: Unsupported OS.{colorama.Style.RESET_ALL}")

def cd(change_dir, work_dir):
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        os_type = config["os_type"]
    if os_type == "windows":
        # 检查 change_dir 是否以盘符开头
        if change_dir.startswith(tuple(f"{chr(x)}:\\" for x in range(67, 91))) or change_dir.startswith(tuple(f'"{chr(x)}:\\"' for x in range(67, 91))):
            if os.path.exists(change_dir):
                return os.path.abspath(change_dir)
            else:
                print(f"{colorama.Fore.RED}Error: Path '{change_dir}' does not exist.{colorama.Style.RESET_ALL}")
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
                print(f"{colorama.Fore.RED}Error: Path '{expanded_path}' does not exist.{colorama.Style.RESET_ALL}")
                return work_dir
        else:
            new_path = os.path.join(work_dir, change_dir)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{colorama.Fore.RED}Error: Path '{new_path}' does not exist.{colorama.Style.RESET_ALL}")
                return work_dir
    elif os_type in ("linux", "macos"):
        # 检查 change_dir 是否以根路径开头
        if change_dir.startswith("/") or change_dir.startswith('"/'):
            path = change_dir.strip('"')
            if os.path.exists(path):
                return os.path.abspath(path)
            else:
                print(f"{colorama.Fore.RED}Error: Path '{path}' does not exist.{colorama.Style.RESET_ALL}")
                return work_dir
        # 处理当前目录
        elif change_dir in (".", '"."'):
            return work_dir
        # 展开用户主目录
        elif change_dir.startswith("~") or change_dir.startswith('"~'):
            path = change_dir.strip('"')
            home_dir = os.path.expanduser("~")
            new_path = os.path.join(home_dir, path[1:])
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{colorama.Fore.RED}Error: Path '{new_path}' does not exist.{colorama.Style.RESET_ALL}")
                return work_dir
        else:
            new_path = os.path.join(work_dir, change_dir)
            if os.path.exists(new_path):
                return os.path.abspath(new_path)
            else:
                print(f"{colorama.Fore.RED}Error: Path '{new_path}' does not exist.{colorama.Style.RESET_ALL}")
                return work_dir
    else:
        print(f"{colorama.Fore.RED}Error: Unsupported OS.{colorama.Style.RESET_ALL}")
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
        print(f"{colorama.Fore.RED}Error: Unsupported OS.{colorama.Style.RESET_ALL}")

def exit():
    print(f"{colorama.Fore.CYAN}Are you sure you want to exit? (y/n){colorama.Style.RESET_ALL}")
    while True:
        try:
            exit_cfm = input("> ").strip().lower()
            if exit_cfm == "y":
                clear()
                sys.exit()
            elif exit_cfm == "n":
                break
            else:
                print(f"{colorama.Fore.RED}Invalid input. Please enter 'y' or 'n'.{colorama.Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{colorama.Fore.DIM}{colorama.Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{colorama.Style.RESET_ALL}")
            clear()
            sys.exit(0)