# QAP Maker - Main Code
"""
# Quarter OS Biscuit Application Package Maker
@ Auther: Dan_Evan aka Dr.Evan aka ElofHew
@ Version: 1.0.0
$ Date: 2025.06.27
"""

qm_ver = "1.0"

import os
import sys
import time
import json
import shutil
import zipfile
import platform
from colorama import init, Fore, Back, Style

pfs = platform.system()

init(autoreset=True)

def view_qap():
    try:
        if os.path.exists("temp"):
            shutil.rmtree("temp")
        print(Fore.LIGHTBLUE_EX + "Please enter the path of qap file to view: " + Fore.RESET)
        while True:
            try:
                view_file_path = input("> ")
                if view_file_path == "exit":
                    return 1
                elif os.path.exists(view_file_path):
                    break
                else:
                    print(Fore.RED + "Error: File not found." + Fore.RESET)
                    return 1
            except Exception as e:
                print(Fore.RED + "Error: " + str(e) + Fore.RESET)
                sys.exit(0)
            except KeyboardInterrupt:
                print(Fore.RED + "KeyboardInterrupt: User Terminated." + Fore.RESET)
                sys.exit(0)
        # Unzipping the qap file
        try:
            with zipfile.ZipFile(view_file_path, 'r') as zipf:
                zipf.extractall(path="temp")
            with open(os.path.join("temp", "info.json"), "r") as f:
                info_json = json.load(f)
                app_name = info_json["name"]
                app_version = info_json["version"]
                app_vcode = info_json["version_code"]
                app_author = info_json["author"]
                app_desc = info_json["description"]
                app_category = info_json["category"]
                app_min = info_json["min_python_version"]
                app_target = info_json["target_python_version"]
                app_compat = info_json["comptb_os"]
                app_bktver = info_json["biscuit_version"]
                # Multi Value Support
                app_tags_list = info_json["tags"]
                app_depends_list = info_json["depends"]
                # Initalizing Variables
                app_tags = [] if app_tags_list is not None else "None"
                for tags in app_tags_list:
                    app_tags.append(tags)
                app_depends = [] if app_depends_list is not None else "None"
                for depends in app_depends_list:
                    app_depends.append(depends)
                # Convert empty values to None
                app_name = str(app_name) if app_name is not None else "None"
                app_version = str(app_version) if app_version is not None else "None"
                app_vcode = str(app_vcode) if app_vcode is not None else "None"
                app_author = str(app_author) if app_author is not None else "None"
                app_desc = str(app_desc) if app_desc is not None else "None"
                app_category = str(app_category) if app_category is not None else "None"
                app_min = str(app_min) if app_min is not None else "None"
                app_target = str(app_target) if app_target is not None else "None"
                app_compat = str(app_compat) if app_compat is not None else "None"
                app_bktver = str(app_bktver) if app_bktver is not None else "None"
            # Printing the values
            print(Fore.LIGHTBLUE_EX + "Application Name: " + Fore.GREEN + app_name + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Version: " + Fore.GREEN + app_version + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Version Code: " + Fore.GREEN + app_vcode + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Author: " + Fore.GREEN + app_author + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Description: " + Fore.GREEN + app_desc + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Category: " + Fore.GREEN + app_category + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Minimum Python Version: " + Fore.GREEN + app_min + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Target Python Version: " + Fore.GREEN + app_target + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Compatible OS: " + Fore.GREEN + app_compat + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Biscuit PM Version: " + Fore.GREEN + app_bktver + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Tags: " + Fore.GREEN + str(app_tags_list) + Fore.RESET)
            print(Fore.LIGHTBLUE_EX + "Application Dependencies: " + Fore.GREEN + str(app_depends_list) + Fore.RESET)
            # Press any key to continue
            input(Fore.GREEN + "(Press any key to continue.)" + Fore.RESET)
            shutil.rmtree("temp")
            return 1
        except Exception as e:
            print(Fore.RED + "Error: " + str(e) + Fore.RESET)
            return 1
    except KeyboardInterrupt:
        print(Fore.RED + "KeyboardInterrupt: User Terminated." + Fore.RESET)
        sys.exit(0)

