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
import platform # 用于获取操作系统类型
from colorama import init, Fore, Back, Style  # 用于控制输出颜色

init(autoreset=True)  # 初始化颜色模块

try:
    with open(os.path.join("data", "config", "config.json"), "r") as f:
        config = json.load(f)
        qos_path = config.get("qos_path", os.getcwd())
        os_type = config.get("os_type", platform.system().lower())
    python_ver = platform.python_version()
    biscuit_ver = "1.0"
except FileNotFoundError:
    print(f"{Fore.RED}Config file not found.{Fore.RESET}")
    sys.exit(19)
except json.JSONDecodeError:
    print(f"{Fore.RED}Config file is not a valid JSON file.{Fore.RESET}")
    sys.exit(19)

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
                    list_apps(args[1:])
                case "search":
                    search(args[1:])
                case "get":
                    get(args[1:])
                case "install":
                    install(working_path, args[1:])
                case "remove":
                    remove(args[1:])
                case "mirror":
                    mirror(args[1:])
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
    print(f"{Fore.LIGHTGREEN_EX}  % Biscuit Package Manager %  {Style.RESET_ALL}")
    print(f"{Fore.LIGHTGREEN_EX}==============================={Style.RESET_ALL}")
    print(f"{Fore.CYAN}list (arg)   - List all installed packages{Style.RESET_ALL}")
    print(f"{Fore.CYAN}mirror <url> - Set a mirror for package repository{Style.RESET_ALL}")
    print(f"{Fore.CYAN}install <package_path>  - Install a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}remove <package>        - Remove a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}search <arg> <keyword>  - Search a package{Style.RESET_ALL}")
    print(f"{Fore.CYAN}get <package> (version) - Get package from online repository{Style.RESET_ALL}")

