"""
# Quarter Operation System (QOS)
# 1 Step to run
@ Author: ElofHew aka Dan_Evan
@ Date: 2025-06-22
"""

import os
import sys
import platform

def make_path():
    old_path = os.getcwd()
    new_path = os.path.join(old_path, 'QOS', 'system')
    os.chdir(new_path)

def check_platform():
    global f_os
    if platform.system() == 'Windows':
        os.system('cls')
        f_os = 'Windows'
    elif platform.system() == 'Linux':
        os.system('clear')
        f_os = 'Linux'
    elif platform.system() == 'Darwin':
        os.system('clear')
        f_os = 'MacOS'
    else:
        f_os = 'Unknown'

def main():
    if f_os == 'Windows':
        os.system('python qos.py')
    elif f_os == 'Linux':
        os.system('python3 qos.py')
    elif f_os == 'MacOS':
        os.system('python3 qos.py')
    else:
        print('Unknown platform')

if __name__ == '__main__':
    check_platform()
    make_path()
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
