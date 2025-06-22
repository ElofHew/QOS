<div align="center">

# QOS

A Professional **Fake-OS** Powered by Python 3

</div>

## 介绍

QOS 是一款基于 Python 3 的伪操作系统，由 [ElofHew](https://github.com/ElofHew) 开发。（[Oak Studio](https://t.me/oakstd) 版权所有）

## 安装指南

### 安装 Python 3

#### 推荐使用 Python 3.12 及以上版本。

**对于 Windows 用户**

前往 [Python 官网](https://www.python.org/downloads/) 或 [阿里云镜像源](https://mirrors.aliyun.com/python-release/) 下载安装包。

下载完成后直接安装即可。

> 注意：安装界面中，请勾选 `Add Python 3.x to PATH` 选项。

**对于 macOS 用户**

使用 Homebrew 安装 Python：

``` bash
brew install python3
```

**对于 Linux 用户**

请根据您的发行版的包管理器安装 Python。

Debian/Ubuntu：

``` bash
sudo apt-get install python3
```

CentOS/Fedora：

``` bash
sudo dnf install python3
```

Arch Linux：

``` bash
sudo pacman -S python3
```

## 安装依赖

找到本存储库根目录的 `requirements.txt` 文件，使用 pip 安装依赖：

``` bash
pip install -r requirements.txt
```

> [!TIP]
> 如果你所在地区访问pypi速度较慢，可以尝试换源，比如 [清华大学镜像源](https://mirrors.tuna.tsinghua.edu.cn/help/pypi/) 或 [阿里云镜像源](https://developer.aliyun.com/mirror/pypi)。

> [!NOTE]
> 【20250622】当前版本：Alpha 0.1，需要的第三方库有：<br>
> colorama<br>
> 可以直接`pip install colorama`安装。

## 运行 QOS

找到本存储库以后，进入QOS文件夹下的system文件夹，并在此处打开终端，输入以下命令：

**Windows**

``` bash
python qos.py
```

**macOS/Linux**

``` bash
python3 qos.py
```

然后 QOS 就会启动。

## 补充说明

QOS 当前版本处于开发阶段（Alpha），功能不完善，如有bug或建议，欢迎提交 issue。

**账户及密码**

root：123456

admin：123456

guest：无

<hr>

<div align="center">

&copy; 2025 [Oak Studio](https://t.me/oakstd). All rights reserved.

</div>