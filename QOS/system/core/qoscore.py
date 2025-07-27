# QOS Boot System Core

import os
import json
import platform
import pathlib

def check_home_dir():
    user_file_path = pathlib.Path("data/config/users.json")
    if not user_file_path.exists():
        print("users.json not found")
        return False
    # Read User Data from users.json
    with open(user_file_path, "r") as qos_user_file:
        config = json.load(qos_user_file)
    # Initialize Conditon of home_created
    home_created = False
    # Check Home Directory, if not exist, create it
    if not os.path.exists("home/"):
        os.mkdir("home/")
        home_created = True
    # Read User Data from users.json
    user_index = 1 # Initialize User Index
    while f"user{user_index}" in config:
        user_data = config[f"user{user_index}"]
        # Check Username in User Data
        if "username" in user_data:
            username = user_data["username"]
            user_home_path = f"home/{username}"
            # Check Home Directory for User, if not exist, create it
            if not os.path.exists(user_home_path):
                os.mkdir(user_home_path)
            else:
                pass
        else:
            pass
        user_index += 1
    return home_created


def check_config_dir():
    try:
        conf_created = False
        data_config_dir = os.path.join(os.getcwd(), "data", "config")
        if not os.path.exists(os.path.join(data_config_dir, "config.json")):
            qos_config_data = {
                "name": "Quarter OS",
                "version": "Alpha 0.2.2",
                "vercode": "0220",
                "os_type": None,
                "qos_path": None,
                "startup_title": "QOS Alpha 0.2.2",
                "qos_startup_logo": "1",
                "startup_timeout": 3,
                "system_name": None,
                "oobe": True,
                "biscuit_repo": "https://os.drevan.xyz/biscuit/repo/",
                "qos_edition": None,
                "activate_code": None,
                "activate_statue": False,
                "ad_statue": True,
                "data_path": None,
                "home_path": None,
                "system_path": None,
                "shell_theme": "default",
                "unknown_command_progression": False,
                "last_login": None,
                "last_login_time": None
            }
            with open(os.path.join(data_config_dir, "config.json"), "w") as qos_config_file:
                json.dump(qos_config_data, qos_config_file, indent=4)
            conf_created = True
        if not os.path.exists(os.path.join(data_config_dir, "users.json")):
            qos_users_data = {
                "user1": {
                    "username": "root",
                    "password": "MTIzNDU2"
                },
                "user2": {
                    "username": "admin",
                    "password": "MTIzNDU2"
                },
                "user3": {
                    "username": "guest",
                    "password": None
                }
            }
            with open(os.path.join(data_config_dir, "users.json"), "w") as qos_users_file:
                json.dump(qos_users_data, qos_users_file, indent=4)
            conf_created = True
        return conf_created
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_more_dir():
    try:
        dir_created = False
        if not os.path.exists("data/"):
            os.mkdir("data/")
            dir_created = True
        if not os.path.exists("data/config/"):
            os.mkdir("data/config/")
            dir_created = True
        if not os.path.exists("data/apps/"):
            os.mkdir("data/apps/")
            dir_created = True
        if not os.path.exists("data/temp/"):
            os.mkdir("data/temp/")
            dir_created = True
        if not os.path.exists("home/"):
            os.mkdir("home/")
            dir_created = True
        return dir_created
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_full_json():
    default_config = {
        "name": "Quarter OS",
        "version": "Alpha 0.2.2",
        "vercode": "0220",
        "os_type": None,
        "qos_path": None,
        "startup_title": "QOS Alpha 0.2.2",
        "qos_startup_logo": "1",
        "startup_timeout": 3,
        "system_name": None,
        "oobe": True,
        "biscuit_repo": "https://os.drevan.xyz/biscuit/repo/",
        "qos_edition": None,
        "activate_code": None,
        "activate_statue": False,
        "ad_statue": True,
        "data_path": None,
        "home_path": None,
        "system_path": None,
        "shell_theme": "default",
        "unknown_command_progression": False,
        "last_login": None,
        "last_login_time": None
    }
    config_path = "data/config/config.json"
    try:
        # 检查文件是否存在，如果不存在则创建并写入默认配置
        if not os.path.exists(config_path):
            with open(config_path, "w") as qos_config_file:
                json.dump(default_config, qos_config_file, indent=4)
            return True
        with open(config_path, "r+") as qos_config_file:  # 修正这里
            config_data = json.load(qos_config_file)
            modified = False
            # 检查并更新默认值
            for key, value in default_config.items():
                if key not in config_data:
                    config_data[key] = value
                    modified = True
            # 只有在配置有修改时才写入文件
            if modified:
                qos_config_file.seek(0)  # 将文件指针移到文件开头
                json.dump(config_data, qos_config_file, indent=4)
                qos_config_file.truncate()  # 截断文件以去除多余内容
            return True
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_os_path():
    try:
        with open("data/config/config.json", "r") as qos_config_file:
            config_data = json.load(qos_config_file)
        os_mapping = {
            "windows": "windows",
            "linux": "linux",
            "darwin": "macos"
        }
        # div
        detected_os = platform.system().lower()
        qos_path = os.getcwd()
        data_path = os.path.join(qos_path, "data")
        home_path = os.path.join(qos_path, "home")
        system_path = os.path.join(qos_path, "system")
        # div
        json_os_type = config_data.get("os_type", "")
        json_qos_path = config_data.get("qos_path", "")
        json_data_path = config_data.get("data_path", "")
        json_home_path = config_data.get("home_path", "")
        json_system_path = config_data.get("system_path", "")
        if json_os_type != detected_os:
            config_data["os_type"] = detected_os
        if json_qos_path != qos_path:
            config_data["qos_path"] = qos_path
        if json_data_path != data_path:
            config_data["data_path"] = data_path
        if json_home_path != home_path:
            config_data["home_path"] = home_path
        if json_system_path != system_path:
            config_data["system_path"] = system_path
        with open("data/config/config.json", "w") as qos_config_file:
            json.dump(config_data, qos_config_file, indent=4)
        return detected_os, qos_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return "unknown", os.getcwd()
