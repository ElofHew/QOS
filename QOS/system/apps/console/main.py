import os
import sys
import platform
import subprocess

from colorama import init, Fore, Back, Style

init(autoreset=True)

def main():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")
    keyboard_interrupt_caught = False
    try:
        print(f"{Fore.GREEN}Quarter OS Python Console{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Type 'exit()' to exit the console.{Style.RESET_ALL}")
        subprocess.run([sys.executable])
    except KeyboardInterrupt:
        if not keyboard_interrupt_caught:
            print(f"{Fore.RED}KeyboardInterrupt: Exiting console.{Style.RESET_ALL}")
            keyboard_interrupt_caught = True
        sys.exit()
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit()

if __name__ == "__main__":
    main()