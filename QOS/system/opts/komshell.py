# QOS - Main Code: Kom Shell
# Version: 0.1
try:
    # Standard library modules
    import os
    import sys
    import json
    import subprocess
    import time
    # Third-party modules
    import colorama
    # Core modules 
    import system.core.login as login
    import system.core.options as options
    import system.core.cmds as cmds
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

colorama.init(autoreset=True)

# Open config files
with open('data/config/config.json', 'r') as config_file:
    config = json.load(config_file)
    version = config["version"]
    os_type = config["os_type"]
    qos_path = config["qos_path"]
with open('data/config/shell.json', 'r') as shell_file:
    shell_config = json.load(shell_file)
    ucp = shell_config["unknown_command_progression"]

def shell(username):
    print(f"{colorama.Style.DIM}{colorama.Fore.YELLOW}Kom Shell for QOS - v0.1{colorama.Style.RESET_ALL}\n")
    working_path = qos_path
    while True:
        try:
            shell_command = input(f"{colorama.Back.LIGHTBLUE_EX}[QOS]{colorama.Back.WHITE}{colorama.Fore.BLACK} {time.strftime('%H:%M:%S')} {colorama.Back.GREEN}{colorama.Fore.WHITE} {username} {colorama.Style.RESET_ALL} > ")
            if shell_command == "help":
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}% Shell Commands Help Menu %{colorama.Style.RESET_ALL}")
                options.cat("system/etc/help.txt")
                if ucp:
                    print(f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Tips: Some unknow commands will be executed with progression. You can disable this option in settings.{colorama.Style.RESET_ALL}")
                else:
                    pass
            elif shell_command == "version":
                print(f"{colorama.Fore.GREEN}QOS version:{colorama.Style.RESET_ALL} {version}")
            elif shell_command == "pwd":
                print(os.getcwd())
            # QOS Shell Commands
            elif shell_command == "time":
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
            elif shell_command == "whoami":
                print(username)
            elif shell_command == "clear":
                cmds.clear()
            elif shell_command == "ls":
                cmds.ls(working_path)
            elif shell_command == "cd":
                print(f"{colorama.Fore.YELLOW}Usage: cd <directory>{colorama.Style.RESET_ALL}")
            elif shell_command.startswith("cd "):
                working_path = cmds.cd(working_path.cmd[3:], working_path)
            elif shell_command == "exit":
                cmds.exit()
            elif shell_command == "":
                pass
            # QOS Login Manager
            elif shell_command == "adduser":
                login.add_user()
            elif shell_command == "removeuser":
                login.remove_user()
            elif shell_command == "chgpasswd":
                login.change_password()
            # QOS Apps
            elif shell_command == "settings":
                try:
                    import system.apps.settings as settings
                    settings.main()
                except ImportError as error:
                    print(f"{colorama.Fore.RED}Error{colorama.Style.RESET_ALL}: {error}")
            else:
                if ucp:
                    # 尝试在working_path目录下查找是否存在同名的.py文件
                    script_path = os.path.join(working_path, shell_command + ".py")
                    if os.path.isfile(script_path):
                        subprocess.call(["python", script_path])
                    else:
                        subprocess.call(shell_command, shell=True)
                else:
                    # 查找是否存在同名的.py文件
                    script_path = os.path.join(working_path, shell_command + ".py")
                    if os.path.isfile(script_path):
                        subprocess.call(["python", script_path])
                    else:
                        print(f"{colorama.Fore.RED}Unknown command:{colorama.Style.RESET_ALL} {shell_command}")
        except KeyboardInterrupt:
            print(f"{colorama.Style.DIM}{colorama.Fore.YELLOW}(KeyboardInterrupt){colorama.Style.RESET_ALL}")
            cmds.exit()
        except Exception as e:
            print(f"Error: {e}")
            cmds.clear()
            sys.exit()
