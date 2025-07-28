import os
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

cinit(autoreset=True)

try:
    with open(os.path.join("data", "config", "config.json"), "r") as config_file:
        config = json.load(config_file)
        os_type = config.get("os_type", "")
        last_login = config.get("last_login", "")
        qos_path = config.get("qos_path", "")
        qos_version = config.get("version", "")
        qos_edition = config.get("qos_edition", "")
        system_path = config.get("system_path", "")
        data_path = config.get("data_path", "")
        home_path = config.get("home_path", "")
        activate_statue = config.get("activate_statue", "")
except FileNotFoundError:
    print(f"{Fore.RED}Error: Config file not found.{Style.RESET_ALL}")
    sys.exit(19)
except json.JSONDecodeError:
    print(f"{Fore.RED}Error: Config file is not in JSON format.{Style.RESET_ALL}")
    sys.exit(19)
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    sys.exit(19)

# Need Args
def cat(work_dir, args):
    """Show the contents of a file."""
    __usage__ = "Usage: cat <file_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    file_path = args[0]
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

def echo(work_dir, args):
    """Display a message on the console."""
    __usage__ = "Usage: echo <text>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    text = " ".join(args)
    try:
        print(text)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return

def cp(work_dir, args):
    """Copy a file or directory."""
    __usage__ = "Usage: cp <source_path> <destination_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    if len(args) < 2:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    src = args[0]
    dst = args[1]
    src_path = os.path.join(work_dir, src)
    dst_path = os.path.join(work_dir, dst)
    try:
        if not os.path.exists(src_path):
            print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
            return
        # Check if both file and directory exist
        if os.path.isfile(src_path) and os.path.isdir(src_path):
            while True:
                choice = input(f"Both a file and a directory named '{src}' exist. Copy the file (f) or the directory (d)? ").strip().lower()
                if choice == 'f':
                    shutil.copy(os.path.join(work_dir, src), os.path.join(work_dir, dst))
                    print(f"{Fore.GREEN}File copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
                    break
                elif choice == 'd':
                    shutil.copytree(os.path.join(work_dir, src), os.path.join(work_dir, dst))
                    print(f"{Fore.GREEN}Directory copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}Error: Invalid choice. Please choose 'f' for file or 'd' for directory.{Style.RESET_ALL}")
                    continue
        elif os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
            print(f"{Fore.GREEN}File copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
        elif os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path)
            print(f"{Fore.GREEN}Directory copied successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Source path '{src}' is neither a file nor a directory.{Style.RESET_ALL}")
            return
        if os.path.exists(dst_path):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}Error: Operation cancelled by user.{Style.RESET_ALL}")
        return
    except (IOError, OSError) as e:
        print(f"{Fore.RED}Error: Failed to copy file or directory. {e}{Style.RESET_ALL}")
        return

def mv(work_dir, args):
    """Move a file or directory."""
    __usage__ = "Usage: mv <source_path> <destination_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    if len(args) < 2:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    src = args[0]
    dst = args[1]
    src_file_path = os.path.join(work_dir, src)
    src_dir_path = os.path.join(work_dir, src)
    dst_path = os.path.join(work_dir, dst)
    try:
        if not os.path.exists(src_file_path) and not os.path.exists(src_dir_path):
            print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
            return
        if os.path.exists(src_file_path) and os.path.exists(src_dir_path):
            while True:
                choice = input(f"{Fore.YELLOW}Warning: '{src}' exists both as a file and a directory. Please specify to move the file or directory (enter 'f' for file, 'd' for directory): {Style.RESET_ALL}")
                if choice == 'f':
                    src_path = src_file_path
                    break
                elif choice == 'd':
                    src_path = src_dir_path
                    break
                else:
                    print(f"{Fore.RED}Error: Invalid choice.{Style.RESET_ALL}")
                    continue
        elif os.path.isfile(src_file_path):
            src_path = src_file_path
        else:
            src_path = src_dir_path
        if os.path.isfile(src_path) and os.path.exists(dst_path) and os.path.isfile(dst_path):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists as a file. It will be overwritten.{Style.RESET_ALL}")
        elif os.path.isdir(src_path) and os.path.exists(dst_path) and os.path.isdir(dst_path):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists as a directory. It will be overwritten.{Style.RESET_ALL}")
        shutil.move(src_path, dst_path)
        print(f"{Fore.GREEN}File or directory moved successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}Error: Operation cancelled by user.{Style.RESET_ALL}")
        return
    except (IOError, OSError) as e:
        print(f"{Fore.RED}Error: Failed to move file or directory. {e}{Style.RESET_ALL}")
        return

