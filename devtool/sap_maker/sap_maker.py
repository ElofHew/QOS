"""
# PY OS Improved
# Shizuku Software Manager
# Application Package Maker
@ Auther: Dan_Evan aka Dr.Evan aka ElofHew
@ Version: 1.0.0
$ Date: 2025.05.01
"""

import os,sys,time,json,zipfile

print("="*24)
print("    Choose Languages    ")
print("------------------------")
print("  1. English (US & UK)  ")
print("  2. 简体中文 (中国大陆)  ")
print("------------------------")
while True:
    lang = str(input("> "))
    if str(lang) == "1":
        print("Let's speak English...")
        break
    elif str(lang) == "2":
        print("让我们说中文...")
        break
    else:
        print("Invalid input. Please choose a number from the list.")
        continue

if lang == "1":
    error_text = "Invalid input. Please retry."
    welcome1 = 'Welcome to the PY OS Improved Application Package Maker'
    welcome2 = 'Please read the application development standard before proceeding:\n("pyos-improved/docs/AppDev/DevStd.md")'
    welcome_ask = "Do you want to continue? (Y/N)"
    done_text = "Ready"
    exit_text = "The program will exit in 10s"
    find1 = 'Please place your application files in the "app_files" folder in the current directory.'
    find2 = 'Please make sure that the "app_files" folder contains at least the following files:'
    find3 = '{1} Main program file (main.py)'
    find4 = '{2} Module list file (requirements.txt)'
    find5 = '{3} Application basic information file (info.json)'
    find6 = '{4} Resource files (such as images, audio, video, etc.)'
    find7 = '{5} Application configuration files (such as json, ini, etc.)'
    find8 = '{6} Application documentation file (README.md)'
    app_file1 = '"app_files" folder already exists'
    app_file2 = '"app_files" folder created'
    app_file3 = f'The absolute path of the "app_files" folder is: '
    find9 = 'Please confirm that all the above files have been placed and press any key to continue...'
    check1 = 'Files to be added: '
    check2 = 'All required files exist'
    info0 = 'Application basic information:'
    info1 = 'Package name: '
    info2 = 'Version: '
    info3 = 'Author: '
    info4 = 'Description: '
    info5 = 'Category: '
    info6 = 'Tags: '
    info7 = 'Minimum Python version: '
    info8 = 'Target Python version: '
    info9 = 'Compatible operating systems: '
    info10 = 'Please confirm that the above information is correct and press any key to continue...'
    info_rt = "Returning to the preparation step in 3s..."
    pack1 = 'Packaging the application...'
    pack2 = 'Application compressed successfully...'
    pack3 = f'Application packaging failed: '
    pack4 = f'Compression process encountered an error: '
    pack_file = f'File '
    pack_pack = f'Software package'
    pack_d1 = f'Packaged'
    pack_d2 = f'Not found'
    pack_d3 = f'Already exists'
    pack_output = f'Package output path: '
    pack_retry = "Do you want to retry? (Y/N)"
    main_ask = "Do you want to return to the main menu? (Y/N)"
    return_main = "Returning to the main menu in 10s..."
elif lang == "2":
    error_text = "输入无效。请重试。"
    welcome1 = '欢迎使用 PY OS Improved 应用程序打包工具'
    welcome2 = '请先确保您已经阅读了应用开发标准：\n("pyos-improved/docs/AppDev/DevStd.md")'
    welcome_ask = "是否继续？(Y/N)"
    done_text = "准备就绪"
    exit_text = "程序将在10s后退出"
    find1 = '请将应用程序文件放置于当前目录下的"app_files"文件夹中。'
    find2 = '请确保"app_files"文件夹中至少含有以下文件：'
    find3 = '{1}程序主体文件（main.py）'
    find4 = '{2}模块列表文件（requirements.txt）'
    find5 = '{3}程序基本信息文件（info.json）'
    find6 = '{4}资源文件（如图片、音频、视频等）'
    find7 = '{5}程序配置文件（如json、ini等）'
    find8 = '{6}程序说明文档（README.md）'
    app_file1 = '"app_files"文件夹已存在'
    app_file2 = '"app_files"文件夹已创建'
    app_file3 = f'"app_files"文件夹的绝对路径为: '
    find9 = '请确认以上文件已放置完成并按任意键继续...'
    check1 = '应补充的文件: '
    check2 = '所有必需的文件都已存在'
    info0 = '应用程序基本信息如下：'
    info1 = '包名：'
    info2 = '版本：'
    info3 = '作者：'
    info4 = '描述：'
    info5 = '类别：'
    info6 = '标签：'
    info7 = '最低Python版本：'
    info8 = '目标Python版本：'
    info9 = '兼容操作系统：'
    info10 = '请确认以上信息无误并按任意键继续...'
    info_rt = "3s后返回准备步骤..."
    pack1 = '正在打包应用程序...'
    pack2 = '应用程序压缩成功...'
    pack3 = f'应用程序打包失败: '
    pack4 = f'压缩过程出现错误: '
    pack_file = f'文件 '
    pack_pack = f'软件包'
    pack_d1 = f'已打包完毕'
    pack_d2 = f'未找到'
    pack_d3 = f'已经存在'
    pack_output = f'软件包输出路径: '
    pack_retry = "是否重试？(Y/N)"
    main_ask = "是否返回主菜单？(Y/N)"
    return_main = "10s后返回主菜单..."

