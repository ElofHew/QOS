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

def tips():
    print(f"{Fore.LIGHTGREEN_EX}% Shizuku Package Manager %{Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}==========================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}install <path> - Install a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}remove <pkg>   - Remove a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}list           - List all installed packages{Style.RESET_ALL}")
    print(f"{Fore.YELLOW}run <pkg>      - Run a installed shizuku package{Style.RESET_ALL}")

def run(pkg_name):
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
                if os_type == "windows":
                    szk_process = subprocess.Popen(["python", app_main_path])
                else:
                    szk_process = subprocess.Popen(["python3", app_main_path])
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

def install(work_dir, pkg_path):
    pkg_file = os.path.join(work_dir, pkg_path)
    # 打印包路径
    print(Fore.CYAN + "path: " + os.path.abspath(pkg_file) + Style.RESET_ALL)
    # 循环提示用户是否要安装该包，直到输入有效选项
    while True:
        check = str(input(Fore.YELLOW + "Do you want to install this package? (y/n): "))
        if check == "y" or check == "Y":
            # 如果用户输入 'y' 或 'Y'，则跳出循环继续安装
            break
        elif check == "n" or check == "N":
            # 如果用户输入 'n' 或 'N'，则取消操作并返回状态码
            print(Fore.RED + "Operation cancelled.")
            return 1
        else:
            # 如果用户输入无效选项，则提示重新输入
            print(Fore.RED + "Invalid input. Please enter 'y' or 'n'.")
            continue
    # 提示开始安装包
    print(Fore.GREEN + "Installing package...")
    try:
        # 定义目标目录路径（data/temp/shizuku）
        destination_dir = os.path.join(qos_path, "data", "temp", "shizuku")
        
        # 检查目标目录是否存在，如果不存在则创建它
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        else:
            # 如果目标目录存在，清空目录中的所有文件和文件夹（但保留tmp文件夹本身）
            for filename in os.listdir(destination_dir):
                file_path = os.path.join(destination_dir, filename)
                if os.path.isfile(file_path):
                    # 对于文件，直接删除
                    os.remove(file_path)
                elif os.path.isdir(file_path) and filename != 'temp':
                    # 对于文件夹且不是 'tmp' 文件夹，递归删除整个文件夹
                    shutil.rmtree(file_path)
        
        # 构建目标文件的完整路径（目标目录加上包的文件名）
        destination_path = os.path.join(destination_dir, os.path.basename(pkg_path))
        # 将包文件复制到目标目录
        shutil.copy(pkg_file, destination_path)
        try:
            # 重命名文件为 .zip 扩展名
            new_name = os.path.splitext(os.path.basename(pkg_path))[0] + ".zip"
            os.rename(destination_path, os.path.join(destination_dir, new_name))
            # 定义解压目录路径（data/shizuku 加上包名去掉 .zip 后缀）
            unzip_dir = os.path.join(qos_path, "data", "shizuku", new_name[:-4])  # 去掉 .zip 后缀
            # 使用 zipfile 模块解压文件到解压目录
            with zipfile.ZipFile(os.path.join(destination_dir, new_name), 'r') as zip_ref:
                zip_ref.extractall(unzip_dir)
            # 打开解压目录中的 info.json 文件以获取应用信息
            with open(os.path.join(unzip_dir, "info.json"), "r") as f:
                config = json.load(f)
            # 从 info.json 中读取应用名称和版本号
            app_name = config["name"]
            app_version = config["version"]
            print(Fore.GREEN + f"Installing {app_name} {app_version}...")
            # 检查是否已经存在同名的应用目录
            existing_app_dir = os.path.join(qos_path, "data", "shizuku", app_name)
            if os.path.exists(existing_app_dir):
                # 打开已安装目录中的 info.json 文件以获取应用信息
                with open(os.path.join(existing_app_dir, "info.json"), "r") as f:
                    existing_config = json.load(f)
                # 从已安装的 info.json 中读取应用版本号
                existing_app_version = existing_config["version"]
                
                # 比较版本号
                if existing_app_version < app_version:
                    print(Fore.YELLOW + f"Found older version {existing_app_version} of {app_name}. Installing newer version {app_version}.")
                    # 删除已安装的软件包
                    shutil.rmtree(existing_app_dir)
                else:
                    print(Fore.YELLOW + f"{app_name} already installed with version {existing_app_version}. No need to install again.")
                    # 删除临时解压的文件夹
                    shutil.rmtree(os.path.join(destination_dir, new_name[:-4]))
                    return 0
            # 将解压目录重命名为应用名称
            os.rename(unzip_dir, os.path.join(qos_path, "data", "shizuku", app_name))
            new_path_app = os.path.join(qos_path, "data", "shizuku", app_name)
            # 将解压目录中的 main.py 文件重命名为应用名称.py
            os.rename(os.path.join(new_path_app, "main.py"), os.path.join(new_path_app, app_name + ".py"))
            print(Fore.GREEN + "Installing dependencies...")
            try:
                # 切换到应用目录
                os.chdir(new_path_app)
                # 安装 requirements.txt 中列出的所有依赖项
                subprocess.run(["pip", "install", "-r", "requirements.txt"], check=True)
                print(Fore.GREEN + "Dependencies installed.")
                print(Fore.GREEN + f"Package successfully installed to {new_path_app}")
                print("="*30)
                print(Fore.CYAN + "How to run the application:")
                print(Fore.CYAN + f"You can just input the command 'shizuku run {app_name}' in Kom Shell.")
                print("="*30)
                print(Fore.GREEN + f"{app_name} {app_version} has been successfully installed.")
                # 安装完成后返回状态码
                return 0
            except subprocess.CalledProcessError:
                # 如果 requirements.txt 文件不存在或命令执行失败，则提示相应信息
                print(Fore.RED + "No requirements.txt found.")
                # 删除临时解压的文件夹
                shutil.rmtree(os.path.join(destination_dir, new_name[:-4]))
                return 1
            except Exception as e:
                # 如果在安装依赖过程中发生其他异常，则打印异常信息
                print(Fore.RED + f"An error occurred during installing dependencies: {e}")
                # 删除临时解压的文件夹
                shutil.rmtree(os.path.join(destination_dir, new_name[:-4]))
                return 1
        except Exception as e:
            # 如果在重命名或解压过程中发生异常，则打印异常信息
            print(Fore.RED + f"An error occurred during renaming or extraction: {e}")
            # 删除临时解压的文件夹
            shutil.rmtree(os.path.join(destination_dir, new_name[:-4]))
            return 1
    except Exception as e:
        # 如果在安装过程中发生其他异常，则打印异常信息
        print(Fore.RED + f"An error occurred: {e}")
        # 删除临时解压的文件夹
        if 'new_name' in locals():
            shutil.rmtree(os.path.join(destination_dir, new_name[:-4]))
        return 1
    finally:
        shutil.rmtree(destination_dir)
        os.chdir(qos_path)
        return

def remove(app_name):
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

def list():
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
