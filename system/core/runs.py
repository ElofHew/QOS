import os
import sys
import subprocess
import json
from pathlib import Path
from colorama import Fore, Style
from colorama import init as cinit

cinit(autoreset=True)

with open(os.path.join("data", "config", "config.json"), "r") as config_file:
    config_data = json.load(config_file)
    qos_path = config_data.get("qos_path", os.getcwd())

# Run system kits
def run_system_kits(command, args=[]):
    try:
        filename = command + ".py"
        if os.path.isfile(os.path.join(qos_path, "system", "kits", filename)):
            current_script_path = os.path.join(qos_path, "system", "kits", filename)
            kitproc = subprocess.run([sys.executable, current_script_path] + args)
            if kitproc.returncode != 0:
                print(f"{Fore.YELLOW}Warning: Return code: {kitproc.returncode}{Style.RESET_ALL}")
            return kitproc.returncode
        else:
            print(f"{Fore.RED}Error: {Style.RESET_ALL}Kit not found: {command}")
            return 1
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {command}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {command}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1

# Run more commands
def ucprogress(working_path, shell_command, args=[]):
    try:
        with open(os.path.join(qos_path, "data", "config", "config.json"), "r") as config_file:
            config_data = json.load(config_file)
        ucp = config_data.get("unknown_command_progression", False)
        if not ucp:
            print(f"{Fore.RED}Unknown command: {Fore.RESET}{shell_command}")
            return 0
        boot_string = str(shell_command)
        boot_args = args if args else []
        os.chdir(working_path)
        process = subprocess.run([boot_string] + boot_args)
        if process.returncode != 0:
            print(f"{Fore.YELLOW}WARNING: This app returned a code: {process.returncode}.{Style.RESET_ALL}")
        os.chdir(qos_path)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(qos_path)

def run_3rd_party_apps(working_path, shell_command, args=[]):
    try:
        # 3rd party apps
        third_party_app_list = os.path.join(qos_path, "data", "shell", "apps.json")
        # Open json files
        with open(third_party_app_list, "r") as tpapp_file:
            tpapp_list = json.load(tpapp_file)
        # Check command
        if shell_command in tpapp_list:
            app_path = tpapp_list.get(shell_command)["path"]
            if os.path.exists(app_path):
                app_file = os.path.join(app_path, "main.py")
                if not os.path.isfile(app_file):
                    print(f"{Fore.RED}Error: {app_file} not found.{Style.RESET_ALL}")
                    return 1
            else:
                print(f"{Fore.RED}Error: {app_path} not found.{Style.RESET_ALL}")
                return 1
            boot_string = str(os.path.join(qos_path, app_file))
            # Check arguments
            boot_args = args if args else []
            # Run app
            os.chdir(app_path)
            process = subprocess.run([sys.executable, boot_string] + boot_args)
            if process.returncode != 0:
                print(f"{Fore.YELLOW}WARNING: This app returned a code: {process.returncode}.{Style.RESET_ALL}")
            os.chdir(qos_path)
            return 0
        else:
            ucprogress(working_path, shell_command, args)
    except FileNotFoundError:
        print(f"{Fore.RED}Info file not found.{Style.RESET_ALL}")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(qos_path)

def run_sys_apps(working_path, shell_command, args=[]):
    try:
        # System apps
        system_app_list = os.path.join(qos_path, "system", "shell", "apps.json")
        # Open json files
        with open(system_app_list, "r") as sysapp_file:
            sysapp_list = json.load(sysapp_file)
        # Check command
        if shell_command in sysapp_list:
            app_path = Path(sysapp_list.get(shell_command)["path"]).resolve()
            if os.path.exists(app_path):
                app_file = os.path.join(app_path, "main.py")
                if not os.path.isfile(app_file):
                    print(f"{Fore.RED}Error: {app_file} not found.{Style.RESET_ALL}")
                    return 1
            else:
                print(f"{Fore.RED}Error: {app_path} not found.{Style.RESET_ALL}")
                return 1
            boot_string = str(os.path.join(qos_path, app_file))
            # Check arguments
            boot_args = args if args else []
            # Run app
            os.chdir(app_path)
            process = subprocess.run([sys.executable, boot_string] + boot_args)
            if process.returncode != 0:
                print(f"{Fore.YELLOW}WARNING: This app returned a code: {process.returncode}.{Style.RESET_ALL}")
            os.chdir(qos_path)
            return 0
        else:
            run_3rd_party_apps(working_path, shell_command, args)
    except FileNotFoundError:
        print(f"{Fore.RED}Info file not found.{Style.RESET_ALL}")
        return 1
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(qos_path)

def run_local_prog(working_path, shell_command, args=[]):
    try:
        current_script_path = os.path.join(working_path, shell_command[2:])
        if os.path.isfile(Path(current_script_path + ".py")):
            current_script_path = Path(current_script_path + ".py")
        elif os.path.isfile(current_script_path):
            pass
        else:
            print(f"{Fore.RED}Local program not found:{Style.RESET_ALL} {shell_command}")
            return 1
        boot_string = str(current_script_path)
        # Process arguments
        boot_args = args if args else []
        os.chdir(working_path)
        process = subprocess.run([sys.executable, boot_string] + boot_args)
        if process.returncode != 0:
            print(f"{Fore.YELLOW}WARNING: This app returned a code: {process.returncode}.{Style.RESET_ALL}")
        os.chdir(qos_path)
        return 0
    except subprocess.CalledProcessError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except OSError as e:
        print(f"{Fore.RED}Error: Failed to run {shell_command}. {e}{Style.RESET_ALL}")
        return 1
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(qos_path)

def main(working_path, shell_command, args=[]):
    try:
        if shell_command.startswith("./"):
            run_local_prog(working_path, shell_command, args)
        else:
            run_sys_apps(working_path, shell_command, args)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        return 1
    finally:
        os.chdir(qos_path)