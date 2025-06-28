# QOS Boot System Core

import os
import sys
import shutil
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
        system_config_dir = os.path.join(os.getcwd(), "system", "config")
        if not os.path.exists(os.path.join(data_config_dir, "config.json")):
            shutil.copyfile(os.path.join(system_config_dir, "config.json"), os.path.join(data_config_dir, "config.json"))
            conf_created = True
        if not os.path.exists(os.path.join(data_config_dir, "users.json")):
            shutil.copyfile(os.path.join(system_config_dir, "users.json"), os.path.join(data_config_dir, "users.json"))
            conf_created = True
        if not os.path.exists(os.path.join(data_config_dir, "shell.json")):
            shutil.copyfile(os.path.join(system_config_dir, "shell.json"), os.path.join(data_config_dir, "shell.json"))
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
        if not os.path.exists("data/etc/"):
            os.mkdir("data/etc/")
            dir_created = True
        if not os.path.exists("home/"):
            os.mkdir("home/")
            dir_created = True
        return dir_created
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def check_os():
    with open("data/config/config.json", "r") as qos_config_file:
        config = json.load(qos_config_file)
    detected_os = platform.system().lower()
    os_mapping = {
        "windows": "windows",
        "linux": "linux",
        "darwin": "macos"
    }
    config_os_type = os_mapping.get(detected_os, "unknown")
    if config.get("os_type", "").lower() != config_os_type:
        config["os_type"] = config_os_type
    with open("data/config/config.json", "w") as qos_config_file:
        json.dump(config, qos_config_file, indent=4)
    return config_os_type

def check_path():
    qos_path = os.getcwd()
    data_path = os.path.join(qos_path, "data")
    home_path = os.path.join(qos_path, "home")
    with open("data/config/config.json", "r") as qos_config_file:
        config_data = json.load(qos_config_file)
    json_qos_path = config_data.get("qos_path", "")
    json_data_path = config_data.get("data_path", "")
    json_home_path = config_data.get("home_path", "")
    if json_qos_path != qos_path or json_data_path != data_path or json_home_path != home_path:
        config_data["qos_path"] = qos_path
        config_data["data_path"] = data_path
        config_data["home_path"] = home_path
        with open("data/config/config.json", "w") as qos_config_file:
            json.dump(config_data, qos_config_file, indent=4)
    else:
        pass
