# QOS - Main Code: Kom Shell
# Version: 0.1
try:
    # Standard library modules
    import os
    import sys
    import json
    import subprocess
    import time
    import pathlib
    # Third-party modules
    from colorama import init as cinit
    from colorama import Fore, Style, Back
    # Core modules 
    import system.core.login as login
    import system.core.options as options
    import system.core.cmds as cmds
    import system.core.biscuit as biscuit
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(1)

cinit(autoreset=True)

# Open config files
with open('data/config/config.json', 'r') as config_file:
    config = json.load(config_file)
    version = config["version"]
    os_type = config["os_type"]
    qos_path = config["qos_path"]
    home_path = config["home_path"]
    data_path = config["data_path"]
with open('data/config/shell.json', 'r') as shell_file:
    shell_config = json.load(shell_file)
    ucp = shell_config["unknown_command_progression"]

def shell(username):
    print(Style.DIM + Fore.YELLOW + "Kom Shell for QOS - " + version + Style.RESET_ALL + "\n")
    # Initialize home directory
    default_path = os.path.join(home_path, username)
    # Initialize working directory
    working_path = default_path
    # Start shell loop
    while True:
        try:
            if working_path == default_path:
                tip_path = "~"
            elif working_path.startswith(default_path):
                tip_path = "~ " + str(pathlib.Path(working_path).relative_to(home_path))
            else:
                tip_path = working_path

            shell_command = input(f"{Back.LIGHTBLUE_EX}[QOS]{Back.WHITE}{Fore.BLACK} {time.strftime('%H:%M:%S')} {Back.GREEN}{Fore.WHITE} {username} {Style.RESET_ALL} > {Fore.LIGHTGREEN_EX}{tip_path} $ {Style.RESET_ALL}")

            match shell_command:
                case "help":
                    print(f"{Style.BRIGHT}{Fore.YELLOW}% Shell Commands Help Menu %{Style.RESET_ALL}")
                    options.cat("system/etc/help.txt")
                    if ucp:
                        print(f"{Style.BRIGHT}{Fore.GREEN}Tips: Unknown commands will be executed as scripts with system. You can disable in the shell settings.{Style.RESET_ALL}")
                case "version":
                    print(f"{Fore.GREEN}QOS Version:{Style.RESET_ALL} {version}")
                case "pwd":
                    print(os.getcwd())
                case "time":
                    print(time.strftime("%Y-%m-%d %H:%M:%S"))
                case "whoami":
                    print(username)
                case "clear":
                    cmds.clear()
                case "ls":
                    cmds.ls(working_path)
                case "cd":
                    print(f"{Fore.YELLOW}Usage: cd <directory>{Style.RESET_ALL}")
                case shell_command if shell_command.startswith("cd "):
                    new_path = cmds.cd(shell_command[3:], working_path)
                    if new_path:
                        working_path = new_path
                case "exit":
                    cmds.exit()
                case "mkdir":
                    cmds.mkdir(working_path)
                case "cp":
                    print(f"{Fore.YELLOW}Usage: cp <source> <destination>{Style.RESET_ALL}")
                case shell_command if shell_command.startswith("cp "):
                    _, src, dst = shell_command.split(' ', 2)
                    cmds.cp(src, dst)
                case "rm":
                    print(f"{Fore.YELLOW}Usage: rm <file>{Style.RESET_ALL}")
                case shell_command if shell_command.startswith("rm "):
                    _, file = shell_command.split(' ', 1)
                    cmds.rm(file)
                case "":
                    pass
                case "adduser":
                    login.add_user()
                case "removeuser":
                    login.remove_user()
                case "chgpasswd":
                    login.change_password()
                case shell_command if shell_command.startswith("biscuit "):
                    _, command, *args = shell_command.split(' ', 2)
                    if shell_command[0:6] == "biscuit":
                        print(f"{Fore.YELLOW}% Biscuit Package Manager %{Style.RESET_ALL}")
                        cmds.cat("system/etc/biscuit.txt")
                    elif command == "install":
                        if args:
                            pkg_path = args[0]
                            biscuit.install(pkg_path)
                        else:
                            print(f"{Fore.YELLOW}Usage: biscuit install <package>{Style.RESET_ALL}")
                    elif command == "remove":
                        if args:
                            app_name = args[0]
                            biscuit.remove(app_name)
                        else:
                            print(f"{Fore.YELLOW}Usage: biscuit remove <package>{Style.RESET_ALL}")
                    elif command == "list":
                        biscuit.list()
                    elif command == "search":
                        if args:
                            query = args[0]
                            biscuit.search(query)
                        else:
                            print(f"{Fore.YELLOW}Usage: biscuit search <query>{Style.RESET_ALL}")
                    else:
                        print(f"{Fore.YELLOW}% Biscuit Package Manager %{Style.RESET_ALL}")
                        cmds.cat("system/etc/biscuit.txt")
                case "settings":
                    try:
                        import system.apps.settings as settings
                        settings.main()
                    except ImportError as error:
                        print(f"{Fore.RED}Error{Style.RESET_ALL}: {error}")
                case _:
                    if ucp:
                        script_path = os.path.join(working_path, shell_command + ".py")
                        if os.path.isfile(script_path):
                            subprocess.call(["python", script_path])
                        else:
                            subprocess.call(shell_command, shell=True)
                    else:
                        script_path = os.path.join(working_path, shell_command + ".py")
                        if os.path.isfile(script_path):
                            subprocess.call(["python", script_path])
                        else:
                            print(f"{Fore.RED}Unknown command:{Style.RESET_ALL} {shell_command}")

        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}(KeyboardInterrupt){Style.RESET_ALL}")
            cmds.exit()
        except Exception as e:
            print(f"Error: {e}")
            cmds.clear()
            sys.exit()
        finally:
            pass

