# Quarter OS 软件包开发帮助文档

## 软件包概述

在Quarter OS中，提供了第三方软件包管理器 `Biscuit`，它可以帮助用户轻松地安装、卸载第三方软件包。

Biscuit 软件包管理器支持的软件包类型为 `.qap`。

**QAP**，全称为 **Quarter OS Application Package**，是一种适用于Biscuit Package Manager for Quarter OS的软件包格式。

## 软件包打包封装

开发 QAP 软件包非常简单，只需要将你写好的Python程序和其他相关文件，通过 **QAP 软件包封装器**（devtool/qap_maker.py） 进行打包即可。

### 软件包封装器

QAP 软件包封装器位于 `devtool` 目录下，可以将Python程序打包为QAP软件包。

### 软件包封装原理

使用 `zipfile` 模块将所有程序文件压缩成 `.zip` 压缩包，并重命名为 `packagename_version.qap` 。

### 软件包结构

QAP 软件包的结构如下：

```txt
QAP_Package/
├── [主要文件] main.py
├── [主要文件] info.json
├── README.md
├── [其他文件]
└── ……
```

### 软件包主程序

`main.py`是一个QAP软件包的主程序，它是在Quarter OS启动第三方软件包时运行的程序。

我们建议您将程序各个功能模块化/函数化，并在 `main.py` 中调用。

比如：

```python
import requests

def get_data():
    url = "https://example.com/api/data"
    response = requests.get(url)
    return response.json()

def main():
    data = get_data()
    print(data)

if __name__ == "__main__":
    main()
```

未来的QAP软件包封装器可能会自动将 `xxx.py` 编译为 `xxx.pyc`，以提高运行效率并保护您的程序源代码。

### 软件包基本信息文件

你需要准备一个 `info.json` 文件，结构如下：

```json
{
    "name": "your_package_name",
    "version": "1.0",
    "author": "your_name",
    "description": "The description of your package",
    "category": "tools",
    "min_python_version": "3.10",
    "target_python_version": "3.12",
    "comptb_os": "windows",
    "biscuit_version": "1.0",
    "tags": [
        "tools",
        "python"
    ],
    "depends": [
        "requests"
    ]
}
```

`name` ：软件包名称

`version` ：软件包版本号

`author` ：软件包作者

`description` ：软件包描述

`category` ：软件包分类

`min_python_version` ：软件包最低支持的Python版本

`target_python_version` ：软件包目标Python版本

`comptb_os` ：软件包兼容最佳的操作系统

`biscuit_version` ：软件包兼容最佳的Biscuit版本

`tags` ：软件包标签

`depends` ：软件包依赖的第三方模块

> [!TIP]
> 当你使用 `qap_maker.py` 工具打包时，如果你还没准备好 `info.json` 文件，`qap_maker.py` 工具会帮助你在封装器中生成一个，你只需要根据提示手动输入这些信息就可以了。

### 软件包名称（包名）

QAP 软件包的包名只能包含 **小写字母，数字和下划线**，并且必须以 **小写字母** 开头。

例如：`example`、`my_package`、`demo_package2` 等。

### 软件包分类

QAP 软件包的分类可以是以下几种：

- `Tools`：工具类软件包
- `Games`：游戏类软件包
- `Amusement`：娱乐类软件包
- `Education`：教育类软件包
- `Others`：其他类软件包

### 软件包标签

QAP 软件包的标签可以自定义，目前Biscuit不会读取标签以实现某些功能。

## 第三方软件包程序开发

### 头部注释

我们建议您在程序的头部添加注释，显示出软件包的名称、版本、作者、描述等信息。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Name: your_package_name
@Version: 1.0
@Author: Your_Name
@Description: The description of your package.
"""

def main():
    print("Hello, world!")

if __name__ == "__main__":
    main()
```

### 报错捕捉

我们建议您在程序中添加错误捕捉机制，避免您的程序因发生错误崩溃，这会产生不好的用户体验，甚至可能波及Quarter OS的运行。

```python
try:
    # 你的程序代码
except KeyboardInterrupt:
    print("Program terminated by user.")
    exit()
except Exception as e:
    print("An error occurred:", e)
    exit()
```

其中，`KeyboardInterrupt` 是用户按下 `Ctrl+C` 产生的异常，我们十分建议您捕捉并处理它，以避免程序因用户的意外操作而崩溃。要注意的是，我们建议您使用 `exit()` 函数退出程序，而不是 `sys.exit()` 函数，避免产生其他的Quarter OS异常。

### 程序测试

我们建议您在开发完成后，测试运行您的程序，确保其正常运行。如果您的程序尚未完成测试，请在封装的时候将软件包名后面加上 `_dev`、`_test` 或 `_beta` 后缀，以表明该软件包还在开发中。

例如：`my_package_dev`、`my_package_test`、`my_package_beta` 等。

## 第三方软件包发布（敬请期待）

（敬请期待，Quarter OS 软件包管理器将在后续版本中支持第三方软件包商店，用户可以从商店下载、安装、更新第三方软件包。）

（当前版本的Quarter OS软件包管理器仅支持本地安装第三方软件包，用户可以 `biscuit install /path/to/your_package.qap` 来安装软件包。）

------

<div align="center">

Written by [ElofHew](https://github.com/ElofHew)

&copy: 2025 [Oak Studio](https://t.me/oakstdcn). All rights reserved.

</div>