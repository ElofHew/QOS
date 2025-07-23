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
    print(f"Error: {e}")
    sys.exit(0)

# Start QOS （启动QOS）
def main():
    # Initialize Colorama （初始化colorama模块）
    init(autoreset=True)

    # Set Working Directory （设置工作目录）
    from os import system as oss
    from os import path as osp
    sys.path.insert(0, osp.abspath(osp.join(osp.dirname(__file__), "..")))

    # Boot Check （启动检查）:
    # Initialize QOS Core Modules （初始化QOS核心模块）
    import system.core.qoscore as qoscore
    # Check Config Files in data （先检查数据目录是否完好，再检查数据目录的配置文件）
    qoscore.check_more_dir()
    qoscore.check_config_dir()
    # Check OS and Path （检查你用的操作系统和工作路径是啥）
    qoscore.check_os_path()

    # Load Basic Modules （加载功能基础模块，如cat、clear等）
    import system.core.features as features

    # Clear Console Screen （清屏）
    features.clear()

    # Load Config Files （加载配置文件）
    with open("data/config/config.json", "r") as qos_config_file:
        config_file = json.load(qos_config_file)
        os_type = config_file["os_type"]
        qos_startup_logo = config_file["qos_startup_logo"]
        version = config_file["version"]
        startup_title = config_file["startup_title"]
        oobe_condition = config_file["oobe"]
    
    # Start Up UI (启动界面)
    try:
        qos_logo = os.path.join("system", "etc", "logo", qos_startup_logo + ".txt")
        qos_version = str(version)
        print(f"{Style.DIM}Quarter Operation System{Style.RESET_ALL}\n")
        print(f"{Fore.MAGENTA}{Style.BRIGHT}Version: {qos_version}{Style.RESET_ALL}\n")
        features.cat(qos_logo)
        print("GitHub Repo: https://github.com/ElofHew/QOS\n"
              "@ 2025 Oak Studio. All Rights Reserved.\n"
              "Official Website: https://os.drevan.xyz/")
        print()
        features.get_ads()
        # 如果OOBE没过，则进入OOBE设置一遍
        if oobe_condition:
            import system.opts.oobe as oobe
            retrun_code = oobe.OOBE().main()
            del oobe
            sys.exit(1)
        # 加载登录管理器
        import system.opts.loginman as loginman
        username = loginman.main(version, startup_title)
        del loginman
        if username:
            qoscore.check_home_dir()
            features.clear()
            # 进入终端界面
            import system.opts.komshell as komshell
            komshell.main(username)
            del komshell
        else:
            sys.exit(0)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
        sys.exit(0)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: File not found.{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 0

if __name__ == "__main__":
    if sys.argv[1:]:
        mode = sys.argv[1]
        if mode == "--boot":
            if sys.argv[2:]:
                if sys.argv[2] == "--regular":
                    main()
                if sys.argv[2] == "--recovery":
                    print(f"{Fore.RED}Error: Recovery mode not supported.{Style.RESET_ALL}")
                    sys.exit(2)
        if mode == "--version":
            print(f"{Fore.LIGHTGREEN_EX}Quarter OS on Python3 - {Fore.CYAN}Alpha 0.2.2{Fore.RESET}")
            sys.exit(0)
    print(f"{Fore.RED}Error: Unknown arguments.{Style.RESET_ALL}")
    sys.exit(3)