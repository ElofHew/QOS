# QOS Boot System Core

import os
import json
import platform

import system.core.cmds as cmds

def check_config():
    try:
        conf_created = False
        if not os.path.exists("data/config/config.json"):
            cmds.cp("system/config/config.json", "data/config/")
            conf_created = True
        if not os.path.exists("data/config/users.json"):
            cmds.cp("system/config/users.json", "data/config/")
            conf_created = True
        if not os.path.exists("data/config/shell.json"):
            cmds.cp("system/config/shell.json", "data/config/")
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