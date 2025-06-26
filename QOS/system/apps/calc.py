# QOS Calculator Application
# 参考了 MPGA-PyOS 的计算器程序代码，进行了改进

from colorama import Fore, Back, Style, init

init(autoreset=True)

def main():
    print(Style.DIM + Fore.GREEN + "Quarter OS Calculator" + Style.RESET_ALL)
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
                try:
                    result = eval(input_text)
                    print(Fore.GREEN + str(result) + Style.RESET_ALL)
                except ZeroDivisionError:
                    print(Fore.RED + "Error: division by zero" + Style.RESET_ALL)
                except SyntaxError:
                    print(Fore.RED + "Error: invalid syntax" + Style.RESET_ALL)
                except NameError:
                    print(Fore.RED + "Error: undefined name" + Style.RESET_ALL)
                except TypeError:
                    print(Fore.RED + "Error: unsupported operand type(s) for operator" + Style.RESET_ALL)
                except:
                    print(Fore.RED + "Error: unknown error" + Style.RESET_ALL)
                finally:
                    pass
        except NameError as e:
            print(Fore.RED + f"Error: {e}" + Style.RESET_ALL)
            continue
        except KeyboardInterrupt:
            print(Fore.RED + "\nKeyboardInterrupt" + Style.RESET_ALL)
            break

if __name__ == '__main__':
    main()