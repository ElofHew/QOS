# QOS Calender App

import time
import datetime
import calendar
from colorama import init, Fore, Back, Style

init(autoreset=True)

def get_date():
    now = datetime.datetime.now()
    d_year = now.strftime("%Y")
    d_month = now.strftime("%m")
    print_start(d_year, d_month)

def print_start(d_year, d_month):
    print(Fore.LIGHTBLUE_EX + calendar.month(int(d_year), int(d_month), w=2, l=1) + Fore.RESET)

def print_date():
    try:
        i_year = input(Fore.LIGHTGREEN_EX + "Year: " + Fore.LIGHTMAGENTA_EX)
        i_month = input(Fore.LIGHTGREEN_EX + "Month: " + Fore.LIGHTMAGENTA_EX)
        if not i_year.isdigit() or not i_month.isdigit():
            raise ValueError
        if int(i_month) < 1 or int(i_month) > 12:
            raise ValueError
        if int(i_year) < 1 or int(i_year) > 9999:
            raise ValueError
        print(Fore.LIGHTBLUE_EX + calendar.month(int(i_year), int(i_month), w=2, l=1) + Fore.RESET)
    except ValueError:
        print(Fore.RED + "Invalid input. Please enter a valid year and month." + Style.RESET_ALL)

def main():
    print(Fore.GREEN + "Quarter OS Calculator" + Style.RESET_ALL)
    get_date()
    while True:
        try:
            option = input(Fore.CYAN + "> " + Style.RESET_ALL)
            if option == "exit":
                break
            elif option == "help":
                print(Fore.YELLOW + "Available commands: date, exit" + Style.RESET_ALL)
            elif option == "date":
                print_date()
        except KeyboardInterrupt:
            print(Style.BRIGHT + Fore.RED + "\nKeyboardInterrupt: Exiting..." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()