def create_qap_progress(app_files_dir, app_name, app_version):
    print(Fore.LIGHTBLUE_EX + "Creating Quarter OS Biscuit Application Package..." + Fore.RESET)
    try:
        output_dir = os.path.join(os.getcwd(), "output")
        compressed_file_name = f"{app_name}_{app_version}.zip"
        output_path = os.path.join(output_dir, compressed_file_name)
        output_file_name = output_path.replace(".zip", ".qap")
        try:
            shutil.make_archive(output_path.replace('.zip', ''), 'zip', app_files_dir)
            print(Fore.LIGHTGREEN_EX + "Successfully Compressed the Application Package." + Fore.RESET)
            try:
                qap_path = os.path.abspath(f"{output_file_name}")
                if os.path.exists(qap_path):
                    os.remove(output_file_name)
                    os.rename(output_path, output_file_name)
                    print(f"{Fore.LIGHTGREEN_EX}Package '{output_file_name}' successfully packaged.")
                    print(f"{Fore.GREEN}Package output path: {Fore.LIGHTBLUE_EX}{qap_path}{Fore.RESET}")
                else:
                    os.rename(output_path, output_file_name)
                    print(f"{Fore.LIGHTGREEN_EX}Package '{output_file_name}' successfully packaged.")
                    print(f"{Fore.GREEN}Package output path: {Fore.LIGHTBLUE_EX}{qap_path}{Fore.RESET}")
                print(f"{Fore.MAGENTA}Return to main menu in 5 seconds...{Fore.RESET}")
                time.sleep(5)
                return 1
            except FileNotFoundError:
                print(f"{Fore.RED}Error: File '{compressed_file_name}' not found.{Fore.RESET}")
                return 0
            except Exception as e:
                print(f"{Fore.RED}Error: {e}{Fore.RESET}")
                return 0
        except Exception as e:
            print(f"{Fore.RED}Error: {e}{Fore.RESET}")
            return 0
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Fore.RESET}")
        return 0

def create_qap_print_info(app_files_dir):
    try:
        with open(os.path.join(app_files_dir, "info.json"), "r") as f:
            info_json = json.load(f)
            # 11 Values in total
            app_name = info_json["name"]
            app_version = info_json["version"]
            app_vcode = info_json["version_code"]
            app_author = info_json["author"]
            app_desc = info_json["description"]
            app_category = info_json["category"]
            app_min = info_json["min_python_version"]
            app_target = info_json["target_python_version"]
            app_compat = info_json["comptb_os"]
            app_bktver = info_json["biscuit_version"]
            # Multi Value Support
            app_tags_list = info_json["tags"]
            app_depends_list = info_json["depends"]
            # Initalizing Variables
            app_tags = [] if app_tags_list is not None else "None"
            for tags in app_tags_list:
                app_tags.append(tags)
            app_depends = [] if app_depends_list is not None else "None"
            for depends in app_depends_list:
                app_depends.append(depends)
            # Convert empty values to None
            app_name = str(app_name) if app_name is not None else "None"
            app_version = str(app_version) if app_version is not None else "None"
            app_vcode = str(app_vcode) if app_vcode is not None else "None"
            app_author = str(app_author) if app_author is not None else "None"
            app_desc = str(app_desc) if app_desc is not None else "None"
            app_category = str(app_category) if app_category is not None else "None"
            app_min = str(app_min) if app_min is not None else "None"
            app_target = str(app_target) if app_target is not None else "None"
            app_compat = str(app_compat) if app_compat is not None else "None"
            app_bktver = str(app_bktver) if app_bktver is not None else "None"
        # Printing the values
        print(Fore.LIGHTBLUE_EX + "Application Name: " + Fore.GREEN + app_name + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Version: " + Fore.GREEN + app_version + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Version Code: " + Fore.GREEN + app_vcode + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Author: " + Fore.GREEN + app_author + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Description: " + Fore.GREEN + app_desc + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Category: " + Fore.GREEN + app_category + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Minimum Python Version: " + Fore.GREEN + app_min + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Target Python Version: " + Fore.GREEN + app_target + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Compatible OS: " + Fore.GREEN + app_compat + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Biscuit PM Version: " + Fore.GREEN + app_bktver + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Tags: " + Fore.GREEN + str(app_tags_list) + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "Application Dependencies: " + Fore.GREEN + str(app_depends_list) + Fore.RESET)
        # Confirm
        print(Fore.GREEN + "Is these information correct? (Y/N)" + Fore.RESET)
        while True:
            try:
                confirm_info = str(input(Fore.YELLOW + "> " + Fore.RESET))
                if confirm_info.lower() == "y":
                    return 1
                elif confirm_info.lower() == "n":
                    return 0
                else:
                    print(Fore.RED + "Invalid input! Please enter 'Y' or 'N'." + Fore.RESET)
                    continue
            except KeyboardInterrupt:
                print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
                sys.exit(0)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

