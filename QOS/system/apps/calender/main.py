# QOS Calender App

import sys
import datetime
import calendar
from colorama import init, Fore, Back, Style

init(autoreset=True)

def get_current_date():
    now = datetime.datetime.now()
    d_year = now.strftime("%Y")
    d_month = now.strftime("%m")
    return d_year, d_month

def print_calendar(year, month):
    print(Fore.LIGHTBLUE_EX + calendar.month(int(year), int(month), w=2, l=1) + Fore.RESET)

def get_user_date():
    try:
        i_year = input(Fore.LIGHTGREEN_EX + "Year: " + Fore.LIGHTMAGENTA_EX).strip()
        i_month = input(Fore.LIGHTGREEN_EX + "Month: " + Fore.LIGHTMAGENTA_EX).strip()
        if not i_year.isdigit() or not i_month.isdigit():
            raise ValueError("Invalid input. Year and month must be digits.")
        if int(i_month) < 1 or int(i_month) > 12:
            raise ValueError("Invalid month. Please enter a value between 1 and 12.")
        if int(i_year) < 1 or int(i_year) > 9999:
            raise ValueError("Invalid year. Please enter a value between 1 and 9999.")
        return i_year, i_month
    except ValueError as ve:
        print(Fore.RED + str(ve) + Style.RESET_ALL)
        return None, None

def print_date():
    year, month = get_user_date()
    if year and month:
        print_calendar(year, month)

def get_date_from_args(year, mouth):
    try:
        if not year.isdigit() or not mouth.isdigit():
            raise ValueError("Invalid input. Year and month must be digits.")
        if int(mouth) < 1 or int(mouth) > 12:
            raise ValueError("Invalid month. Please enter a value between 1 and 12.")
        if int(year) < 1 or int(year) > 9999:
            raise ValueError("Invalid year. Please enter a value between 1 and 9999.")
        print_calendar(year, mouth)
        return 0
    except ValueError as ve:
        print(Fore.RED + str(ve) + Style.RESET_ALL)
        return 1

def main():
    if sys.argv[1:]:
        if sys.argv[2:]:
            return_code = get_date_from_args(sys.argv[1], sys.argv[2])
            sys.exit(return_code)
        else:
            return_code = get_date_from_args(sys.argv[1], "1")
            sys.exit(return_code)
    # Main UI
    print(Fore.GREEN + "Quarter OS Calender App" + Style.RESET_ALL)
    year, month = get_current_date()
    print_calendar(year, month)
    
    while True:
        try:
            option = input(Fore.CYAN + "> " + Style.RESET_ALL).strip().lower()
            if option == "exit":
                break
            elif option == "help":
                print(Fore.YELLOW + "Available commands: date, exit" + Style.RESET_ALL)
            elif option == "date":
                print_date()
            else:
                print(Fore.RED + "Invalid command. Please try again." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Style.BRIGHT + Fore.RED + "\nKeyboardInterrupt: Exiting..." + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
