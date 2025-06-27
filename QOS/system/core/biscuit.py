"""
@ Biscuit Software Manager for QOS
@ Author: ElofHew
@ Version: 0.1
@ Date: 2025.06.24
"""

import os       # 用于操作系统交互，如获取当前目录、创建目录和删除文件等
import sys      # 用于与Python解释器交互，如退出程序等
import subprocess # 用于在Python脚本中运行外部命令
import zipfile  # 用于处理ZIP文件的压缩和解压缩
import time     # 用于添加延迟
import json     # 用于处理JSON文件的读取和写入
import shutil   # 用于文件和目录的高级操作，如复制文件和删除文件夹等
from colorama import init, Fore, Back, Style  # 用于控制输出颜色

init(autoreset=True)  # 初始化颜色模块

with open("data/config/config.json", "r") as f:
    config = json.load(f)
    qos_path = config["qos_path"]

def install(pkg_path):
    package_file_name = os.path.basename(pkg_path)
    # Confirm installation
    print(f"Do you want to install '{package_file_name}' ? (y/n): ")
    while True:
        try:
            check = str(input("> "))
            if check.lower() == "y" or check.lower() == "yes":
                break
            elif check.lower() == "n" or check.lower() == "no":
                print(Fore.RED + "Operation cancelled." + Fore.RESET)
                return 1
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Style.RESET)
                continue
        except KeyboardInterrupt:
            print(Fore.RED + "Operation cancelled." + Fore.RESET)
            return 1
    # Start installation
    print("Installing package...")
    try:
        # Check temp directory
        temp_dir = os.path.join(qos_path, "data", "temp")
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
        else:
            for filename in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path) and filename != 'tmp':
                    shutil.rmtree(file_path)
        # Extract package to temp directory
        destination_path = os.path.join(temp_dir, os.path.basename(pkg_path))
        shutil.copy(pkg_path, destination_path)
        try:
            new_name = os.path.splitext(os.path.basename(pkg_path))[0] + ".zip"
            os.rename(destination_path, os.path.join(temp_dir, new_name))
            unzip_dir = os.path.join(qos_path, "data", "apps", new_name[:-4])
            with zipfile.ZipFile(os.path.join(temp_dir, new_name), 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            with open(os.path.join(unzip_dir, "info.json"), "r") as demo_f:
                config = json.load(demo_f)
            app_name = config["name"]
            app_version = config["version"]
            print(f"{Fore.GREEN}App Name:{Fore.RESET} {app_name}")
            print(f"{Fore.GREEN}App Version:{Fore.RESET} {app_version}")
            # Confirm continue installation
            while True:
                try:
                    contn = str(input(Fore.CYAN + "Continue to install this package? (y/n): " + Fore.RESET))
                    if contn.lower() == "y" or contn.lower() == "yes":
                        break
                    elif contn.lower() == "n" or contn.lower() == "no":
                        print(Fore.RED + "Operation cancelled." + Fore.RESET)
                        return 1
                    else:
                        print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Style.RESET)
                        continue
                except KeyboardInterrupt:
                    print(Fore.RED + "Operation cancelled." + Fore.RESET)
                    return 1
            # Check older version of app
            existing_app_dir = os.path.join(qos_path, "data", "apps", app_name)
            if os.path.exists(existing_app_dir):
                with open(os.path.join(existing_app_dir, "info.json"), "r") as old_f:
                    existing_config = json.load(old_f)
                existing_app_version = existing_config["version"]
                if existing_app_version < app_version:
                    print(f"{Fore.YELLOW}Found older version {existing_app_version} of {app_name}. Installing newer version {app_version}.")
                    shutil.rmtree(existing_app_dir)
                elif existing_app_version == app_version:
                    # Move new app to existing app directory
                    print(f"{app_name} already installed with version {existing_app_version}. No need to install again.")
                    shutil.rmtree(os.path.join(temp_dir, new_name[:-4]))
                    return 0
                else:
                    print(f"{Fore.RED}Error: {app_name} has a higher version than the existing version {existing_app_version}. Please uninstall the existing version first.{Fore.RESET}")
                    return 1
                old_f.close()
            os.rename(unzip_dir, os.path.join(qos_path, "data", "apps", app_name))
            new_path_app = os.path.join(qos_path, "data", "apps", app_name)
            print(f"{Fore.CYAN}Installing dependencies...{Fore.RESET}")
            try:
                if not os.path.exists(os.path.join(new_path_app, "requirements.txt")):
                    pass
                else:
                    os.chdir(new_path_app)
                    subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
                    print(f"{Fore.GREEN}Dependencies installed.{Fore.RESET}")
                with open("data/shell/apps.json") as add_app_f:
                    add_app_config = json.load(add_app_f)
                add_app_config[app_name] = {"path": new_path_app, "version": app_version}
                with open("data/shell/apps.json", "w") as add_app_f:
                    json.dump(add_app_config, add_app_f, indent=4)
                add_app_f.close()
                print(f"{Fore.LIGHTGREEN_EX}Package successfully installed to {new_path_app}!{Fore.RESET}")
                return 0
            except subprocess.CalledProcessError:
                print(f"{Fore.RED}File not found.{Fore.RESET}")
                shutil.rmtree(os.path.join(temp_dir, new_name[:-4]))
                return 1
            except Exception as e:
                print(f"{Fore.RED}An error occurred during installing dependencies: {e}{Fore.RESET}")
                shutil.rmtree(os.path.join(temp_dir, new_name[:-4]))
                return 1
        except Exception as e:
            print(f"{Fore.RED}An error occurred during renaming or extraction: {e}{Fore.RESET}")
            shutil.rmtree(os.path.join(temp_dir, new_name[:-4]))
            return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        if 'new_name' in locals():
            shutil.rmtree(os.path.join(temp_dir, new_name[:-4]))
        return 1

def remove(app_name):
    print(f"{Fore.RED}Removing package: {app_name}{Fore.RESET}")
    # Confirm removal
    while True:
        try:
            check = str(input(f"{Fore.CYAN}Do you want to remove the package '{app_name}'? (y/n): {Fore.RESET}"))
            if check == "y" or check == "Y":
                break
            elif check == "n" or check == "N":
                print(Fore.RED + "Operation cancelled." + Fore.RESET)
                return 1
            else:
                print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Fore.RESET)
                continue
        except KeyboardInterrupt:
            print(Fore.RED + "Operation cancelled." + Fore.RESET)
            return 1
    # Cheak app registry
    try:
        with open("data/shell/apps.json") as add_app_f:
            add_app_config = json.load(add_app_f)
            if app_name in add_app_config:
                app_dir = add_app_config[app_name]["path"]
                pass
            else:
                print(f"{Fore.YELLOW}Package '{app_name}' not found. No need to remove.{Fore.RESET}")
                return 1
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    # Remove app directory
    try:
        shutil.rmtree(app_dir)
        print(f"{Fore.GREEN}Package '{app_name}' has been successfully removed.{Fore.RESET}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}An error occurred during removal: {e}{Fore.RESET}")
        return 1

def list():
    try:
        with open("data/shell/apps.json") as add_app_f:
            add_app_config = json.load(add_app_f)
        if len(add_app_config) == 0:
            print(f"{Fore.YELLOW}No packages installed.{Fore.RESET}")
            return 1
        else:
            print(f"{Fore.GREEN}Installed packages:{Fore.RESET}")
            for app_name in add_app_config:
                app_version = add_app_config[app_name]["version"]
                print(f"{Fore.CYAN}{app_name} {app_version}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1