# QOS Boot System Core

import os
import json
import platform

def check_os():
    with open("config/config.json", "r") as qos_config_file:
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
    with open("config/config.json", "w") as qos_config_file:
        json.dump(config, qos_config_file, indent=4)

def check_path():
    qos_path = os.getcwd()
    with open("config/config.json", "r") as qos_config_file:
        config_data = json.load(qos_config_file)
    json_path = config_data.get("qos_path", "")
    if json_path != qos_path:
        config_data["qos_path"] = qos_path
        with open("config/config.json", "w") as qos_config_file:
            json.dump(config_data, qos_config_file, indent=4)
    else:
        pass