def install(working_path, aargs):
    __usage__ = "Usage: biscuit install <package_path>"
    if not aargs or len(aargs) > 1:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    pkg_path = aargs[0]
    # Main
    ins_pkg_path = os.path.join(working_path, pkg_path)
    temp_path = os.path.join(qos_path, "data", "temp")
    sysapp_path = os.path.join(qos_path, "system", "apps")
    apps_path = os.path.join(qos_path, "data", "apps")

    try:
        # Check if package exists
        if not os.path.exists(ins_pkg_path):
            if not os.path.exists(os.path.abspath(pkg_path)):
                print(f"{Fore.RED}Package not found.{Fore.RESET}")
            return 1
        if not os.path.exists(temp_path):
            os.makedirs(temp_path)
        if not os.path.exists(apps_path):
            os.makedirs(apps_path)

        # Extract package
        print(f"{Fore.CYAN}Installing package...{Fore.RESET}")
        extra_path = os.path.join(temp_path, "package")
        if os.path.exists(extra_path):
            shutil.rmtree(extra_path)
        os.makedirs(extra_path)
        with zipfile.ZipFile(ins_pkg_path, "r") as zip_ref:
            zip_ref.extractall(extra_path)
    except FileNotFoundError:
        print(f"{Fore.RED}Package file not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during package check: {e}{Fore.RESET}")
        return 1
    
    # Get app name and version
    try:
        with open(os.path.join(extra_path, "info.json"), "r") as app_json_f:
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
        shutil.rmtree(extra_path)
        return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'info.json' not found.{Fore.RESET}")
        shutil.rmtree(extra_path)
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        shutil.rmtree(extra_path)
        return 1

    # Install app
    # Check the most compatible items
    try:
        if app_comptb.lower() != os_type.lower():
            print(f"{Fore.YELLOW}WARN: This app may be not compatible with your system.{Fore.RESET}")
        if int(app_min.split(".")[1]) > int(python_ver.split(".")[1]):
            print(f"{Fore.YELLOW}WARN: This app requires Python {app_min} or higher, but your Python version is {python_ver}.{Fore.RESET}")
        if int(app_tar.split(".")[1]) != int(python_ver.split(".")[1]):
            print(f"{Fore.YELLOW}WARN: This app may not work properly with your Python version.{Fore.RESET}")
        if app_bktver != biscuit_ver:
            print(f"{Fore.YELLOW}WARN: This app may not work properly with your Biscuit version.{Fore.RESET}")
    except Exception as e:
        print(f"{Fore.RED}An error occurred while checking compatibility: {e}{Fore.RESET}")
        return 1

    # Check if app already exists
    try:
        sysapp_dir = os.path.join(sysapp_path, app_name)
        app_dir = os.path.join(apps_path, app_name)
        if os.path.exists(sysapp_dir):
            print(f"{Fore.YELLOW}Package '{app_name}' is already installed as a system app.{Fore.RESET}")
            return 1
        if os.path.exists(app_dir):
            with open(os.path.join(app_dir, "info.json"), "r") as exist_app_json_f:
                exist_app_json = json.load(exist_app_json_f)
            # Same version, reinstall ask
            if exist_app_json["version_code"] == app_vcode:
                print(f"{Fore.YELLOW}Package '{app_name}' already installed. Do you want to install it again? (y/n){Fore.RESET}")
            # Higher version, downgrade ask
            elif exist_app_json["version_code"] > app_vcode:
                print(f"{Fore.YELLOW}There is a newer version of package '{app_name}'. Would you like to downgrade it? (y/n){Fore.RESET}")
            # Lower version, upgrade ask
            elif exist_app_json["version_code"] < app_vcode:
                print(f"{Fore.YELLOW}There is an older version of package '{app_name}'. Would you like to upgrade it? (y/n){Fore.RESET}")
            else:
                print(f"{Fore.RED}An error occurred while checking package '{app_name}'.{Fore.RESET}")
                return 1
            while True:
                check = str(input("> "))
                if check == "y" or check == "Y":
                    break
                elif check == "n" or check == "N":
                    print(Fore.RED + "Operation cancelled." + Fore.RESET)
                    return 0
                else:
                    print(Fore.RED + "Invalid input. Please enter 'y' or 'n'." + Fore.RESET)
                    continue
            # Remove old app directory
            shutil.rmtree(app_dir)
        # Copy app files to app directory
        shutil.copytree(extra_path, app_dir)
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        return 0
    except FileExistsError:
        print(f"{Fore.RED}Directory '{app_name}' already exists.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during package installation: {e}{Fore.RESET}")
        return 1

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
            installed_packages = subprocess.check_output([subprocess.sys.executable, '-m', 'pip', 'freeze']).decode('utf-8').split('\n')
            installed_packages = {pkg.split('==')[0].strip().lower() for pkg in installed_packages if pkg}
            # 获取已安装的包
            try:
                req_index = 1
                for req in req_list:
                    req = req.strip().replace(" ", "").lower()  # 将包名转换为小写以便比较
                    if req:  # 确保 req 不是空字符串
                        if req in installed_packages:  # 检查包是否已经安装
                            print(f"{Fore.CYAN}Module {req_index}: {Fore.YELLOW}{req}{Fore.CYAN} is already installed.{Fore.RESET}")
                        else:
                            print(f"{Fore.CYAN}Installing Module {req_index}: {Fore.YELLOW}{req}{Fore.CYAN}...{Fore.RESET}")
                            subprocess.run([subprocess.sys.executable, "-m", "pip", "install", req], check=True)
                            print(f"{Fore.GREEN}Module {req_index}: {Fore.YELLOW}{req}{Fore.GREEN} installed successfully.{Fore.RESET}")
                        req_index += 1
                print(f"{Fore.GREEN}All dependencies installed successfully.{Fore.RESET}")
            except subprocess.CalledProcessError as e:
                print(f"{Fore.RED}An error occurred while installing dependencies: {e}{Fore.RESET}")
                return 1
    except FileNotFoundError:
        print(f"{Fore.RED}File 'info.json' in app directory not found.{Fore.RESET}")
        return 1
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        return 0
    except json.JSONDecodeError:
        print(f"{Fore.RED}File 'info.json' format is incorrect.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
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
            "path": app_dir if not app_dir.startswith(qos_path) else app_dir.replace(qos_path, "."),
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
        print(f"{Fore.GREEN}Package '{app_name}' has been successfully installed.{Fore.RESET}")
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during app registry update: {e}{Fore.RESET}")
        return 1
    
    # Clean up
    try:
        shutil.rmtree(extra_path)
        return 0
    except Exception as e:
        print(f"{Fore.RED}An error occurred during cleanup: {e}{Fore.RESET}")
        return 1

def remove(aargs):
    __usage__ = "Usage: biscuit remove <package>"
    if not aargs or len(aargs) > 1:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    app_name = aargs[0]
    # Check if app exists in registry
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
            return 0

    # Check app registry
    try:
        with open("data/shell/apps.json", "r") as add_app_f:
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
    except FileNotFoundError:
        print(f"{Fore.RED}Directory '{app_name}' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred during removal: {e}{Fore.RESET}")
        return 1

def list_apps(aargs):
    __usage__ = "Usage: biscuit list (no args)"
    if aargs:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    # Main
    try:
        with open(os.path.join(qos_path, "system", "shell", "apps.json")) as sys_app_f:
            sys_app_config = json.load(sys_app_f)
        if os.path.exists(os.path.join(qos_path, "data", "shell", "apps.json")):
            with open(os.path.join(qos_path, "data", "shell", "apps.json")) as add_app_f:
                add_app_config = json.load(add_app_f)
        else:
            add_app_config = {}
        if len(add_app_config) == 0 and len(sys_app_config) == 0:
            print(f"{Fore.YELLOW}No packages installed.{Fore.RESET}")
            return 1
        else:
            all_app_list = {**sys_app_config, **add_app_config}
            print(f"{Fore.GREEN}Installed packages:{Fore.RESET}")
            print(f"{Fore.CYAN}[Name]{Fore.RESET} - {Fore.GREEN}[Version]{Fore.RESET} - {Fore.LIGHTBLUE_EX}[Author]{Fore.RESET} - {Fore.YELLOW}[Category]{Fore.RESET} - {Fore.LIGHTMAGENTA_EX}[Description]{Style.RESET_ALL}")
            for app_name in all_app_list:
                app_version = all_app_list[app_name]["version"]
                app_author = all_app_list[app_name]["author"]
                app_desc = all_app_list[app_name]["description"]
                app_category = all_app_list[app_name]["category"]
                print(f"{Fore.CYAN}{app_name}{Fore.RESET} - {Fore.GREEN}{app_version}{Fore.RESET} - {Fore.LIGHTBLUE_EX}{app_author}{Fore.RESET} - {Fore.YELLOW}{app_category}{Fore.RESET} - {Fore.LIGHTMAGENTA_EX}{app_desc}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.\n{Fore.CYAN}Looks like you haven't installed any packages yet.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1

def search(aargs):
    __usage__ = "Usage: biscuit search <keyword>"
    if not aargs or len(aargs) > 1:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    keyword = aargs[0]
    # Main
    try:
        with open("system/shell/apps.json") as sys_app_f:
            sys_app_config = json.load(sys_app_f)
        if os.path.exists("data/shell/apps.json"):
            with open("data/shell/apps.json") as add_app_f:
                add_app_config = json.load(add_app_f)
        else:
            add_app_config = {}
        if len(add_app_config) == 0 and len(sys_app_config) == 0:
            print(f"{Fore.YELLOW}No packages installed.{Fore.RESET}")
            return 1
        else:
            all_app_list = {**sys_app_config, **add_app_config}
            print(f"{Fore.GREEN}Search results for '{keyword}':{Fore.RESET}")
            for app_name in all_app_list:
                if keyword.lower() in app_name.lower():
                    app_version = all_app_list[app_name]["version"]
                    print(f"{Fore.CYAN}{app_name}{Fore.RESET} - {Fore.GREEN}{app_version}{Fore.RESET}")
            return 0
    except FileNotFoundError:
        print(f"{Fore.RED}File 'apps.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1

def get(aargs):
    __usage__ = "Usage: biscuit get <package> [version]"
    if not aargs or len(aargs) > 2:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    if len(aargs) == 1:
        app_name = aargs[0]
        app_version = None
    elif len(aargs) == 2:
        app_name = aargs[0]
        app_version = aargs[1]
    
    # Main
    # 获取软件源URL
    try:
        with open(os.path.join("data", "config", "config.json"), "r") as config_f:
            config_json = json.load(config_f)
            repo_url = config_json["biscuit_repo"]
    except FileNotFoundError:
        print(f"{Fore.RED}File 'config.json' not found.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Fore.RESET}")
        return 1
    # 查找软件包信息
    try:
        response = requests.get(f"{repo_url}/apps.json", timeout=10)
        response.raise_for_status()
        repo_app_list = response.json()
        if app_name in repo_app_list:
            app_category = repo_app_list[app_name]["category"]
        else:
            print(f"{Fore.RED}Invalid package name.{Fore.RESET}")
            return 1
        app_cg_url = f"{repo_url}/{app_category}/"
        response = requests.get(f"{app_cg_url}/package.json", timeout=10)
        response.raise_for_status()
        app_pkg_info = response.json()
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        return 0
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}The request to get request timed out.{Fore.RESET}")
        return 1
    except requests.exceptions.HTTPError:
        print(f"{Fore.RED}HTTP error occurred while fetching apps.json.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred while fetching apps.json: {e}{Fore.RESET}")
        return 1
    if app_version is None:
        app_ver = app_pkg_info[app_name]["latest_version"]
    else:
        if app_version in app_pkg_info[app_name]["version"]:
            app_ver = str(app_version)
        else:
            print(f"{Fore.RED}Invalid package version. You can choose latest version: {app_pkg_info[app_name]['latest_version']}.{Fore.RESET}")
            return 1
    # 下载qap软件包
    try:
        app_url = f"{app_cg_url}/{app_name}/{app_name + '_' + app_ver + '.qap'}"
        start_time = time.time()
        print(f"{Fore.CYAN}Downloading package '{app_name}'...{Fore.RESET}")
        response = requests.get(app_url, timeout=10, stream=True)
        response.raise_for_status()
        down_path = os.path.join("data", "temp", "biscuit")
        os.makedirs(down_path, exist_ok=True)
        down_file = os.path.join(down_path, app_name + "_" + app_ver + ".qap")
        with open(down_file, "wb") as app_pkg_f:
            for chunk in response.iter_content(chunk_size=8192):
                app_pkg_f.write(chunk)
        end_time = time.time()
        print(f"{Fore.GREEN}Package '{app_name}' downloaded successfully in {end_time - start_time:.2f} seconds.{Fore.RESET}")
    except KeyboardInterrupt:
        print(Fore.RED + "Operation cancelled." + Fore.RESET)
        shutil.rmtree(down_path)
        return 0
    except requests.exceptions.Timeout:
        print(f"{Fore.RED}The request to download package timed out.{Fore.RESET}")
        return 1
    except requests.exceptions.HTTPError:
        print(f"{Fore.RED}HTTP error occurred while downloading package.{Fore.RESET}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred while downloading package: {e}{Fore.RESET}")
        return 1
    # 调用安装qap包
    try:
        ins_ret = install(qos_path, [down_file])
        if not ins_ret == 0:
            print(f"{Fore.RED}Failed to install package.{Fore.RESET}")
            return 1
    except Exception as e:
        print(f"{Fore.RED}An error occurred while installing package: {e}{Fore.RESET}")
        return 1
    finally:
        os.remove(down_file)
    
def mirror(aargs):
    __usage__ = "Usage: biscuit mirror <repository_url>"
    if not aargs or len(aargs) > 1:
        print(f"{Fore.YELLOW}{__usage__}{Fore.RESET}")
        return 1
    if aargs[0]:
        repo_url = aargs[0]
    else:
        print(f"{Fore.YELLOW}No repository URL provided.{Fore.RESET}")
        return 1
    # Main
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
