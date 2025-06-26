# QOS - Quarter Operation System - Main Code
"""
# QOS - Quarter Operation System
@ Author: ElofHew aka Dan_Evan
@ Version: Alpha 0.1
@ Date: 2025-06-22
@ License: GNU General Public License v3.0
@ Description: A Professional Fake-OS Powered by Python3.
"""

# Check qos.py in path
try:
    import os,sys
    now_path = os.getcwd()
    if not os.path.isfile(os.path.join(now_path, 'qos.py')):
        if now_path.endswith('QOS'):
            raise FileNotFoundError("No such file: 'qos.py' in this directory.\n(Maybe you should 'cd QOS' at this directory first?)")
        else:
            raise FileNotFoundError("No such file: 'qos.py' in this directory.")
    if not os.path.isdir(os.path.join(now_path, 'system')):
        if now_path.endswith('QOS'):
            raise NotADirectoryError("No such directory:'system' in this directory.\n(Maybe you should 'cd QOS' at this directory first?)")
        else:
            raise NotADirectoryError("No such directory:'system' in this directory.")
except FileNotFoundError as e:
    print(e)
    sys.exit(0)
except NotADirectoryError as e:
    print(e)
    sys.exit(0)
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(0)
# (20250625)稍微解释一下：
# 上面会检测你当前所在目录是否是QOS所在目录
# 如果不是则不允许你启动，直接sys.exit(0)退出
# 另外如果当前目录最后是"QOS"时，提示你再次cd QOS

# Initialize QOS Core Modules （导入核心工作模块）
try:
    import system.core.qoscore as qoscore
except ImportError as e:
    print(f"Error: {e}")
    print("Start QOS Core Services Failed.")
    sys.exit(0)

# Check Config Files in data （先检查数据目录是否完好，再检查数据目录的配置文件）
qoscore.check_more_dir()
qoscore.check_config_dir()
qoscore.check_home_dir()

# Check OS （检查你用的操作系统是啥）
qoscore.check_os()

# Check QOS Path （识别你存放QOS的绝对路径，再存入配置文件）
qoscore.check_path()

# Import Modules （开始导入模块了,先把QOS系统所有需要用到的模块导入，检查是否存在，再把用不到的释放掉）
try:
    # Import Python Standard Modules （标准库）
    import os
    import sys
    import time
    import json
    import base64
    import shutil
    import zipfile
    import pathlib
    import getpass
    import platform
    import subprocess
    # Import Trird-Party Modules （三方库）
    from colorama import init as cinit
    from colorama import Fore, Style, Back
    # Import QOS Cores （本地库）
    import system.core.cmds as cmds
    import system.core.login as login
    import system.core.options as options
    import system.core.qoscore as qoscore
    # Import QOS Applications （本地应用）
    import system.opts.oobe as oobe
    import system.opts.komshell as komshell
    import system.apps.settings as settings
except ImportError as e:
    print(f"Error: {e}")
    print("Import Modules or QOS Core Failed.")
    sys.exit(0)

try:
    # Delete Unused Modules （删除没用的模块）
    del os, sys, platform, shutil, subprocess, zipfile, base64, getpass, oobe, settings
except NameError as e:
    print(f"{Style.BRIGHT}{Fore.YELLOW}WARNING: Some modules are not found.{Style.RESET_ALL}")

# Initialize Colorama （初始化colorama模块）
cinit(autoreset=True)

# Clear Console Screen （清屏）
cmds.clear()

# Load Config Files （加载配置文件）
with open("data/config/config.json", "r") as qos_config_file:
    config_file = json.load(qos_config_file)
    os_type = config_file["os_type"]
    qos_logo_path = config_file["qos_logo_path"]
    version = config_file["version"]
    startup_title = config_file["startup_title"]
    oobe_condition = config_file["oobe"]

# Boot Kom Shell （启动Kom Shell）
def boot_shell(username):
    cmds.clear()
    komshell.shell(username)

# second_boot function （二次启动）
def second_boot():
    print(Style.DIM + Fore.YELLOW + "Quarter OS Login Manager - " + version + Style.RESET_ALL + "\n")
    try:
        username = login.qos_login()
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        sys.exit(0)
    print(" " + Fore.LIGHTBLUE_EX + str(startup_title) + Style.RESET_ALL + " ")
    time.sleep(1)
    print(f"\n{Fore.GREEN}QOS will start in 3 seconds...{Style.RESET_ALL}")
    time.sleep(3)
    if username:
        boot_shell(username)
    else:
        print(f"{Fore.RED}Error: Some wrong with Login Manager!{Style.RESET_ALL}")
        sys.exit(0)

# main function （主函数）
def main():
    qos_logo = pathlib.Path(qos_logo_path)
    qos_version = str(version)
    print(f"{Style.DIM}Quarter Operation System{Style.RESET_ALL}\n")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}Version: {qos_version}{Style.RESET_ALL}\n")
    options.cat(qos_logo)
    print("GitHub Repo: https://github.com/ElofHew/QOS")
    print("Oak Studio: https://t.me/oakstd")
    print("")
    time.sleep(1)

# Start QOS （启动QOS）
if __name__ == "__main__":
    main()
    if oobe_condition:
        import system.opts.oobe as oobe
        oobe.OOBE().main()
        del oobe
    else:
        pass
    second_boot()