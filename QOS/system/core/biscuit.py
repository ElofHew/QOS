"""
@ Biscuit Software Manager for QOS
@ Author: ElofHew
@ Version: 1.0
@ Date: 2025.06.24
"""

import os       # 用于操作系统交互，如获取当前目录、创建目录和删除文件等
import sys      # 用于与Python解释器交互，如退出程序等
import subprocess # 用于在Python脚本中运行外部命令
import zipfile  # 用于处理ZIP文件的压缩和解压缩
import time     # 用于添加延迟
import json     # 用于处理JSON文件的读取和写入
import shutil   # 用于文件和目录的高级操作，如复制文件和删除文件夹等
import requests # 用于处理HTTP请求
from colorama import init, Fore, Back, Style  # 用于控制输出颜色

init(autoreset=True)  # 初始化颜色模块

with open("data/config/config.json", "r") as f:
    config = json.load(f)
    qos_path = config["qos_path"]

def install(working_path, pkg_path):
    ins_pkg_path = os.path.join(working_path, pkg_path)
    temp_path = os.path.join(qos_path,"data", "temp")
    apps_path = os.path.join(qos_path,"data", "apps")
    if not os.path.exists(ins_pkg_path):
        print(f"{Fore.RED}Package not found.{Fore.RESET}")
        return 1
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    if not os.path.exists(apps_path):
        os.makedirs(apps_path)
    # Extract package
    print(f"{Fore.CYAN}Installing package...{Fore.RESET}")
    try:
        with zipfile.ZipFile(ins_pkg_path, "r") as zip_ref:
            zip_ref.extractall(os.path.join(temp_path, "package"))
        temp_path = os.path.join(temp_path, "package")
    except Exception as e:
        print(f"{Fore.RED}An error occurred during package extraction: {e}{Fore.RESET}")
        return 1
    # Get app name and version
    try:
        with open(os.path.join(temp_path, "info.json"), "r") as app_json_f:
            app_json = json.load(app_json_f)
            app_name = app_json["name"]
            app_version = app_json["version"]
            app_vcode = app_json["version_code"]
            app_author = app_json["author"]
            app_desc = app_json["description"]
            app_category = app_json["category"]
            app_min = app_json["min_python_version"]
            app_tar = app_json["target_python_version"]
            app_comptb = app_json["comptb_os"]
            app_bktver = app_json["biscuit_version"]
        while True:
            try:
                check = str(input(f"{Fore.CYAN}Do you want to install the package '{app_name}'? (y/n): {Fore.RESET}"))
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
    except FileNotFoundError:
        print(f"{Fore.RED}File 'info.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    finally:
        app_json_f.close()
    # Install app
    try:
        app_dir = os.path.join(apps_path, app_name)
        if os.path.exists(app_dir):
            with open(os.path.join(app_dir, "info.json"), "r") as exist_app_json_f:
                exist_app_json = json.load(exist_app_json_f)
            if exist_app_json["version_code"] == app_vcode:
                print(f"{Fore.YELLOW}Package '{app_name}' already installed. Do you want to install it again? (y/n): {Fore.RESET}")
                while True:
                    try:
                        check = str(input("> "))
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
                shutil.rmtree(app_dir)
            elif exist_app_json["version_code"] > app_vcode:
                print(f"{Fore.YELLOW}There is a newer version of package '{app_name}'. You couldn't downgrade it.{Fore.RESET}")
                input(f"{Fore.CYAN}(Press any key to continue.){Fore.RESET}")
                return 1
            elif exist_app_json["version_code"] < app_vcode:
                print(f"{Fore.YELLOW}There is an older version of package '{app_name}'. Biscuit will upgrade it.{Fore.RESET}")
                print(f"{Fore.CYAN}(Press any key to continue.){Fore.RESET}")
        shutil.copytree(temp_path, app_dir)
        # Install dependencies
        try:
            with open(os.path.join(app_dir, "info.json"), "r") as req_f:
                req_json = json.load(req_f)
                req_list = req_json.get("depends", [])
                # 处理 req_list 为空或只有空字符串的情况
                if not req_list or all(not req.strip() for req in req_list):
                    print(f"{Fore.GREEN}No dependencies needed to install.{Fore.RESET}")
                else:
                    print(f"{Fore.CYAN}Installing dependencies...{Fore.RESET}")
                    try:
                        for req in req_list:
                            req = req.strip().replace(" ", "")
                            if req:  # 确保 req 不是空字符串
                                subprocess.run([sys.executable, "-m", "pip", "install", req], check=True)
                        print(f"{Fore.GREEN}Dependencies installed successfully.{Fore.RESET}")
                    except subprocess.CalledProcessError as e:
                        print(f"{Fore.RED}An error occurred while installing dependencies: {e}{Fore.RESET}")
                        return 1
            req_f.close()
        except FileNotFoundError:
            print(f"{Fore.RED}File 'info.json' not found.{Fore.RESET}")
            return 1
        except json.JSONDecodeError:
            print(f"{Fore.RED}File 'info.json' format is incorrect.{Fore.RESET}")
            return 1
        # Add app to registry
        try:
            if not os.path.exists(os.path.join(qos_path, "data", "shell")):
                os.makedirs(os.path.join(qos_path, "data", "shell"))
            apps_json_path = os.path.join(qos_path, "data", "shell", "apps.json")
            if os.path.exists(apps_json_path):
                with open(apps_json_path, "r") as add_app_f:
                    add_app_config = json.load(add_app_f)
            else:
                add_app_config = {}
            add_app_config[app_name] = {
                "path": app_dir,
                "version": app_version,
                "version_code": app_vcode,
                "author": app_author,
                "description": app_desc,
                "category": app_category,
                "min_python_version": app_min,
                "target_python_version": app_tar,
                "comptb_os": app_comptb,
                "biscuit_version": app_bktver
            }
            with open(apps_json_path, "w") as add_app_f:
                json.dump(add_app_config, add_app_f, indent=4)
        except Exception as e:
            print(f"{Fore.RED}An error occurred during app registry update: {e}{Fore.RESET}")
            return 1
        # Clean up
        print(f"{Fore.GREEN}Package '{app_name}' has been successfully installed.{Fore.RESET}")
        return 0
    except Exception as e:
        print(f"{Fore.RED}An error occurred during installation: {e}{Fore.RESET}")
        return 1
    finally:
        shutil.rmtree(temp_path)

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
        with open("data/shell/apps.json", "r") as add_app_f:
            add_app_config = json.load(add_app_f)
        del add_app_config[app_name]
        with open("data/shell/apps.json", "w") as add_app_f:
            json.dump(add_app_config, add_app_f, indent=4)
        add_app_f.close()
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
            print(f"{Fore.CYAN}[Name]{Fore.RESET} - {Fore.GREEN}[Version]{Fore.RESET} - {Fore.BLUE}[Author]{Fore.RESET} - {Fore.YELLOW}[Category]{Fore.RESET} - {Fore.MAGENTA}[Description]{Fore.RESET}")
            for app_name in add_app_config:
                app_version = add_app_config[app_name]["version"]
                app_author = add_app_config[app_name]["author"]
                app_desc = add_app_config[app_name]["description"]
                app_category = add_app_config[app_name]["category"]
                print(f"{Fore.CYAN}{app_name}{Fore.RESET} - {Fore.GREEN}{app_version}{Fore.RESET} - {Fore.BLUE}{app_author}{Fore.RESET} - {Fore.YELLOW}{app_category}{Fore.RESET} - {Fore.MAGENTA}{app_desc}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.\n{Fore.CYAN}Looks like you haven't installed any packages yet.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    
def search(keyword):
    try:
        with open("data/shell/apps.json") as add_app_f:
            add_app_config = json.load(add_app_f)
        if len(add_app_config) == 0:
            print(f"{Fore.YELLOW}No packages installed.{Fore.RESET}")
            return 1
        else:
            print(f"{Fore.GREEN}Search results for '{keyword}':{Fore.RESET}")
            for app_name in add_app_config:
                if keyword.lower() in app_name.lower():
                    app_version = add_app_config[app_name]["version"]
                    print(f"{Fore.CYAN}{app_name}{Fore.RESET} - {Fore.GREEN}{app_version}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1

def get(app_name, app_version):
    try:
        with open(os.path.join("data", "config", "config.json"), "r") as config_f:
            config_json = json.load(config_f)
            repo_url = config_json["biscuit_repo"]
        repo_app_list = requests.get(f"{repo_url}/apps.json").json()
        if app_name in repo_app_list:
            app_category = repo_app_list[app_name]["category"]
        else:
            print(f"{Fore.RED}Invalid package name.{Fore.RESET}")
            return 1
        app_cg_url = f"{repo_url}/{app_category}/"
        app_pkg_info_response = requests.get(f"{app_cg_url}/package.json")
        app_pkg_info = app_pkg_info_response.json()
        if app_version == None:
            app_ver = app_pkg_info[app_name]["latest_version"]
        else:
            if app_version in app_pkg_info[app_name]["version"]:
                app_ver = str(app_version)
            else:
                print(f"{Fore.RED}Invalid package version. You can choose latest version: {app_pkg_info[app_name]['latest_version']}.{Fore.RESET}")
                return 1
        app_url = f"{app_cg_url}/{app_name}/{app_name + '_' + app_ver + '.qap'}"
        response = requests.get(app_url)
        if response.status_code == 200:
            down_path = os.path.join("data", "temp", "biscuit")
            os.makedirs(down_path, exist_ok=True)
            down_file = os.path.join(down_path, app_name + "_" + app_ver + ".qap")
            with open(down_file, "wb") as app_pkg_f:
                app_pkg_f.write(response.content)
            print(f"{Fore.GREEN}Package '{app_name}' downloaded successfully.{Fore.RESET}")
        else:
            print(f"{Fore.RED}Failed to download package '{app_name}'.{Fore.RESET}")
            return 1
        install(qos_path, os.path.join("data", "temp", "biscuit", app_name + "_" + app_ver + ".qap"))
    except FileNotFoundError:
        print(f"{Fore.RED}File 'config.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    
def mirror(repo_url):
    try:
        apps_json_url = f"{repo_url}/apps.json"
        apps_json_response = requests.get(apps_json_url)
        if apps_json_response.status_code != 200:
            print(f"{Fore.RED}Cannot connect to repository, status code: {apps_json_response.status_code}{Fore.RESET}")
            return 1
        data_dir = os.path.join("data")
        config_path = os.path.join(data_dir, "config", "config.json")
        with open(config_path, "r") as config_f:
            config_json = json.load(config_f)
        config_json["biscuit_repo"] = repo_url
        with open(config_path, "w") as config_f:
            json.dump(config_json, config_f, indent=4)
        print(f"{Fore.GREEN}Biscuit Package Repository has been set to '{repo_url}'。{Fore.RESET}")
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'config.json' not found.{Fore.RESET}")
        return 1
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Request error: {e}{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
