"""
@ PY OS Improved
@ Shizuku Software Manager
@ Shizuku Application Package Installer Core Module
@ Author: ElofHew
@ Version: 1.0
@ Date: 2025.05.02
"""

import os       # 用于操作系统交互，如获取当前目录、创建目录和删除文件等
import sys      # 用于与Python解释器交互，如退出程序等
import subprocess # 用于在Python脚本中运行外部命令
import zipfile  # 用于处理ZIP文件的压缩和解压缩
import time     # 用于添加延迟
import json     # 用于处理JSON文件的读取和写入
import shutil   # 用于文件和目录的高级操作，如复制文件和删除文件夹等
from colorama import Fore, Style, init # 用于控制终端输出的颜色

init(autoreset=True) # 初始化颜色模块

with open(os.path.join(os.getcwd(), "data", "config", "config.json")) as qos_config_file:
    qos_config = json.load(qos_config_file)
    os_type = qos_config["os_type"]
    qos_path = qos_config["qos_path"]

szk_install_path = os.path.join(qos_path, "data", "shizuku")
if not os.path.exists(szk_install_path):
    os.makedirs(szk_install_path)

def main(working_path, args):
    try:
        if not args:
            tips()
            return 0
        if args[0]:
            match args[0]:
                case "help":
                    tips()
                case "list":
                    list_apps()
                case "install":
                    install(working_path, args[1:])
                case "remove":
                    remove(args[1:])
                case "run":
                    run(args[1:])
                case _:
                    print(f"{Fore.RED}Invalid arguments.{Fore.RESET}")
            return 0
    except KeyboardInterrupt:
        print(f"{Fore.RED}Operation cancelled.{Fore.RESET}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1

def tips():
    print(f"{Fore.LIGHTGREEN_EX}% Shizuku Package Manager %{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}==========================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}install <path> - Install a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}remove <pkg>   - Remove a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}list           - List all installed packages{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}run <pkg>      - Run a installed shizuku package{Style.RESET_ALL}")

def run(aargs):
    __usage__ = "Usage: shizuku run <pkg>"
    if len(aargs)!= 1:
        print(f"{Fore.YELLOW}{__usage__}{Style.RESET_ALL}")
        return
    pkg_name = aargs[0]
    app_dir_path = os.path.join(szk_install_path, pkg_name)
    if not os.path.isdir(app_dir_path):
        print(f"{Fore.RED}Error: {pkg_name} not found.{Style.RESET_ALL}")
        return
    if os.listdir(app_dir_path) == []:
        print(f"{Fore.RED}No Shizuku package installed.{Style.RESET_ALL}")
        return
    for app_main in os.listdir(app_dir_path):
        app_main_path = os.path.join(app_dir_path, app_main)
        if os.path.isfile(app_main_path) and app_main.endswith(".py"):
            try:
                os.chdir(app_dir_path)
                szk_process = subprocess.Popen([subprocess.sys.executable, app_main_path])
                szk_process.wait()
                if szk_process.returncode != 0:
                    print(f"{Fore.RED}Error: subprocess returned {szk_process.returncode}{Style.RESET_ALL}")
                    return
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
                return
            finally:
                if szk_process.poll() is None:
                    szk_process.kill()
                os.chdir(qos_path)

def install(work_dir, aargs):
    __usage__ = "Usage: shizuku install <path>"
    if len(aargs)!= 1:
        print(f"{Fore.YELLOW}{__usage__}{Style.RESET_ALL}")
        return 1
    pkg_path = aargs[0]
    if not os.path.isfile(os.path.join(work_dir, pkg_path)):
        print(f"{Fore.RED}Error: {pkg_path} not found.{Style.RESET_ALL}")
        return 1
    pkg_file = os.path.join(work_dir, pkg_path)
    print(Fore.CYAN + f"path: {os.path.abspath(pkg_file)}" + Style.RESET_ALL)
    
    while True:
        check = input(Fore.YELLOW + "Do you want to install this package? (y/n): ").strip().lower()
        if check == "y":
            break
        elif check == "n":
            print(Fore.RED + "Operation cancelled.")
            return 1
        else:
            print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")
    
    print(Fore.GREEN + "Installing package...")
    try:
        destination_dir = os.path.join(qos_path, "data", "temp", "shizuku")
        os.makedirs(destination_dir, exist_ok=True)  # 创建目录，如果已存在则忽略
        
        destination_path = os.path.join(destination_dir, os.path.basename(pkg_path))
        shutil.copy(pkg_file, destination_path)
        
        new_name = os.path.splitext(destination_path)[0] + ".zip"
        os.rename(destination_path, new_name)
        
        unzip_dir = os.path.join(qos_path, "data", "shizuku", os.path.basename(new_name)[:-4])
        with zipfile.ZipFile(new_name, 'r') as zip_ref:
            zip_ref.extractall(unzip_dir)
        
        with open(os.path.join(unzip_dir, "info.json"), "r") as f:
            config = json.load(f)
        
        app_name = config["name"]
        app_version = config["version"]
        print(Fore.GREEN + f"Installing {app_name} {app_version}...")
        
        existing_app_dir = os.path.join(qos_path, "data", "shizuku", app_name)
        if os.path.exists(existing_app_dir):
            with open(os.path.join(existing_app_dir, "info.json"), "r") as f:
                existing_config = json.load(f)
            
            existing_app_version = existing_config["version"]
            if existing_app_version < app_version:
                print(Fore.YELLOW + f"Found older version {existing_app_version} of {app_name}. Installing newer version {app_version}.")
                shutil.rmtree(existing_app_dir)
            else:
                print(Fore.YELLOW + f"{app_name} already installed with version {existing_app_version}. No need to install again.")
                shutil.rmtree(unzip_dir)
                return 0
        
        os.rename(unzip_dir, os.path.join(qos_path, "data", "shizuku", app_name))
        new_path_app = os.path.join(qos_path, "data", "shizuku", app_name)
        os.rename(os.path.join(new_path_app, "main.py"), os.path.join(new_path_app, app_name + ".py"))
        
        print(Fore.GREEN + "Installing dependencies...")
        try:
            os.chdir(new_path_app)
            subprocess.run([subprocess.sys.executable, '-m', 'pip', "install", "-r", "requirements.txt"], check=True)
            print(Fore.GREEN + "Dependencies installed.")
            print(Fore.GREEN + f"Package successfully installed to {new_path_app}")
            print("="*30)
            print(Fore.CYAN + "How to run the application:")
            print(Fore.CYAN + f"You can just input the command 'shizuku run {app_name}' in Kom Shell.")
            print("="*30)
            print(Fore.GREEN + f"{app_name} {app_version} has been successfully installed.")
            return 0
        except subprocess.CalledProcessError:
            print(Fore.RED + "No requirements.txt found or installation failed.")
        except Exception as e:
            print(Fore.RED + f"An error occurred during installing dependencies: {e}")
        finally:
            os.chdir(qos_path)
            shutil.rmtree(destination_dir)
            return 1
    except Exception as e:
        print(Fore.RED + f"An error occurred: {e}")
        os.chdir(qos_path)
        if os.path.exists(destination_dir):
            shutil.rmtree(destination_dir)
        return 1


def remove(aargs):
    __usage__ = "Usage: shizuku remove <pkg>"
    if len(aargs)!= 1:
        print(f"{Fore.YELLOW}{__usage__}{Style.RESET_ALL}")
        return 1
    app_name = aargs[0]
    # 打印应用名称
    print(Fore.CYAN + f"Removing package: {app_name}")
    # 循环提示用户是否要卸载该包，直到输入有效选项
    while True:
        check = str(input(Fore.YELLOW + f"Do you want to remove the package '{app_name}'? (y/n): "))
        if check == "y" or check == "Y":
            # 如果用户输入 'y' 或 'Y'，则跳出循环继续卸载
            break
        elif check == "n" or check == "N":
            # 如果用户输入 'n' 或 'N'，则取消操作并返回状态码
            print(Fore.RED + "Operation cancelled.")
            return 1
        else:
            # 如果用户输入无效选项，则提示重新输入
            print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")
            continue
    # 定义应用目录路径
    app_dir = os.path.join(qos_path, "data", "shizuku", app_name)
    # 检查应用目录是否存在
    if not os.path.exists(app_dir):
        print(Fore.RED + f"Package '{app_name}' not found. No need to remove.")
        return 1
    try:
        # 删除应用目录
        shutil.rmtree(app_dir)
        print(Fore.GREEN + f"Package '{app_name}' has been successfully removed.")
        # 再次添加延迟以便用户查看卸载完成信息
        time.sleep(2)
        # 卸载完成后返回状态码
        return 0
    except Exception as e:
        # 如果在删除过程中发生异常，则打印异常信息
        print(Fore.RED + f"An error occurred during removal: {e}")
        return 1

def list_apps():
    try:
        # 打印已安装的应用列表
        print(Fore.CYAN + "Installed packages:")
        # 遍历 shizuku 目录下的所有应用目录
        for app_name in os.listdir(os.path.join(qos_path, "data", "shizuku")):
            if os.listdir(os.path.join(qos_path, "data", "shizuku", app_name)) == []:
                print(Fore.CYAN + "No Shizuku package installed.")
                return 1
            # 打开应用目录中的 info.json 文件以获取应用信息
            with open(os.path.join(qos_path, "data", "shizuku", app_name, "info.json"), "r") as f:
                config = json.load(f)
            # 从 info.json 中读取应用名称和版本号
            app_name = config["name"]
            app_version = config["version"]
            # 打印应用名称和版本号
            print(Fore.GREEN + f"{app_name} {app_version}")
    except FileNotFoundError:
        # 如果 shizuku 目录不存在，则提示相应信息
        print(Fore.RED + "Error: shizuku directory not found.")
        return 1
    except Exception as e:
        # 如果在列出过程中发生异常，则打印异常信息
        print(Fore.RED + f"An error occurred during listing: {e}")
        return 1
