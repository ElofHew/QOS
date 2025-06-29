# Quarter OS 快速使用指南

## 下载安装

下载QOS Release：[GitHub Release](https://github.com/ElofHew/QOS/releases)

如果你想参与开发，可以直接下载源代码：[GitHub Repository](https://github.com/ElofHew/QOS)

 （注意，可能遇到bug或不稳定的功能，请不要在生产环境中使用）

终端运行：`git clone https://github.com/ElofHew/QOS.git`

## 配置并启动QOS

### ① 安装Python 3.10及以上版本

请详阅 [Python3 安装帮助](../HelpDocs/Install_Python3.md)

### ② 配置一个Python虚拟环境

请详阅 [Python虚拟环境帮助](../HelpDocs/Set_PythonVenv.md)

### ③ 激活虚拟环境

``` powershell
# Windows
# 例如虚拟环境名为 qosvenv
.\qosvenv\Scripts\Activate.ps1
```

``` bash
# Linux/macOS
# 例如虚拟环境名为 qosvenv
source qosvenv/bin/activate
```

### ④ 在虚拟环境中安装依赖

找到本存储库根目录的 `requirements.txt` 文件，使用 pip 安装依赖：

``` bash
pip install -r requirements.txt
```

> [!TIP]
> 如果你所在地区访问pypi官方源的速度较慢，可以尝试换源，详阅 [pip换源帮助](../HelpDocs/Change_pip_Mirror.md)

> [!NOTE]
> 【20250629】当前版本：Alpha 0.2，需要的第三方库有：<br>
> colorama、requests<br>
> 可以直接`pip install colorama`、`pip install requests`安装。

### ⑤ 在虚拟环境中运行Quarter OS

**注意，对于Windows系统，请在PowerShell中运行，而非cmd或其他命令行。** Linux/macOS用户请在系统自带的终端中运行。

进入Quarter OS文件夹，并在此处打开终端，输入以下命令：

``` powershell
# Windows
python Quarter OS.py
```

``` bash
# Linux/macOS
python3 Quarter OS.py
```

然后 Quarter OS 就会启动。

## 常用命令

**（系统设置）**

| 命令 | 描述 |
|------|------|
| settings | 打开系统设置 |

**（不需要参数的命令）**

| 命令 | 描述 |
|------|------|
| pwd  | 显示当前工作目录 |
| cwd  | 显示真实的当前工作目录 |
| help | 显示可用命令列表 |
| about | 显示关于QOS的信息 |
| version | 显示QOS的系统版本 |
| whoami  | 显示当前用户 |
| time  | 显示当前时间 |
| date  | 显示当前日期 |
| sysinfo | 显示系统信息 |
| clear | 清空控制台 |
| exit  | 退出QOS |

**（需要参数的命令）**

| 命令 | 描述 | 用法 |
|------|------|------|
| cat  | 显示文件内容 | cat <文件名> |
| echo | 在控制台上显示消息 | echo <消息> |
| cp   | 复制文件或目录 | cp <源文件/目录> <目标文件/目录> |
| mv   | 移动文件或目录 | mv <源文件/目录> <目标文件/目录> |
| ls   | 显示目录中的文件和目录列表 | ls <目录(空则当前目录)> |
| cd   | 更改当前目录 | cd <目录> |
| touch| 创建新文件 | touch <文件名> |
| edit | 编辑文件 | edit <文件名> |
| mkdir| 创建新目录 | mkdir <目录名> |
| rename | 重命名文件或目录 | rename <源文件/目录> <目标文件/目录> |
| rm   | 删除文件或目录 | rm <文件/目录> |

**（Biscuit软件包管理器）**

| 命令 | 描述 |
|------|------|
| biscuit | Quarter OS包管理器 |
| pkg/bkt/bpm/pm | 调用Biscuit的易记别名 |
| biscuit install <软件包名> | 安装软件包 |
| biscuit remove <软件包名> | 卸载软件包 |
| biscuit search <软件包名> | 搜索软件包 |
| biscuit list | 列出已安装的软件包 |
| biscuit get <软件包名> | 下载软件包（未实现） |
| biscuit mirror | 更改软件包镜像源（未实现） |

**（兼容PYOSI的Shizuku软件包管理器）**

| 命令 | 描述 |
|------|------|
| shizuku | PY OS改进的包管理器，适用于Quarter OS |
| szk     | 调用Shizuku的易记别名 |
| shizuku install <软件包名> | 安装软件包 |
| shizuku remove <软件包名> | 卸载软件包 |
| shizuku list | 列出已安装的软件包 |
| shizuku run <软件包名> | 启动Shizuku软件包 |

## 内置账户密码

通常情况下，当你第一次启动Quarter OS时，它会进入OOBE（Out-of-Box Experience，即开箱即用）阶段，会让你创建一个用户名和密码。所以不需要用到内置的 `root`、`admin`、`guest` 等账户。但在这里也列出这些账户的密码以备用：

- root：`123456`
- admin：`123456`
- guest：`无密码`

------

<div align="center">

Written by [ElofHew](https://github.com/ElofHew)

&copy; 2025 [Oak Studio](https://t.me/oakstdcn). All rights reserved.

</div>