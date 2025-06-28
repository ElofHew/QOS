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
    import system.core.cmds as cmds
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
        func = getattr(cmds, shell_command)
        if callable(func):
            func()
        else:
            pass
    except AttributeError:
        keyboard_interrupt_caught = False
        try:
            current_script_path = os.path.join(working_path, shell_command + ".py")
            if os.path.isfile(current_script_path):
                if os_type == "windows":
                    process = subprocess.Popen(["python", current_script_path])
                else:
                    process = subprocess.Popen(["python3", current_script_path])
            else:
                system_app_path = os.path.join(qos_path, "system", "apps", shell_command + ".py")
                if os.path.isfile(system_app_path):
                    if os_type == "windows":
                        process = subprocess.Popen(["python", system_app_path])
                    else:
                        process = subprocess.Popen(["python3", system_app_path])
                else:
                    third_party_script_path = os.path.join(qos_path, "data", "apps", shell_command, "main.py")
                    if os.path.isfile(third_party_script_path):
                        if os_type == "windows":
                            process = subprocess.Popen(["python", third_party_script_path])
                        else:
                            process = subprocess.Popen(["python3", third_party_script_path])
                    else:
                        if ucp:
                            process = subprocess.Popen(shell_command, shell=True)
                        else:
                            print(f"{Fore.RED}Unknown command:{Style.RESET_ALL} {shell_command}")
            process.wait()
            process.kill()
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}Process terminated with error code:{Style.RESET_ALL} {process.returncode}")
        except KeyboardInterrupt:
            if not keyboard_interrupt_caught:
                print(f"{Fore.YELLOW}Process terminated.{Style.RESET_ALL}")
                keyboard_interrupt_caught = True
        except FileNotFoundError:
            print(f"{Fore.RED}Program not found:{Style.RESET_ALL} {shell_command}")
        except Exception as e:
            print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def main(username):
    print(Style.DIM + Fore.YELLOW + "Kom Shell for QOS - " + version + Style.RESET_ALL + "\n")
    keyboard_interrupt_caught_shell = False
    # Initialize home directory
    default_path = os.path.join(home_path, username)
    # Initialize working directory
    working_path = default_path
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
                tip_path = "~ " + str(pathlib.Path(working_path).relative_to(home_path))
            else:
                tip_path = working_path
            shell_command = input(f"{Back.LIGHTBLUE_EX}[QOS]{Back.WHITE}{Fore.BLACK} {time.strftime('%H:%M:%S')} {Back.GREEN}{Fore.WHITE} {username} {Style.RESET_ALL} > {Fore.LIGHTGREEN_EX}{tip_path} $ {Style.RESET_ALL}")
            # Run shell commands
            match shell_command.split(" "):
                case [command] if command in supported_cmds["NoArgs"]:
                    if command == "whoami":
                        cmds.whoami(username)
                    if command == "pwd":
                        cmds.pwd(working_path)
                    else:
                        run_cmd = getattr(cmds, command)
                        run_cmd()
                case [command, *args] if command in supported_cmds["NeedArgs"]:
                    if args == []:
                        if command == "ls":
                            cmds.ls(working_path)
                        else:
                            cmds.args_tips(command)
                    else:
                        check_status = cmds.check_args(command, args)
                        if check_status:
                            run_cmd = getattr(cmds, command)
                            run_cmd(*args)
                        else:
                            cmds.args_tips(command)
                case [command, *args] if command in supported_cmds["PackageManager"]:
                    import system.core.biscuit as biscuit
                    biscuit_tips = f"{Fore.YELLOW}Usage: \n{command} <install> <package_path>\n{command} <remove> <app_name>\n{command} <list>\n{command} <search> <keyword>{Style.RESET_ALL}"
                    if args == []:
                        print(biscuit_tips)
                    else:
                        if args[0] == "install":
                            biscuit.install(args[1])
                        elif args[0] == "remove":
                            biscuit.remove(args[1])
                        elif args[0] == "list":
                            biscuit.list()
                        elif args[0] == "search":
                            biscuit.search(args[1])
                        else:
                            print(biscuit_tips)
                case _:
                    case_more_commands(shell_command, working_path)
        except KeyboardInterrupt:
            if not keyboard_interrupt_caught_shell:
                print(f"{Style.DIM}{Fore.YELLOW}(Keyboard Detected){Style.RESET_ALL}")
                statue = cmds.exit()
                if statue == "0":
                    keyboard_interrupt_caught_shell = False
                else:
                    keyboard_interrupt_caught_shell = True
        except EOFError:
            if not keyboard_interrupt_caught_shell:
                print(f"{Style.DIM}{Fore.YELLOW}(Keyboard Detected){Style.RESET_ALL}")
                statue = cmds.exit()
                if statue == "0":
                    keyboard_interrupt_caught_shell = False
                else:
                    keyboard_interrupt_caught_shell = True
        except Exception as e:
            print(f"Error: {e}")
            cmds.clear()
            sys.exit()
