"""
# Quarter Operation System (QOS)
# 1 Step to run
@ Author: ElofHew aka Dan_Evan
@ Date: 2025-08-02
@ Version: 0.2.2
"""

import os
import sys
import platform
import subprocess

def main():
    # WARNING
    print("WARNING: This script will be deprecated in the future. Please use Leaf Boot Manager (LBM) instead.")
    print("WARNING: And if you really want to use this script, please input 'I understand' to continue.")
    if input("> ") != "I understand":
        input("Press any key to exit...")
        sys.exit(1)

    # Check system environment (Windows: must be Windows 10 or higher, and using PowerShell; other systems not checked)
    pfs = platform.system().lower()
    work_path = os.path.dirname(os.path.realpath(__file__))
    now_path = os.getcwd()

    if work_path != now_path:
        print("Error: Please run this script in the QOS directory.")
        sys.exit(1)

    if pfs == 'windows':
        try:
            if platform.release() < '10':
                raise ValueError("You must be using Windows 10 or higher to run QOS.")
            if not os.getenv('PSModulePath'):
                raise IndexError("You must be using PowerShell to run QOS.")
        except (ValueError, IndexError) as e:
            print(f"Error: {e}")
            sys.exit(1)

    # Check environment (repository exists, Python version is 3.10 or higher)
    try:
        if not os.path.exists(os.path.join(work_path, "qos.py")):
            raise FileNotFoundError("QOS not found. Please check QOS directory.")
        if not sys.version_info >= (3, 10):
            raise ValueError("Python version must be 3.10 or higher.")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Create/check virtual environment
    venv_path = os.path.join(work_path, "qosvenv", "Scripts" if pfs == 'windows' else "bin")

    try:
        if not os.path.exists('qosvenv'):
            print("Making virtual environment...")
            subprocess.check_call(["python" if pfs == 'windows' else "python3", "-m", "venv", "qosvenv"])
        print("Found virtual environment.")
    except FileNotFoundError:
        print("Error: Virtual environment not found. Please check QOS directory.")
        sys.exit(1)

    # Check/install requirements
    try:
        print("Checking and installing requirements...")
        subprocess.check_call([os.path.join(venv_path, 'python.exe' if pfs == 'windows' else 'python'), '-m', 'pip', 'install', '-r', os.path.join(work_path, 'requirements.txt')])
        print("Requirements installed.")
    except Exception as e:
        print("Error: Failed to install requirements. Please check your internet connection or try again later.")
        print(e)
        sys.exit(1)

    print("=============================")
    print(" Quarter OS is ready to use. ")
    print("=============================")

    # Run QOS.py
    try:
        subprocess.check_call([os.path.join(venv_path, 'python.exe' if pfs == 'windows' else 'python'), 'qos.py'])
    except FileNotFoundError as e:
        print("Error: QOS.py not found. Please check QOS directory.")
        sys.exit(1)

if __name__ == "__main__":
    main()
