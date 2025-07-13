# QOS - Main Code: Kom Shell
# Version: 0.1
try:
    # Standard library modules
    import os
    import sys
    import json
    import shlex
    import subprocess
    import time
    import pathlib
    # Third-party modules
    from colorama import init as cinit
    from colorama import Fore, Style, Back
    # Core modules
    import system.core.cmds as cmds
    from system.core.options import get_ads
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

def case_more_commands(shell_command, working_path):
    try:
        if not (shell_command == "args_tips" or shell_command == "check_args" or shell_command == "pm_tips"):
            func = getattr(cmds, shell_command)
            if callable(func):
                func()
        else:
            print(f"{Fore.RED}Error: {Style.RESET_ALL}Found the command: {shell_command}, but you cannot run it directly.")
    except AttributeError:
        try:
            if shell_command.startswith("./"):
                if os.path.isfile(os.path.join(working_path, shell_command[2:] + ".py")):
                    current_script_path = os.path.join(working_path, shell_command[2:] + ".py")
                    cmds.run_local_prog(working_path, current_script_path)
                elif os.path.isfile(os.path.join(working_path, shell_command[2:])):
                    current_script_path = os.path.join(working_path, shell_command[2:])
                    cmds.run_local_prog(working_path, current_script_path)
                else:
                    cmds.run_sys_apps(shell_command[2:], working_path)
            else:
                if os.path.isfile(os.path.join(working_path, shell_command + ".py")):
                    print(f"{Fore.YELLOW}WARNING: If you want to run this python program, please add './' before the command.{Style.RESET_ALL}")
                    return False
                elif os.path.isfile(os.path.join(working_path, shell_command)):
                    print(f"{Fore.YELLOW}WARNING: If you want to run this python program, please add './' before the command.{Style.RESET_ALL}")
                    return False
                else:
                    cmds.run_sys_apps(shell_command, working_path)
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}Process terminated.{Style.RESET_ALL}")
            return False
        except FileNotFoundError:
            print(f"{Fore.RED}Program not found:{Style.RESET_ALL} {shell_command}")
        except Exception as e:
            print(f"Error: {e}")
        finally:
            os.chdir(qos_path)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        os.chdir(qos_path)

def main(username):
    print(Style.DIM + Fore.YELLOW + "Kom Shell for QOS - " + version + Style.RESET_ALL + "\n")
    # Initialize home directory
    default_path = os.path.join(home_path, username)
    # Initialize working directory
    working_path = default_path
    # Get ADs
    get_ads()
    # Start shell loop
    try:
        with open(os.path.join(qos_path,"system", "shell", "cmds.json"), "r") as supported_cmds_file:
            supported_cmds = json.load(supported_cmds_file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {Style.RESET_ALL}'cmds.json' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    while True:
        try:
            if working_path == default_path:
                tip_path = "~"
            elif working_path.startswith(default_path):
                tip_path = "~ " + str(pathlib.Path(working_path).relative_to(os.path.join(home_path, username)))
            else:
                tip_path = working_path
            shell_command = input(f"{Back.LIGHTBLUE_EX}[QOS]{Back.WHITE}{Fore.BLACK} {time.strftime('%H:%M:%S')} {Back.GREEN}{Fore.WHITE} {username} {Style.RESET_ALL} > {Fore.LIGHTGREEN_EX}{tip_path} $ {Style.RESET_ALL}")
            # Run shell commands
            match shlex.split(shell_command):
                case [command] if command in supported_cmds["NoArgs"]:
                    if command == "whoami":
                        cmds.whoami(username)
                    elif command == "pwd":
                        cmds.pwd(working_path)
                    elif command == "exit":
                        exit_statu = cmds.exit()
                        if exit_statu:
                            return 0
                    elif command == "reboot":
                        reboot_statu = cmds.reboot()
                        if reboot_statu:
                            return 1
                    else:
                        run_cmd = getattr(cmds, command)
                        run_cmd()
                case [command, *args] if command in supported_cmds["NeedArgs"]:
                    if args == []:
                        if command == "ls":
                            cmds.ls(working_path, ".")
                        else:
                            cmds.args_tips(command)
                    else:
                        check_status = cmds.check_args(command, args)
                        if check_status:
                            if command == "cd":
                                working_path = cmds.cd(working_path, args[0])
                            else:
                                run_cmd = getattr(cmds, command)
                                run_cmd(working_path, *args)
                        else:
                            cmds.args_tips(command)
                case [command] if command in supported_cmds["SystemKit"]:
                    if command == "settings":
                        import system.opts.settings as settings
                        settings.main()
                        del settings
                case [command, *args] if command in supported_cmds["PackageManager"]:
                    if args == []:
                        cmds.pm_tips()
                    else:
                        cmds.pm_check_args(args, working_path)
                case [command, *args] if command in supported_cmds["ShizukuCompat"]:
                    import system.core.shizuku as shizuku
                    if args == []:
                        shizuku.tips()
                    else:
                        if args[0] == "install":
                            shizuku.install(working_path, args[1])
                        elif args[0] == "remove":
                            shizuku.remove(args[1])
                        elif args[0] == "list":
                            shizuku.list()
                        elif args[0] == "run":
                            shizuku.run(args[1])
                        else:
                            shizuku.tips()
                    del shizuku
                case _:
                    if shell_command.strip() == "":
                        continue
                    case_more_commands(shell_command, working_path)
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}(Keyboard Detected){Style.RESET_ALL}")
            cmds.exit()
            return 0
        except EOFError:
            print(f"{Style.DIM}{Fore.YELLOW}(EOF Detected){Style.RESET_ALL}")
            cmds.exit()
            return 0
        except Exception as e:
            print(f"Error: {e}")
            cmds.clear()
            sys.exit()
