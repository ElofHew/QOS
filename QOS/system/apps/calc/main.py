# QOS Calculator Application
# 参考了 MPGA-PyOS 的计算器程序代码，进行了改进

import sys
from colorama import Fore, Back, Style, init

init(autoreset=True)

def calculate(expression=None):
    try:
        if expression:
            result = eval(expression)
            print(f"{Fore.GREEN}Result: {result}" + Style.RESET_ALL)
        else:
            print(f"{Fore.CYAN}Unsolved expression: {expression}")
            return None
    except ZeroDivisionError:
        print(Fore.RED + "Error: division by zero" + Style.RESET_ALL)
        return None
    except SyntaxError:
        print(Fore.RED + "Error: invalid syntax" + Style.RESET_ALL)
        return None
    except NameError:
        print(Fore.RED + "Error: undefined name" + Style.RESET_ALL)
        return None
    except TypeError:
        print(Fore.RED + "Error: unsupported operand type(s) for operator" + Style.RESET_ALL)
        return None
    except:
        print(Fore.RED + "Error: unknown error" + Style.RESET_ALL)
        return None

def main():
    if sys.argv[1:]:
        if sys.argv[1] == "-c":
            if sys.argv[2]:
                calculate(sys.argv[2])
                return 0
            else:
                print(Fore.RED + "Error: no expression provided" + Style.RESET_ALL)
                return 1
        else:
            print(Fore.RED + "Error: unknown option" + Style.RESET_ALL)
            return 0
    # Main UI
    print(Fore.GREEN + "Quarter OS Calculator" + Style.RESET_ALL)
    while True:
        try:
            input_text = input(Fore.CYAN + "> " + Style.RESET_ALL)
            if input_text == "exit":
                break
            elif input_text == "help":
                print(Fore.YELLOW + "Available operators: +, -, *, /, **, //\nUse 'exit' to exit the program." + Style.RESET_ALL)
            elif not all(char in "0123456789+-*/.eE" for char in input_text): # 防止恶意运行Python其他代码
                raise NameError(f"{Fore.RED}Input error.")
            else:
                calculate(input_text)
        except NameError as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            continue
        except KeyboardInterrupt:
            print(Fore.RED + "\nKeyboardInterrupt" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()