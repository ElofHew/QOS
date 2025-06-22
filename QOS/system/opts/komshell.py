# QOS - Main Code: Kom Shell
# Version: 0.1

import os
import sys
import json
import subprocess
import time
import colorama

import core.login as login
import core.options as options

import apps.settings as settings

colorama.init(autoreset=True)

# Open config files
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)
    version = config["version"]
with open('config/shell.json', 'r') as shell_file:
    shell_config = json.load(shell_file)
    ucp = shell_config["unknown_command_progression"]

def shell(username):
    print(f"{colorama.Style.DIM}{colorama.Fore.YELLOW}Kom Shell for QOS - v0.1{colorama.Style.RESET_ALL}\n")
    while True:
        try:
            shell_command = input(f"{colorama.Back.LIGHTBLUE_EX}[QOS]{colorama.Back.WHITE}{colorama.Fore.BLACK} {time.strftime('%H:%M:%S')} {colorama.Back.GREEN}{colorama.Fore.WHITE} {username} {colorama.Style.RESET_ALL} > ")
            if shell_command == "help":
                print(f"{colorama.Style.BRIGHT}{colorama.Fore.YELLOW}% Shell Commands Help Menu %{colorama.Style.RESET_ALL}")
                options.cat("etc/help.txt")
                if ucp:
                    print(f"{colorama.Style.BRIGHT}{colorama.Fore.GREEN}Tips: Some unknow commands will be executed with progression. You can disable this option in settings.{colorama.Style.RESET_ALL}")
                else:
                    pass
            elif shell_command == "version":
                print(f"{colorama.Fore.MAGENTA}QOS version:{colorama.Style.RESET_ALL} {version}")
            elif shell_command == "time":
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
            elif shell_command == "adduser":
                login.add_user()
            elif shell_command == "removeuser":
                login.remove_user()
            elif shell_command == "chgpasswd":
                login.change_password()
            elif shell_command == "whoami":
                print(username)
            elif shell_command == "settings":
                settings.main()
            elif shell_command == "pwd":
                print(os.getcwd())
            elif shell_command == "clear":
                options.clear()
            elif shell_command == "ls":
                options.ls()
            elif shell_command == "cd":
                print("This version of QOS won't support changing directory, because it will make something wrong with QOS.")
            elif shell_command == "exit":
                options.exit()
            elif shell_command == "":
                pass
            else:
                if ucp:
                    subprocess.call(shell_command, shell=True)
                else:
                    print(f"{colorama.Fore.RED}Unknown command:{colorama.Style.RESET_ALL} {shell_command}")
        except KeyboardInterrupt:
            print(f"{colorama.Style.DIM}{colorama.Fore.YELLOW}(KeyboardInterrupt){colorama.Style.RESET_ALL}")
            options.exit()
        except Exception as e:
            print(f"Error: {e}")
            options.clear()
            sys.exit()