def create_qap_make_info_json(app_files_dir):
    try:
        app_name = str(input(Fore.YELLOW + "Enter the name of your application: " + Fore.RESET))
        app_version = str(input(Fore.YELLOW + "Enter the version of your application: " + Fore.RESET))
        app_vcode = str(input(Fore.YELLOW + "Enter the version code of your application: " + Fore.RESET))
        app_author = str(input(Fore.YELLOW + "Enter the author of your application: " + Fore.RESET))
        app_desc = str(input(Fore.YELLOW + "Enter a brief description of your application: " + Fore.RESET))
        app_category = str(input(Fore.YELLOW + "Enter the category of your application: " + Fore.RESET))
        app_min = str(input(Fore.YELLOW + "Enter the minimum Python version required for your application: " + Fore.RESET))
        app_target = str(input(Fore.YELLOW + "Enter the target Python version for your application: " + Fore.RESET))
        app_compat = str(input(Fore.YELLOW + "Enter the compatible OS for your application: " + Fore.RESET))
        app_bktver = str(input(Fore.YELLOW + "Enter the version of the Quarter OS Biscuit you are using: " + Fore.RESET))
        # Multi Value Support
        app_tags = str(input(Fore.YELLOW + "Enter the tags of your application (separated by commas): " + Fore.RESET))
        app_depends = str(input(Fore.YELLOW + "Enter the dependencies of your application (separated by commas): " + Fore.RESET))
        # Converting comma separated values to lists
        app_tags_list = [tag.strip() for tag in app_tags.split(",")]
        app_depends_list = [depend.strip() for depend in app_depends.split(",")]
        # Removing any extra spaces
        app_name = app_name.strip()
        app_version = app_version.strip()
        app_author = app_author.strip()
        app_desc = app_desc.strip()
        app_category = app_category.strip()
        app_min = app_min.strip()
        app_target = app_target.strip()
        app_compat = app_compat.strip()
        app_bktver = app_bktver.strip()
        app_tags = app_tags.strip()
        app_depends = app_depends.strip()
        # Creating the info.json file
        info_json = {
            "name": app_name,
            "version": app_version,
            "version_code": app_vcode,
            "author": app_author,
            "description": app_desc,
            "category": app_category,
            "min_python_version": app_min,
            "target_python_version": app_target,
            "comptb_os": app_compat,
            "biscuit_version": app_bktver,
            "tags": app_tags_list,
            "depends": app_depends_list
        }
        # Writing the info.json file
        with open(os.path.join(app_files_dir, "info.json"), "w") as f:
            json.dump(info_json, f, indent=4)
        info_confirm = create_qap_print_info(app_files_dir)
        if info_confirm == 1:
            progress = create_qap_progress(app_files_dir, app_name, app_version)
            if progress == 1:
                return 1
            else:
                return 0
        elif info_confirm == 0:
            input(Fore.YELLOW + "Press enter to retry.\n" + Fore.RESET)
            return create_qap_make_info_json(app_files_dir)
        else:
            print(Fore.RED + "Unknown error occurred." + Fore.RESET)
            sys.exit(0)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

