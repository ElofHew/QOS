# QOS - Quarter Operation System - Main Code
"""
# QOS - Quarter Operation System
@ Author: ElofHew aka Dan_Evan
@ Version: Alpha 0.2
@ Date: 2025-06-29
@ License: GNU General Public License v3.0
@ Description: A Professional Fake-OS Powered by Python3.
"""

try:
    # Import Required Modules （导入所需模块）
    import os
    import sys
    import json
    import pathlib
    from colorama import Fore, Style, init
except ImportError as e:
    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    sys.exit(0)

# Boot Check （启动检查）:
try:
    # Initialize QOS Core Modules （初始化QOS核心模块）
    import system.core.qoscore as qoscore
    # Check Config Files in data （先检查数据目录是否完好，再检查数据目录的配置文件）
    qoscore.check_more_dir()
    qoscore.check_config_dir()
    # Check OS （检查你用的操作系统是啥）
    qoscore.check_os()
    # Check QOS Path （识别你存放QOS的绝对路径，再存入配置文件）
    qoscore.check_path()
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    sys.exit(0)

try:
    # Initialize QOS Modules （初始化QOS模块）
    import system.core.cmds as cmds
    import system.core.options as options
except Exception as e:
    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    sys.exit(0)

# Initialize Colorama （初始化colorama模块）
init(autoreset=True)

# Clear Console Screen （清屏）
options.clear()


# Load Config Files （加载配置文件）
with open("data/config/config.json", "r") as qos_config_file:
    config_file = json.load(qos_config_file)
    os_type = config_file["os_type"]
    qos_startup_logo = config_file["qos_startup_logo"]
    version = config_file["version"]
    startup_title = config_file["startup_title"]
    oobe_condition = config_file["oobe"]

# Start QOS （启动QOS）
def main():
    try:
        qos_logo = os.path.join("system", "etc", "logo", qos_startup_logo + ".txt")
        qos_startup = pathlib.Path("system/etc/startup.txt")
        qos_version = str(version)
        print(f"{Style.DIM}Quarter Operation System{Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Version: {qos_version}{Style.RESET_ALL}\n")
        options.cat(qos_logo)
        options.cat(qos_startup)
        print("")
        options.get_ads()
        if oobe_condition:
            import system.opts.oobe as oobe
            retrun_code = oobe.OOBE().main()
            del oobe
        import system.opts.loginman as loginman
        username = loginman.main(version, startup_title)
        del loginman
        if username:
            qoscore.check_home_dir()
            cmds.clear()
            import system.opts.komshell as komshell
            shell_statu = komshell.main(username)
            if shell_statu == 0:
                return 0
            elif shell_statu == 1:
                return 1
            else:
                return False
        else:
            sys.exit(0)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found.{Style.RESET_ALL}")
        sys.exit(0)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 0