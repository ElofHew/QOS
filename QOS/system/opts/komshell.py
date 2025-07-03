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
        if not (shell_command == "args_tips" or shell_command == "check_args" or shell_command == "pm_tips"):
            func = getattr(cmds, shell_command)
            if callable(func):
                func()
        else:
            print(f"{Fore.RED}Error: {Style.RESET_ALL}Found the command: {shell_command}, but you cannot run it directly.")
    except AttributeError:
        try:
            if shell_command.startswith("./"):
                if shell_command.endswith(".py"):
                    if os.path.isfile(os.path.join(working_path, shell_command)):
                        current_script_path = os.path.join(working_path, shell_command)
                    else:
                        current_script_path = os.path.join(working_path, shell_command + ".py")
                else:
                    current_script_path = os.path.join(working_path, shell_command + ".py")
            else:
                if os.path.isfile(os.path.join(working_path, shell_command + ".py")):
                    print(f"{Fore.YELLOW}WARNING: If you want to run this python program, please add './' before the program name.{Style.RESET_ALL}")
                    return
            if os.path.isfile(current_script_path):
                os.chdir(working_path)
                if os_type == "windows":
                    process = subprocess.Popen(["python", current_script_path])
                else:
                    process = subprocess.Popen(["python3", current_script_path])
                os.chdir(qos_path)
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
                        os.chdir(os.path.join(qos_path, "data", "apps", shell_command))
                        if os_type == "windows":
                            process = subprocess.Popen(["python", third_party_script_path])
                        else:
                            process = subprocess.Popen(["python3", third_party_script_path])
                        os.chdir(qos_path)
                    else:
                        if ucp:
                            process = subprocess.Popen(shell_command, shell=True)
                        else:
                            print(f"{Fore.RED}Unknown command:{Style.RESET_ALL} {shell_command}")
                            return
            process.wait()
            process.kill()
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}Process terminated with error code:{Style.RESET_ALL} {process.returncode}")
            return False
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
                    elif command == "pwd":
                        cmds.pwd(working_path)
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
                            if command == "activate":
                                cmds.activate(args[0])
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
                    case_more_commands(shell_command, working_path)
        except KeyboardInterrupt:
            print(f"{Style.DIM}{Fore.YELLOW}(Keyboard Detected){Style.RESET_ALL}")
            cmds.exit()
        except EOFError:
            print(f"{Style.DIM}{Fore.YELLOW}(EOF Detected){Style.RESET_ALL}")
            cmds.exit()
        except Exception as e:
            print(f"Error: {e}")
            cmds.clear()
            sys.exit()