def ls(work_dir, args):
    """Show the list of files and directories in a directory."""
    __usage__ = "Usage: ls <directory_path>"
    if len(args) == 0:
        list_path = "."
    else:
        list_path = args[0]
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
        return

def cd(work_dir, args):
    """Change the current directory."""
    __usage__ = "Usage: cd <directory_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return work_dir
    change_dir = args[0]
    try:
        with open("data/config/config.json", "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
            home_path = config.get("home_path", "")
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

def touch(work_dir, args):
    """Create a new file."""
    __usage__ = "Usage: touch <file_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    file_path = args[0]
    try:
        if os.path.exists(os.path.join(work_dir, file_path)):
            print(f"{Fore.YELLOW}Warning: File '{file_path}' already exists.{Style.RESET_ALL}")
        else:
            with open(os.path.join(work_dir, file_path), "w") as f:
                f.write("")
            print(f"{Fore.GREEN}File '{file_path}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create file. {e}{Style.RESET_ALL}")
        return

def edit(work_dir, args):
    """Edit a file."""
    __usage__ = "Usage: edit <file_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    file_path = args[0]
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
        return

def mkdir(work_dir, args):
    """Create a new directory."""
    __usage__ = "Usage: mkdir <directory_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    new_dir = args[0]
    try:
        if os.path.exists(os.path.join(work_dir, new_dir)):
            print(f"{Fore.YELLOW}Warning: Path '{work_dir}' already exists.{Style.RESET_ALL}")
        else:
            os.makedirs(os.path.join(work_dir, new_dir))
            print(f"{Fore.GREEN}Directory '{new_dir}' created successfully.{Style.RESET_ALL}")
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to create directory. {e}{Style.RESET_ALL}")
        return

def rename(work_dir, args):
    """Rename a file or directory."""
    __usage__ = "Usage: rename <old_name> <new_name>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    if len(args) < 2:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    src = args[0]
    dst = args[1]
    src_path = os.path.join(work_dir, src)
    dst_path = os.path.join(work_dir, dst)
    try:
        if not os.path.exists(src_path):
            print(f"{Fore.RED}Error: Source path '{src}' does not exist.{Style.RESET_ALL}")
            return
        # Check if both file and directory exist
        if os.path.isfile(src_path) and os.path.isdir(src_path):
            while True:
                choice = input(f"Both a file and a directory named '{src}' exist. Rename the file (f) or the directory (d)? ").strip().lower()
                if choice == 'f':
                    src_path = os.path.join(work_dir, src)
                    break
                elif choice == 'd':
                    src_path = os.path.join(work_dir, src)
                    break
                else:
                    print(f"{Fore.RED}Error: Invalid choice. Please choose 'f' for file or 'd' for directory.{Style.RESET_ALL}")
                    continue
        elif os.path.isfile(src_path):
            pass  # src_path is already correctly set to the file path
        elif os.path.isdir(src_path):
            pass  # src_path is already correctly set to the directory path
        else:
            print(f"{Fore.RED}Error: Source path '{src}' is neither a file nor a directory.{Style.RESET_ALL}")
            return
        if os.path.exists(dst_path):
            print(f"{Fore.YELLOW}Warning: Destination path '{dst}' already exists. It will be overwritten.{Style.RESET_ALL}")
        os.rename(src_path, dst_path)
        print(f"{Fore.GREEN}File or directory renamed successfully from '{src}' to '{dst}'.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}Error: Operation cancelled by user.{Style.RESET_ALL}")
        return
    except (IOError, OSError) as e:
        print(f"{Fore.RED}Error: Failed to rename file or directory. {e}{Style.RESET_ALL}")
        return

def rm(work_dir, args):
    """Remove a file or directory."""
    __usage__ = "Usage: rm <file_path>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    rm_path = args[0]
    rm_full_path = os.path.join(work_dir, rm_path)
    try:
        if not os.path.exists(rm_full_path):
            print(f"{Fore.RED}Error: Path '{rm_path}' does not exist.{Style.RESET_ALL}")
            return
        # Check if both file and directory exist
        if os.path.isfile(rm_full_path) and os.path.isdir(rm_full_path):
            while True:
                choice = input(f"Both a file and a directory named '{rm_path}' exist. Remove the file (f) or the directory (d)? ").strip().lower()
                if choice == 'f':
                    rm_full_path = os.path.join(work_dir, rm_path)
                    os.remove(rm_full_path)
                    print(f"{Fore.GREEN}File '{rm_path}' removed successfully.{Style.RESET_ALL}")
                    break
                elif choice == 'd':
                    rm_full_path = os.path.join(work_dir, rm_path)
                    shutil.rmtree(rm_full_path)
                    print(f"{Fore.GREEN}Directory '{rm_path}' removed successfully.{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}Error: Invalid choice. Please choose 'f' for file or 'd' for directory.{Style.RESET_ALL}")
                    continue
        elif os.path.isfile(rm_full_path):
            os.remove(rm_full_path)
            print(f"{Fore.GREEN}File '{rm_path}' removed successfully.{Style.RESET_ALL}")
        elif os.path.isdir(rm_full_path):
            shutil.rmtree(rm_full_path)
            print(f"{Fore.GREEN}Directory '{rm_path}' removed successfully.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Error: Path '{rm_path}' is neither a file nor a directory.{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"{Fore.RED}Error: Operation cancelled by user.{Style.RESET_ALL}")
        return
    except (IOError, OSError) as e:
        print(f"{Fore.RED}Error: Failed to remove file or directory. {e}{Style.RESET_ALL}")
        return

def ping(working_dir, args):
    """Check the network connection to a host."""
    __usage__ = "Usage: ping <host>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    host = args[0]
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

def down(working_dir, args):
    """Download a file from the internet."""
    __usage__ = "Usage: down <url>"
    if len(args) == 0:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return
    url = args[0]
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
            start_time = tm.time()
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            end_time = tm.time()
            print(f"{Fore.LIGHTGREEN_EX}Download file successfully in {end_time - start_time:.2f} seconds.{Fore.RESET}")
            print(f"{Fore.CYAN}Path: {file_path}{Fore.RESET}")
        else:
            print(f"{Fore.RED}Download file failed. Code: {response.status_code}{Fore.RESET}")
    except KeyboardInterrupt:
        print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
        return
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error: Failed to download file. {e}{Style.RESET_ALL}")
        return
    except Exception as e:
        print(f"{Fore.RED}Download file failed. Error: {e}{Fore.RESET}")
        return

# No Args
def pwd(working_dir=None, args=None):
    print(pathlib.Path(working_dir))

def cwd(working_dir=None, args=None):
    print(os.getcwd())

def help(working_dir=None, args=None):
    try:
        with open(os.path.join(qos_path, "system", "shell", "cmds.json"), "r") as cmds_file:
            cmds_list = json.load(cmds_file)
            core_list = cmds_list["Core"]
            syskit_list = cmds_list["SystemKit"]
            pm_cmds_list = cmds_list["PackageManager"]
    except FileNotFoundError:
        print(f"{Fore.RED}Error: Failed to load commands list.{Style.RESET_ALL}")
        return
    except json.JSONDecodeError:
        print(f"{Fore.RED}Error: Failed to parse commands list.{Style.RESET_ALL}")
        return
    print(f"{Fore.YELLOW}% Quarter OS - Help Menu %{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}=========================={Style.RESET_ALL}")
    for cmd, desc in core_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in syskit_list.items():
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    for cmd, desc in pm_cmds_list.items():
        if desc == None:
            continue
        print(f"{Fore.GREEN}{cmd}{Style.RESET_ALL}: {desc}")
    print(f"{Fore.YELLOW}=========={Style.RESET_ALL}")
    print(f"{Fore.LIGHTBLUE_EX}For Other Apps, please enter 'biscuit list'.{Style.RESET_ALL}")
    with open(os.path.join(data_path, "config", "config.json"), "r") as apps_file:
        apps_config = json.load(apps_file)
        ucp = apps_config["unknown_command_progression"]
    if ucp:
        print(f"{Fore.CYAN}Tips: Run system commands is enabled. Unknown commands will be executed as system commands.{Style.RESET_ALL}")
    else:
        print(f"{Fore.CYAN}Tips: Run system commands is disabled. Unknown commands will not be executed.{Style.RESET_ALL}")

def about(working_dir=None, args=None):
    print(f"{Fore.LIGHTBLUE_EX}% Quarter OS - About %{Style.RESET_ALL}")
    cat("system/etc/about.txt")

def version(working_dir=None, args=None):
    print(f"{Fore.GREEN}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")

def whoami(working_dir=None, args=None):
    with open("data/config/config.json", "r") as config_file:
        config = json.load(config_file)
        username = config["last_login"]
    print(f"{Fore.GREEN}Current user: {Fore.CYAN}{username}{Style.RESET_ALL}")

def time(working_dir=None, args=None):
    print(f"{Fore.GREEN}Current time: {Fore.CYAN}{tm.strftime('%H:%M:%S', tm.localtime())}{Style.RESET_ALL}")

def date(working_dir=None, args=None):
    print(f"{Fore.GREEN}Current date: {Fore.CYAN}{tm.strftime('%Y-%m-%d', tm.localtime())}{Style.RESET_ALL}")

def sysinfo(working_dir=None, args=None):
    print(f"{Fore.BLUE}& Quarter OS System Info &{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Operating System: {Fore.CYAN}{platform.system()} {platform.release()}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}Python Version: {Fore.CYAN}{platform.python_version()}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Version: {Fore.CYAN}{qos_version}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Activate Condition: {Fore.CYAN}{str(activate_statue)}{Style.RESET_ALL}")
    if activate_statue:
        print(f"{Fore.LIGHTMAGENTA_EX}Quarter OS Edition: {Fore.CYAN}{qos_edition}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTMAGENTA_EX}Current User: {Fore.CYAN}{last_login}{Style.RESET_ALL}")
    print(f"{Fore.LIGHTYELLOW_EX}QOS Path: {Fore.CYAN}{qos_path}{Style.RESET_ALL}")

def clear(working_dir=None, args=None):
    pfs = platform.system().lower()
    if pfs == "windows":
        os.system("cls")
    elif pfs == "linux" or pfs == "darwin":
        os.system("clear")
    else:
        print(f"{Fore.RED}Error: Unsupported OS.{Style.RESET_ALL}")

def eula(working_dir=None, args=None):
    cat(qos_path, ["system/etc/eula.txt"])

def exit(working_dir=None, args=None):
    print(f"{Fore.CYAN}Are you sure you want to exit? (y/n){Style.RESET_ALL}")
    while True:
        try:
            exit_cfm = input("> ").strip().lower()
            if exit_cfm == "y":
                clear()
                sys.exit(0)
            elif exit_cfm == "n":
                return False
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            clear()
            sys.exit(17)

def reboot(working_dir=None, args=None):
    print(f"{Fore.CYAN}Are you sure you want to reboot? (y/n){Style.RESET_ALL}")
    while True:
        try:
            reboot_cfm = input("> ").strip().lower()
            if reboot_cfm == "y":
                clear()
                sys.exit(11)
            elif reboot_cfm == "n":
                return False
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
            clear()
            sys.exit(17)
