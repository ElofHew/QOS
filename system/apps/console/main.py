import os
import sys
from platform import system as pfs
from subprocess import run as subprocess_run

from colorama import init, Fore, Style

init(autoreset=True)

def from_args(args):
    subprocess_run([sys.executable, "-c"] + args)

def main():
    os.system("cls" if pfs() == "Windows" else "clear")
    keyboard_interrupt_caught = False
    try:
        print(f"{Fore.GREEN}Quarter OS Python Console{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit()' to exit the console.{Style.RESET_ALL}")
        subprocess_run([sys.executable])
    except KeyboardInterrupt:
        if not keyboard_interrupt_caught:
            print(f"{Fore.RED}KeyboardInterrupt: Exiting console.{Style.RESET_ALL}")
            keyboard_interrupt_caught = True
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)

if __name__ == "__main__":
    if sys.argv[1:]:
        from_args(sys.argv[1:])
        sys.exit(0)
    main()