def create_qap_read_info_json(app_files_dir):
    try:
        with open(os.path.join(app_files_dir, "info.json"), "r") as f:
            info_json = json.load(f)
            # List a part of the values
            app_name = info_json["name"]
            app_version = info_json["version"]
        info_confirm = create_qap_print_info(app_files_dir)
        if info_confirm == 1:
            progress = create_qap_progress(app_files_dir, app_name, app_version)
            if progress == 1:
                return 1
            else:
                return 0
        elif info_confirm == 0:
            input(Fore.YELLOW + "Please edit the 'info.json', and press enter to retry.\n" + Fore.RESET)
            return create_qap_read_info_json(app_files_dir)
        else:
            print(Fore.RED + "Unknown error occurred." + Fore.RESET)
            sys.exit(0)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

def create_qap_check_files(app_files_dir):
    try:
        if not os.path.exists(os.path.join(app_files_dir, "main.py")):
            print(Fore.RED + "Error: 'main.py' not found in the current directory." + Fore.RESET)
            return 0
        if not os.path.exists(os.path.join(app_files_dir, "info.json")):
            print(Fore.YELLOW + "WARNING: 'info.json' not found. " + Fore.CYAN + "Would you like to create one by this program? (Y/N)" + Fore.RESET)
            while True:
                try:
                    create_info_json = str(input("> "))
                    if create_info_json.lower() == "y":
                        make_pg = create_qap_make_info_json(app_files_dir)
                        if make_pg == 1:
                            return 1
                        else:
                            return 0
                    elif create_info_json.lower() == "n":
                        print(Fore.RED + "Error: 'info.json' not found. Please put it in the current directory and try again." + Fore.RESET)
                        return 0
                    else:
                        print(Fore.RED + "Invalid choice! Please try again." + Fore.RESET)
                        continue
                except KeyboardInterrupt:
                    print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
                    sys.exit(0)
        if (os.path.exists(os.path.join(app_files_dir, "main.py") and os.path.exists(os.path.join(app_files_dir, "info.json")))):
            read_pg = create_qap_read_info_json(app_files_dir)
            if read_pg == 1:
                return 1
            else:
                return 0
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

def create_qap():
    try:
        if os.path.exists("app_files"):
            pass
        else:
            os.mkdir("app_files")
        working_dir = os.getcwd()
        app_files_dir = os.path.join(working_dir, "app_files")
        print(Fore.LIGHTBLUE_EX + "Now please put your application files in the 'app_files' folder." + Fore.RESET)
        print(Fore.LIGHTGREEN_EX + "The directory is at: \n" + Fore.GREEN + app_files_dir + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "When you are done, press enter to continue." + Fore.RESET)
        input("(Press enter to continue)")
        print(Fore.LIGHTBLUE_EX + "Creating QAP..." + Fore.RESET)
        check_pg = create_qap_check_files(app_files_dir)
        if check_pg == 1:
            return 1
        else:
            sys.exit(0)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

def main():
    try:
        while True:
            if pfs == "Windows":
                os.system("cls")
            elif pfs == "Linux" or pfs == "Darwin":
                os.system("clear")
            else:
                os.system("clear")
            print(Style.DIM + Fore.GREEN + "Quarter OS Biscuit Application Package Maker")
            print(Fore.MAGENTA + "% QAP Maker - " + qm_ver + " %" + Fore.RESET)
            print(Fore.CYAN + "1. Create a new QAP" + Fore.RESET)
            print(Fore.CYAN + "2. View info of QAP" + Fore.RESET)
            print(Fore.CYAN + "0. Exit" + Fore.RESET)
            main_choice = str(input(Fore.YELLOW + "> " + Fore.RESET))
            if main_choice == "1":
                create_qap()
            elif main_choice == "2":
                view_qap()
            elif main_choice == "0":
                sys.exit(0)
            else:
                print(Fore.RED + "Invalid choice! Please try again." + Fore.RESET)
    except Exception as e:
        print(Fore.RED + "An error occurred: " + str(e) + Fore.RESET)
        sys.exit(0)
    except KeyboardInterrupt:
        print(Fore.RED + "\nKeyboardInterrupt detected! Exiting..." + Fore.RESET)
        sys.exit(0)

if __name__ == "__main__":
    main()
