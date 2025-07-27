import sys
from os import path as osp
from colorama import init as cinit
from colorama import Fore, Style

cinit(autoreset=True)

sys.path.insert(0, osp.abspath(osp.join(osp.dirname(__file__), '..', '..')))

try:
    import system.core.login as login
    import system.core.options as options
except ImportError as e:
    print(f"Error: {e}")
    input("(Press enter to continue...)")
    sys.exit(1)

__usage__ = """QOS Kom Shell Settings Usage:
-a : Account settings.
-s : Shell settings.
-g : General settings.

-a (account) >>>
adduser : Add a new user.
rmuser : Remove a user.
passwd : Change a user's password.
sysname : Change the system name.

-s (shell) >>>
theme : Change the shell theme.
ucp : Change Unknown Command Progression.
timeout : Change startup wait time.

-g (general) >>>
startup : Change the startup title.
qoslogo : Change the QOS logo text.
mngads : Manage ADs.
"""

invalid_arg = "Invalid argument. Please use '-h' to check it."
missing_arg = "Missing argument. Please use '-h' to check it."

# 处理缺失参数
def handle_missing_arg(command=""):
    if command == "":
        print(__usage__)
    elif command == "adduser":
        print(f"{Fore.YELLOW}Usage: adduser <username> <password>{Fore.RESET}")
    elif command == "rmuser":
        print(f"{Fore.YELLOW}Usage: rmuser <username>{Fore.RESET}")
    elif command == "passwd":
        print(f"{Fore.YELLOW}Usage: passwd <username> <new_password ('none' for no password)>{Fore.RESET}")
    elif command == "sysname":
        print(f"{Fore.YELLOW}Usage: sysname <new_system_name>{Fore.RESET}")
    elif command == "theme":
        print(f"{Fore.YELLOW}Usage: theme <theme_name>{Fore.RESET}")
    elif command == "ucp":
        print(f"{Fore.YELLOW}Usage: ucp <check/enable/disable>{Fore.RESET}")
    elif command == "timeout":
        print(f"{Fore.YELLOW}Usage: timeout <seconds (0 for no timeout) (default for 3s)>{Fore.RESET}")
    elif command == "startup":
        print(f"{Fore.YELLOW}Usage: startup <new_startup_title>{Fore.RESET}")
    elif command == "qoslogo":
        print(f"{Fore.YELLOW}Usage: qoslogo (No Arguments){Fore.RESET}")
    elif command == "mngads":
        print(f"{Fore.YELLOW}Usage: mngads <check/enable/disable>{Fore.RESET}")
    else:
        print(f"{Fore.YELLOW}{missing_arg}{Fore.RESET}")
    sys.exit(1)

# 处理无效参数
def handle_invalid_arg():
    print(invalid_arg)
    sys.exit(1)

# 通用命令处理
def process_command(args, command_dict):
    try:
        if not args:
            handle_invalid_arg()
        command = args[0]
        if command in command_dict:
            func, min_args = command_dict[command]
            if len(args) >= min_args:
                cdt = func(*args[1:])
                if cdt == 1:
                    sys.exit(1)
            else:
                handle_missing_arg(args[0])
        else:
            handle_invalid_arg()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")
        sys.exit(1)

def account(args):
    command_dict = {
        "adduser": (login.add_user, 3),
        "rmuser": (login.remove_user, 2),
        "passwd": (login.change_password, 3),
        "sysname": (login.make_system_name, 2)
    }
    process_command(args, command_dict)

def shell(args):
    command_dict = {
        "theme": (options.set_theme, 2),
        "ucp": (options.unknown_command_progression, 2),
        "timeout": (options.set_startup_timeout, 2)
    }
    process_command(args, command_dict)

def general(args):
    command_dict = {
        "startup": (options.change_startup_title, 2),
        "qoslogo": (options.change_qos_logo_text, 1),
        "mngads": (options.manage_ads, 2)
    }
    process_command(args, command_dict)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-h":
            print(__usage__)
            sys.exit(0)
        elif sys.argv[1] == "-s":
            shell(sys.argv[2:] if len(sys.argv) > 2 else [])
        elif sys.argv[1] == "-g":
            general(sys.argv[2:] if len(sys.argv) > 2 else [])
        elif sys.argv[1] == "-a":
            account(sys.argv[2:] if len(sys.argv) > 2 else [])
        else:
            handle_invalid_arg()
    else:
        print(__usage__)
        sys.exit(0)