with open("app_files/info.json", "r", encoding="utf-8") as f:
    app_info = json.load(f)
    app_name = app_info.get("name")
    app_version = app_info.get("version")
    app_author = app_info.get("author")
    app_desc = app_info.get("description")
    app_category = app_info.get("category")
    app_tags = app_info.get("tags")
    app_min = app_info.get("min_python_version")
    app_target = app_info.get("target_python_version")
    app_compat = app_info.get("compatible_os")
    # 将None转换为字符串"None"
    app_name = str(app_name) if app_name is not None else "None"
    app_version = str(app_version) if app_version is not None else "None"
    app_author = str(app_author) if app_author is not None else "None"
    app_desc = str(app_desc) if app_desc is not None else "None"
    app_category = str(app_category) if app_category is not None else "None"
    app_tags = str(app_tags) if app_tags is not None else "None"
    app_min = str(app_min) if app_min is not None else "None"
    app_target = str(app_target) if app_target is not None else "None"
    app_compat = str(app_compat) if app_compat is not None else "None"

def pack_apps():
    print("="*30)
    print(pack1)
    # 定义源目录和输出压缩包文件名
    source_directory = "app_files"
    output_archive = app_name + "_" + "v" + app_version + ".zip"
    sap_archive = app_name + "_" + "v" + app_version + ".sap"
    # 创建一个ZIP文件
    try:
        with zipfile.ZipFile(output_archive, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # 遍历源目录下的所有文件并添加到ZIP文件中
            for root, _, files in os.walk(source_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    zipf.write(file_path, os.path.relpath(file_path, source_directory))
        print(pack2)
        # 尝试重命名ZIP文件为SAP文件
        try:
            os.rename(output_archive, sap_archive)
            print(pack_pack + f'{sap_archive}' + pack_d1)
            sap_path = os.path.abspath(f"{sap_archive}")
            print(pack_output + f"{sap_path}")
        except FileNotFoundError:
            print(pack_file + f'{output_archive}' + pack_d2)
        except FileExistsError:
            print(pack_file + f'{sap_archive}' + pack_d3)
            sap_path = os.path.abspath(f"{sap_archive}")
            print(pack_output + f"{sap_path}")
        except Exception as e:
            print(pack4 + f"{e}")
    except Exception as e:
        print(pack3 + f"{e}")
        while True:
            error01 = str(input(pack_retry))
            if error01 == "Y" or error01 == "y":
                return pack_apps()
            elif error01 == "N" or error01 == "n":
                print(return_main)
                time.sleep(10)
                return main()
            else:
                print(error_text)
                continue
    while True:
        choice03 = str(input(main_ask))
        if choice03 == "Y" or choice03 == "y":
            return main()
        elif choice03 == "N" or choice03 == "n":
            print(exit_text)
            time.sleep(10)
            sys.exit()
        else:
            print(error_text)
            continue

def check_app_files():
    while True:
        missing_files = []
        if not os.path.exists("app_files/info.json"):
            missing_files.append("info.json")
        if not os.path.exists("app_files/requirements.txt"):
            missing_files.append("requirements.txt")
        if not os.path.exists("app_files/main.py"):
            missing_files.append("main.py")
        if missing_files:
            print(check1 + ", ".join(missing_files))
            continue
        else:
            print(check2)
            break
    print("="*30)
    print(info0)
    print(info1 + app_name)
    print(info2 + app_version)
    print(info3 + app_author)
    print(info4 + app_desc)
    print(info5 + app_category)
    print(info6 + app_tags)
    print(info7 + app_min)
    print(info8 + app_target)
    print(info9 + app_compat)
    print("="*30)
    while True:
        choice02 = str(input(info10))
        if choice02 == "":
            print(done_text)
            break
        else:
            print(info_rt)
            time.sleep(3)
            return find_app_files()
    pack_apps()

def find_app_files():
    print("="*30)
    print(find1)
    print(find2)
    print(find3)
    print(find4)
    print(find5)
    print(find6)
    print(find7)
    print(find8)
    print("="*30)
    if os.path.exists("app_files"):
        print(app_file1)
    else:
        os.mkdir("app_files")
        print(app_file2)
    app_files_path = os.path.abspath("app_files")
    print(app_file3 + f"{app_files_path}")
    while True:
        choice01 = str(input(find9))
        if choice01 == "":
            print(done_text)
            break
        else:
            print(error_text)
            continue
    check_app_files()

# main function
def main():
    print("="*40)
    print(welcome1)
    print(welcome2)
    while True:
        main01 = str(input(welcome_ask))
        if main01 == "Y" or main01 == "y":
            print(done_text)
            break
        elif main01 == "N" or main01 == "n":
            print(exit_text)
            time.sleep(10)
            sys.exit()
        else:
            print(error_text)
            continue
    find_app_files()

main()
