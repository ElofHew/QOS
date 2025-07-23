# Quarter OS Backup Application
import os
import sys
import json
import zipfile
import time as tm
import pathlib
from colorama import Fore, Style

try:
    with open(os.path.join("data", "config", "config.json"), "r") as f:
        config = json.load(f)
    qos_path = config.get("qos_path", os.getcwd())
    qos_version = config.get("version", "Unknown")
except FileNotFoundError:
    print(f"{Fore.RED}Error: File 'config.json' in QOS not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"{Fore.RED}Error: Failed to parse 'config.json'.")
    sys.exit(1)
except Exception as e:
    print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    sys.exit(1)

bpath = os.path.join(qos_path, "backup")

__usage__ = """Quarter OS Backup Usage:
-c : Create backup
-r : Remove backup file
-l : List all backup files
"""

def create():
    try:
        # 询问是否确认创建备份
        while True:
            confirm = input(f"{Fore.CYAN}Are you sure to backup? (y/n): {Fore.RESET}")
            if confirm.lower() == "y":
                break
            elif confirm.lower() == "n":
                return 0
            else:
                print(f"{Fore.RED}Invalid input. Please enter 'y' or 'n'.{Style.RESET_ALL}")
                continue

        print(f"{Fore.YELLOW}Creating backup...{Fore.RESET}")

        if not os.path.exists(bpath):
            os.makedirs(bpath)

        backup_file = os.path.join(bpath, f"QOS_{qos_version}_Backup_{tm.strftime('%Y-%m-%d_%H-%M-%S', tm.localtime())}.zip")
        with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 压缩 qos_path 下的 data 文件夹
            data_folder = os.path.join(qos_path, 'data')
            if os.path.exists(data_folder):
                for foldername, subfolders, filenames in os.walk(data_folder):
                    # 跳过备份目录
                    if bpath in foldername:
                        continue
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        # 计算文件在压缩包中的相对路径
                        arcname = os.path.relpath(file_path, start=qos_path)
                        zipf.write(file_path, arcname=arcname)
            else:
                print(f"{Fore.YELLOW}Warning: 'data' folder does not exist under qos_path.{Style.RESET_ALL}")
            # 压缩 qos_path 下的 home 文件夹
            home_folder = os.path.join(qos_path, 'home')
            if os.path.exists(home_folder):
                for foldername, subfolders, filenames in os.walk(home_folder):
                    # 跳过备份目录
                    if bpath in foldername:
                        continue
                    for filename in filenames:
                        file_path = os.path.join(foldername, filename)
                        # 计算文件在压缩包中的相对路径
                        arcname = os.path.relpath(file_path, start=qos_path)
                        zipf.write(file_path, arcname=arcname)
            else:
                print(f"{Fore.YELLOW}Warning: 'home' folder does not exist under qos_path.{Style.RESET_ALL}")
        print(f"{Fore.LIGHTGREEN_EX}Backup created successfully: {Fore.LIGHTBLUE_EX}{pathlib.Path(backup_file)}{Style.RESET_ALL}")
        return 0
    except KeyboardInterrupt:
        print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
        return 0
    except (IOError, OSError) as e:
        print(f"{Fore.RED}Error: Failed to create backup file. {str(e)}{Style.RESET_ALL}")
        return 1
    except ImportError:
        print(f"{Fore.RED}Error: Failed to import 'zipfile' module.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return 1

def list_all():
    try:
        if not os.path.exists(bpath) or not os.listdir(bpath):
            print(f"{Fore.YELLOW}(You have no backup yet.){Style.RESET_ALL}")
            return 0
        print(f"{Fore.LIGHTGREEN_EX}Backup files:{Style.RESET_ALL}")
        dir_list = os.listdir(bpath)
        backup_index = 1
        backup_list = []
        for file in dir_list:
            if file.startswith("QOS_") and file.endswith(".zip"):
                print(f"{Fore.CYAN}{backup_index} - {file}{Style.RESET_ALL}")
                backup_index += 1
                backup_list.append(file)
        return backup_list
    except OSError:
        print(f"{Fore.RED}Error: Failed to list backup files.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return 1

def remove(backup_file=None):
    try:
        if backup_file is None:
            backup_list = list_all()
            if backup_list is None:
                print(f"{Fore.LIGHTGREEN_EX}No backup file need to be removed.{Style.RESET_ALL}")
                return 0
            while True:
                print(f"{Fore.YELLOW}Please select a backup to remove (0 to exit):{Style.RESET_ALL}")
                option = input("> ")
                if option.isdigit() and int(option) > 0 and int(option) <= len(backup_list):
                    will_remove = backup_list[int(option) - 1]
                    break
                else:
                    print(f"{Fore.RED}Invalid input. Please enter a number between 0 and {len(backup_list)}.{Style.RESET_ALL}")
                    continue
        else:
            will_remove = backup_file
        if not os.path.exists(bpath):
            print(f"{Fore.YELLOW}(You have no backup yet.){Style.RESET_ALL}")
            return 0
        if not os.path.exists(os.path.join(bpath, will_remove)):
            print(f"{Fore.YELLOW}Backup file '{will_remove}' does not exist.{Style.RESET_ALL}")
            return 0
        os.remove(os.path.join(bpath, will_remove))
        print(f"{Fore.LIGHTGREEN_EX}Backup file '{will_remove}' removed successfully.{Style.RESET_ALL}")
        return 0
    except KeyboardInterrupt:
        print(f"{Style.DIM}{Fore.YELLOW}\nKeyboardInterrupt detected. Exiting...{Style.RESET_ALL}")
        return 0
    except OSError:
        print(f"{Fore.RED}Error: Failed to remove backup file.{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        return 1

if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "-c":
            create()
        elif sys.argv[1] == "-r":
            remove()
        elif sys.argv[1] == "-l":
            list_all()
        else:
            print(f"{Fore.RED}Error: Unknown option '{sys.argv[1]}'.{Style.RESET_ALL}")
            print(__usage__)
            sys.exit(1)
    else:
        print(__usage__)
        sys.exit(0)
