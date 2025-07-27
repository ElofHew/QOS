# Quarter Operation System (QOS) - Boot Program
"""
# QOS - Quarter Operation System
@ Author: ElofHew aka Dan_Evan
@ Version: Alpha 0.2
@ Date: 2025-06-29
@ License: GNU General Public License v3.0
@ Description: A Professional Fake-OS Powered by Python3.
"""

# Check qos.py in path （检测路径是否正确）
try:
    import os, sys, colorama
    now_path = os.getcwd()
    if not os.path.isfile(os.path.join(now_path, 'qos.py')):
        if now_path.endswith('QOS'):
            raise FileNotFoundError(f"{colorama.Fore.RED}No such file: 'qos.py' in this directory.\n{colorama.Fore.CYAN}(Maybe you should 'cd QOS' at this directory first?){colorama.Fore.RESET}")
        else:
            raise FileNotFoundError(f"{colorama.Fore.RED}No such file: 'qos.py' in this directory.{colorama.Fore.RESET}")
    if not os.path.isdir(os.path.join(now_path, 'system')):
        if now_path.endswith('QOS'):
            raise NotADirectoryError(f"{colorama.Fore.RED}No such directory:'system' in this directory.\n{colorama.Fore.CYAN}(Maybe you should 'cd QOS' at this directory first?){colorama.Fore.RESET}")
        else:
            raise NotADirectoryError(f"{colorama.Fore.RED}No such directory:'system' in this directory.{colorama.Fore.RESET}")
    if not os.path.isfile(os.path.join(now_path, 'system', 'main.py')):
        print(f"{colorama.Fore.RED}No such file:'main.py' in'system' directory.{colorama.Fore.RESET}")
        print(f"{colorama.Fore.CYAN}Maybe QOS on your system has been broken.{colorama.Fore.RESET}")
        sys.exit(0)
except FileNotFoundError as e:
    print(e)
    sys.exit(0)
except NotADirectoryError as e:
    print(e)
    sys.exit(0)
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(0)
# (20250625)稍微解释一下：
# 上面会检测你当前所在目录是否是QOS所在目录
# 如果不是则不允许你启动，直接sys.exit(0)退出
# 另外如果当前目录最后是"QOS"时，提示你再次cd QOS
# (20250713)新增：检测system文件夹下是否存在main.py文件，如果不存在则提示你可能是QOS损坏

# Check Python Version （检测Python版本）
try:
    import sys, colorama
    if sys.version_info.major < 3 or sys.version_info.minor < 10:
        print(f"{colorama.Fore.RED}Error: QOS requires Python 3.10 or higher.{colorama.Fore.RESET}")
        sys.exit(0)
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(0)
# (20250629)解释一下：
# 这里检测你是否安装了Python 3.10或更高版本，如果不是则不允许你启动，直接sys.exit(0)退出

# Check Python Virtual Environment （检测Python虚拟环境）
try:
    import sys, colorama
    if hasattr(sys, "real_prefix") or (hasattr(sys, "base_prefix") and sys.prefix != sys.base_prefix):
        pass
    else:
        print(f"{colorama.Fore.RED}Error: Please run QOS in a Python Virtual Environment.{colorama.Fore.RESET}")
        print(f"{colorama.Fore.CYAN}If you don't know how to create or activate a Python Virtual Environment, please read the official documentation in 'docs' folder.{colorama.Fore.RESET}")
        sys.exit(0)
except ImportError as e:
    print(f"Error: {e}")
    sys.exit(0)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(0)
# (20250627)解释一下：
# 这里检测你是否在Python虚拟环境中，如果不是则不允许你启动，直接sys.exit(0)退出
# 这里的检测方法是通过判断sys.real_prefix是否存在来实现的，如果存在则说明你在虚拟环境中，否则反之。

# Start Main Program （启动主程序）
if __name__ == "__main__":
    work_path = os.getcwd()
    try:
        import os
        import sys
        import time
        import subprocess
        while True:
            process = subprocess.run([sys.executable, os.path.join(work_path, "system", "main.py"), "--boot", "--regular"])
            qos_return_code = process.returncode
            match qos_return_code:
                case 0:
                    # 0: 正常退出(关机)
                    break
                case 11:
                    # 1: 重新运行(重启)
                    time.sleep(1)
                    continue
                case 12:
                    # 2: 暂未开发但已预留的启动项
                    print("Error: This feature is not yet developed.")
                    break
                case 16:
                    # 3: 启动参数不正确
                    print("Error: Invalid startup parameters.")
                    break
                case 19:
                    # 4: 捕捉到错误
                    print("Error: Something went wrong.")
                    break
                case _:
                    # 其他值: 未知错误
                    print(f"Error: Unknown return code {qos_return_code}.")
                    break
        input("(Press any key to exit)")
    except KeyboardInterrupt:
        print("\nKeyboardInterrupt: Exiting QOS.")
        sys.exit(0)
    except (FileNotFoundError, NotADirectoryError, ImportError, Exception) as e:
        print(f"Error: {e}")
        sys.exit(0)