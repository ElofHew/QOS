"""
# Quarter Operation System (QOS)
# 1 Step to run
@ Author: ElofHew aka Dan_Evan
@ Date: 2025-06-29
@ Version: 0.2
"""

import os
import sys
import platform

try:
    if not os.path.exists(os.path.join(os.getcwd(),"QOS","qos.py")) and os.path.exists(os.path.join(os.getcwd(),"QOS","system")):
        raise FileNotFoundError
    if not sys.version_info >= (3, 10):
        raise ValueError
except FileNotFoundError:
    print("QOS not found. Please check QOS directory.")
    sys.exit(1)
except ValueError:
    print("Python version must be 3.10 or higher.")
    sys.exit(1)

pfs = platform.system().lower()

try:
    if pfs == 'windows':
        if platform.release() < '10':
            raise ValueError
except ValueError:
    print("Error: You must be using Windows 10 or higher to run QOS.")
    sys.exit(1)

if pfs == 'windows':
    try:
        if not os.getenv('PSModulePath'):
            raise ValueError
    except ValueError:
        print("Error: You must be using PowerShell to run QOS.")
        sys.exit(1)

def activate_venv():
    print("Making virtual environment...")
    os.system('python -m venv qosvenv')
    print("Activating requirements...")
    if pfs == 'windows':
        os.system('.\\qosvenv\\Scripts\\activate.ps1')
    else:
        os.system('source qosvenv/bin/activate')

def ins_req():
    print("Installing requirements...")
    os.system('pip install -r requirements.txt')
    print("QOS is ready to use.")

def make_path():
    old_path = os.getcwd()
    new_path = os.path.join(old_path, "QOS")
    os.chdir(new_path)

def run_qos():
    if pfs == 'windows':
        os.system('python qos.py')
    else:
        os.system('python3 qos.py')

def main():
    activate_venv()
    ins_req()
    make_path()
    try:
        run_qos()
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    main()
