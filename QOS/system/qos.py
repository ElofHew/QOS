"""
# QOS - Quarter Operation System
@ Author: ElofHew aka Dan_Evan
@ Version: Alpha 0.1
@ Date: 2025-06-22
@ License: GNU General Public License v3.0
@ Description: A Professional Fake-OS Powered by Python3.
"""
# Import Python Standard Modules
try:
    import sys
    import time
    import json
except ImportError as e:
    print(f"Error: {e}")
    print("Import Python Standard Modules Failed.")
    sys.exit(0)
# Import Third-party Modules
try:
    import colorama
except ImportError as e:
    print(f"Error: {e}")
    print("Import Trird-party Modules Failed.")
    sys.exit(0)
# Import QOS Core Modules
try:
    import core.login as login
    import core.qoscore as qoscore
    import core.options as options
except ImportError as e:
    print(f"Error: {e}")
    print("Import QOS Core Modules Failed.")
    sys.exit(0)
# Import QOS Apps & Opts
try:
    import opts.komshell as komshell
except ImportError as e:
    print(f"Error: {e}")
    print("Import QOS Apps & Opts Failed.")
    sys.exit(0)
# Initialize Colorama
colorama.init(autoreset=True)
# Clear Console Screen
options.clear()
# Check OS and Load Config
qoscore.check_os()

# Load Config Files
with open("config/config.json", "r") as qos_config_file:
    config_file = json.load(qos_config_file)
    os_type = config_file["os_type"]
    qos_logo_path = config_file["qos_logo_path"]
    version = config_file["version"]
    startup_title = config_file["startup_title"]

# main function
def main():
    qos_logo = str(qos_logo_path)
    qos_version = str(version)
    qoscore.check_os()
    print(f"{colorama.Style.DIM}Quarter Operation System{colorama.Style.RESET_ALL}")
    print("")
    print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}Version: {qos_version}{colorama.Style.RESET_ALL}")
    print("")
    options.cat(qos_logo)
    print("")
    print("GitHub Repo: https://github.com/ElofHew/QOS")
    print("Oak Studio: https://t.me/oakstd")
    print("")
    time.sleep(1)

# Start QOS
if __name__ == "__main__":
    main()
    qoscore.check_path()
    username = login.qos_login()
    print(" " + colorama.Fore.LIGHTBLUE_EX + str(startup_title) + colorama.Style.RESET_ALL + " ")
    time.sleep(1)
    print(f"\n{colorama.Fore.GREEN}QOS will start in 3 seconds...{colorama.Style.RESET_ALL}")
    time.sleep(3)
    options.clear()
    if username:
        komshell.shell(username)
