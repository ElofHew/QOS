# QOS - Main Code: Kom Shell
try:
    # Standard library modules
    import os
    import sys
    import json
    import shlex
    import time
    import pathlib
    from platform import system as pfs
    # Third-party modules
    from colorama import init as cinit
    from colorama import Fore, Style, Back
    # Core modules
    import system.core.cmds as cmds
    import system.core.runs as runs
    from system.core.features import get_ads
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(0)

cinit(autoreset=True)

# Open config files
try:
    with open('data/config/config.json', 'r') as config_file:
        config = json.load(config_file)
    version = config.get("version", "?")
    os_type = config.get("os_type", pfs().lower())
    qos_path = config.get("qos_path", os.getcwd())
    home_path = config.get("home_path", os.path.join(os.getcwd(), "home"))
except FileNotFoundError:
    print(f"{Fore.RED}Error: {Style.RESET_ALL}'config.json' not found.")
    sys.exit(0)
except json.JSONDecodeError:
    print(f"{Fore.RED}Error: {Style.RESET_ALL}'config.json' is not valid JSON.")
    sys.exit(0)
except Exception as e:
    print(f"{Fore.RED}Error: {Style.RESET_ALL}{e}")
    sys.exit(0)

def main(username):
    print(f"{Style.DIM}{Fore.YELLOW}Kom Shell for QOS - {version}{Style.RESET_ALL}\n")
    # Initialize home directory
    default_path = os.path.join(home_path, username)
    # Initialize working directory
    working_path = default_path
    # Initialize user directory
    user_path = os.path.join(home_path, username)
    # Initialize supported commands
    try:
        with open(os.path.join(qos_path, "system", "shell", "cmds.json"), "r") as supported_cmds_file:
            supported_cmds = json.load(supported_cmds_file)
    except FileNotFoundError:
        print(f"{Fore.RED}Error: {Style.RESET_ALL}'cmds.json' not found.")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {Style.RESET_ALL}{e}")
        sys.exit(0)
    # Get ADs
    get_ads()
    # Start shell loop
    while True:
        try:
            # Get working directory
            if working_path == default_path:
                tip_path = "~"
            elif working_path.startswith(default_path):
                tip_path = "~ " + str(pathlib.Path(working_path).relative_to(os.path.join(home_path, username)))
            else:
                tip_path = working_path
            # Get user input
            shell_command = input(f"{Back.LIGHTBLUE_EX}[QOS]{Back.WHITE}{Fore.BLACK} {time.strftime('%H:%M:%S')} {Back.GREEN}{Fore.WHITE} {username} {Style.RESET_ALL} > {Fore.LIGHTGREEN_EX}{tip_path} $ {Style.RESET_ALL}")
            # Run shell commands
            match shlex.split(shell_command):
                case [command, *args] if command in supported_cmds["Core"]:
                    if command == "pwd":
                        cmds.pwd(working_path, [])
                        continue
                    if command == "cd":
                        working_path = cmds.cd(working_path, args if args else [])
                        continue
                    run_cmd = getattr(cmds, command)
                    if callable(run_cmd):
                        run_cmd(working_path, args if args else [])
                        continue
                    else:
                        print(f"{Fore.RED}Error: {Style.RESET_ALL}Command not found: {command}")
                        continue
                case [command, *args] if command in supported_cmds["PackageManager"]:
                    if command in ["biscuit", "pm", "bpm", "bkt", "pkg"]:
                        import system.core.biscuit as biscuit
                        biscuit.main(working_path, args)
                        del biscuit
                        continue
                    elif command in ["shizuku", "szk"]:
                        import system.core.shizuku as shizuku
                        shizuku.main(working_path, args)
                        del shizuku
                        continue
                    else:
                        print(f"{Fore.RED}Error: {Style.RESET_ALL}Command not found: {command}")
                        continue
                case [command, *args] if command in supported_cmds["SystemKit"]:
                    runs.run_system_kits(command, args)
                case _:
                    if shell_command.strip() == "":
                        continue
                    runs.main(working_path, command, args)
        except (KeyboardInterrupt, EOFError):
            print(f"{Style.BRIGHT}{Fore.RED}^C{Style.RESET_ALL}")
            continue
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(0)