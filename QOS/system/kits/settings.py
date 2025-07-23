# QOS Kom Shell Settings

import sys
from os import path as osp

sys.path.insert(0, osp.abspath(osp.join(osp.dirname(__file__), '..', '..')))

try:
    import system.core.login as login
    import system.core.options as options
except ImportError as e:
    print(f"Error: {e}")
    input("(Press enter to continue...)")
    exit()

__usage__ = """Quarter OS Settings Usage:
-a : Account settings.
-s : Shell settings.
-g : General settings.

account :
adduser : Add a new user.
rmuser : Remove a user.
passwd : Change a user's password.
sysname : Change the system name.

shell :
theme : Change the shell theme.
ucp : Change Unknown Command Progression.

general :
startup : Change the startup title.
qoslogo : Change the QOS logo text.
mngads : Manage ADs.
"""

def account(args):
    if args:
        if args[0] == "adduser":
            login.add_user()
        elif args[0] == "rmuser":
            login.remove_user()
        elif args[0] == "passwd":
            login.change_password()
        elif args[0] == "sysname":
            login.make_system_name()
        else:
            print("Invalid argument. Please use '-h' check it.")
            sys.exit(1)
    else:
        print("Invalid argument. Please use '-h' check it.")
        sys.exit(1)

def shell(args):
    if args:
        if args[0] == "theme":
            print("Not implemented yet.")
        elif args[0] == "ucp":
            options.unknown_command_progression()
        else:
            print("Invalid argument. Please use '-h' check it.")
            sys.exit(1)
    else:
        print("Invalid argument. Please use '-h' check it.")
        sys.exit(1)

def general(args):
    if args:
        if args[0] == "startup":
            options.change_startup_title()
        elif args[0] == "qoslogo":
            options.change_qos_logo_text()
        elif args[0] == "mngads":
            options.manage_ads()
        else:
            print("Invalid argument. Please use '-h' check it.")
            sys.exit(1)
    else:
        print("Invalid argument. Please use '-h' check it.")
        sys.exit(1)

if __name__ == "__main__":
    if sys.argv[1:]:
        if sys.argv[1] == "-h":
            print(__usage__)
            sys.exit(0)
        elif sys.argv[1] == "-s":
            shell(sys.argv[2:] if sys.argv[2:] else "")
        elif sys.argv[1] == "-g":
            general(sys.argv[2:] if sys.argv[2:] else "")
        elif sys.argv[1] == "-a":
            account(sys.argv[2:] if sys.argv[2:] else "")
        else:
            print("Invalid argument. Please use '-h' check it.")
            sys.exit(1)
    else:
        print(__usage__)
        sys.exit(0)
    