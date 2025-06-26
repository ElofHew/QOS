# Python 3 安装帮助

***推荐使用 Python 3.12 及以上版本。***

***Quarter OS 最低支持 Python 3.10 版本！***

## 对于 Windows 用户

**（Windows最低支持Windows 8.1）**

### ① 前往 [Python 官网](https://www.python.org/downloads/) 或 [阿里云镜像源](https://mirrors.aliyun.com/python-release/) 下载 `exe` 或 `msi` 安装包。

![Python 下载页面](../img/pythonorg.png)

下载完成后直接安装即可。

> 注意：安装界面中，请勾选 `Add Python 3.x to PATH` 选项。

---

### ② （对于 Windows 10/11 用户）通过`winget`命令安装（Windows 10/11）：

``` powershell
# 查找Python版本
winget search Python.Python
# 比如要下载Python3.12
winget install --id Python.Python.3.12 --source winget --scope machine
```

### ③ （对于 Windows 10/11 用户）直接在Microsoft Store搜索 `Python 3` 安装。

![Python 3 安装](../img/msstore.png)

## 对于 macOS 用户

**（macOS最低支持 macOS 10.9 Mavericks）**

### ① 前往 [Python 官网](https://www.python.org/downloads/) 或 [阿里云镜像源](https://mirrors.aliyun.com/python-release/) 下载 `dmg` 安装包。

![Python 下载页面](../img/pythonorg.png)

### ② 或者使用 Homebrew 安装 Python3：

``` bash
# 因为macOS内置Python2，所以这里要安装"python3"
brew install python3
```

## 对于 Linux 用户

**（Linux最低支持 glibc 2.17，若低于该版本需自行编译）**

### 请根据您的发行版的包管理器安装 Python3：

### Debian/Ubuntu：

**（最低支持：Debian 10 Buster、Ubuntu 20.04 LTS Focal）**

``` bash
sudo apt-get install python3
```

### CentOS/Fedora：

**（最低支持：CentOS 8 Stream、Fedora 32）**

``` bash
sudo dnf install python3
```

Arch Linux：

**（最低支持：未知）**

``` bash
sudo pacman -S python3
```

------

<div align="center">

Written by [ElofHew](https://github.com/ElofHew).

&copy; 2025 [Oak Studio](https://t.me/oakstdcn). All rights reserved.

</div>
