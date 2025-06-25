"""
# QOS - Quarter Operation System
@ Author: ElofHew aka Dan_Evan
@ Version: Alpha 0.1
@ Date: 2025-06-22
@ License: GNU General Public License v3.0
@ Description: A Professional Fake-OS Powered by Python3.
"""
# Initialize QOS Core Modules
import system.core.qoscore as qoscore
# Check Config Files in data
qoscore.check_more_dir()
qoscore.check_config()
# Check OS
qoscore.check_os()
# Check QOS Path
qoscore.check_path()
# Import Python Standard Modules
try:
    import sys
    import time
    import json
    import pathlib
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
    import system.core.cmds as cmds
    import system.core.login as login
    import system.core.options as options
except ImportError as e:
    print(f"Error: {e}")
    print("Import QOS Core Modules Failed.")
    sys.exit(0)
# Import QOS Apps & Opts
try:
    import system.opts.komshell as komshell
except ImportError as e:
    print(f"Error: {e}")
    print("Import QOS Apps & Opts Failed.")
    sys.exit(0)
# Initialize Colorama
colorama.init(autoreset=True)
# Clear Console Screen
cmds.clear()

# Load Config Files
with open("data/config/config.json", "r") as qos_config_file:
    config_file = json.load(qos_config_file)
    os_type = config_file["os_type"]
    qos_logo_path = config_file["qos_logo_path"]
    version = config_file["version"]
    startup_title = config_file["startup_title"]
    oobe_condition = config_file["oobe"]

# Boot Kom Shell
def boot_shell(username):
    cmds.clear()
    komshell.shell(username)

# second_boot function
def second_boot():
    username = login.qos_login()
    print(" " + colorama.Fore.LIGHTBLUE_EX + str(startup_title) + colorama.Style.RESET_ALL + " ")
    time.sleep(1)
    print(f"\n{colorama.Fore.GREEN}QOS will start in 3 seconds...{colorama.Style.RESET_ALL}")
    time.sleep(3)
    if username:
        boot_shell(username)
    else:
        print(f"{colorama.Fore.RED}Error: Some wrong with Login Manager!{colorama.Style.RESET_ALL}")
        sys.exit(0)

# main function
def main():
    qos_logo = pathlib.Path(qos_logo_path)
    qos_version = str(version)
    print(f"{colorama.Style.DIM}Quarter Operation System{colorama.Style.RESET_ALL}\n")
    print(f"{colorama.Fore.MAGENTA}{colorama.Style.BRIGHT}Version: {qos_version}{colorama.Style.RESET_ALL}\n")
    options.cat(qos_logo)
    print("GitHub Repo: https://github.com/ElofHew/QOS")
    print("Oak Studio: https://t.me/oakstd")
    print("")
    time.sleep(1)

# Start QOS
if __name__ == "__main__":
    main()
    if oobe_condition:
        import system.opts.oobe as oobe
        oobe.OOBE().main()
        del oobe
    else:
        pass
    second_boot()