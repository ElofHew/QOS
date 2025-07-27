# Python 3 虚拟环境配置帮助

## 完整安装 Python 3

详见 [Python 3 安装帮助](Install_Python3.md)

## 创建虚拟环境

也许您的设备上已经创建过虚拟环境了，也可能没有。无论怎样，我们都建议您**专门创建一个只用于 Quarter OS 的 Python 3 虚拟环境**。

### 对于Windows

```powershell
# 打开PowerShell，cd到一个合适的位置，例如：
cd D:\QOS

# 然后创建虚拟环境，例如：
python -m venv qosvenv 
# qosvenv是虚拟环境的名称
```

### 对于macOS和Linux

```bash
# 打开终端，cd到一个合适的位置，例如：
cd ~/QOS

# 然后创建虚拟环境，例如：
python3 -m venv qosvenv 
# qosvenv是虚拟环境的名称
```

## 激活虚拟环境

创建虚拟环境后，我们需要激活它。

### 对于Windows

```powershell
# 打开PowerShell，cd到虚拟环境所在目录，例如：
cd D:\QOS\qosvenv

# 然后激活虚拟环境，例如：
.\Scripts\activate.ps1
```

你也可以在执行Python命令时，直接指定虚拟环境的Python解释器，例如：

```powershell
# 打开PowerShell，cd到你将运行Python程序的目录，例如：
cd D:\QOS\QOS

# 然后运行Python程序，指定虚拟环境，例如：
D:\QOS\qosvenv\Scripts\python.exe qos.py
# qos.py是你要运行的Python程序，前面的文件路径指向的就是虚拟环境中的Python解释器。
```

### 对于macOS和Linux

```bash
# 打开终端，cd到虚拟环境所在目录，例如：
cd ~/QOS/qosvenv

# 然后激活虚拟环境，例如：
source bin/activate
```

你也可以在执行Python命令时，直接指定虚拟环境的Python解释器，例如：

```bash
# 打开终端，cd到你将运行Python程序的目录，例如：
cd ~/QOS/QOS

# 然后运行Python程序，指定虚拟环境，例如：
~/QOS/qosvenv/bin/python qos.py
# qos.py是你要运行的Python程序，前面的文件路径指向的就是虚拟环境中的Python解释器。
```

## 安装Quarter OS所需的Python包

激活虚拟环境后，我们需要安装Quarter OS所需的Python包。

> [!TIP]
> 在进入虚拟环境前，建议根据您所在的网络环境，决定是否换源。详见 [pip换源帮助](Change_pip_Mirror.md)

### 激活环境法

**Windows**

```powershell
# 先激活虚拟环境
.\Scripts\activate.ps1

# cd到Quarter OS的目录，例如：
cd D:\QOS

# 然后安装Quarter OS所需的Python包
pip install -r requirements.txt
```

**macOS和Linux**

```bash
# 先激活虚拟环境
source bin/activate

# cd到Quarter OS的目录，例如：
cd ~/QOS

# 然后安装Quarter OS所需的Python包
pip3 install -r requirements.txt
```

### 直接调用法

**Windows**

```powershell
# cd到Quarter OS的目录，例如：
cd D:\QOS

# 直接调用Python，指定虚拟环境，安装Quarter OS所需的Python包
D:\QOS\qosvenv\Scripts\pip install -r requirements.txt
```

**macOS和Linux**

```bash
# cd到Quarter OS的目录，例如：
cd ~/QOS

# 直接调用Python，指定虚拟环境，安装Quarter OS所需的Python包
~/QOS/qosvenv/bin/pip3 install -r requirements.txt
```

## 常见问题

### 如何退出虚拟环境？

**Windows**

```powershell
# 退出虚拟环境
deactivate
```

**macOS和Linux**

```bash
# 退出虚拟环境
deactivate
```

### 如何删除虚拟环境？

**Windows**

```powershell
# 打开PowerShell，cd到虚拟环境所在目录，例如：
cd D:\QOS\qosvenv

# 然后删除虚拟环境，例如：
Remove-Item -Recurse -Force qosvenv
```

**macOS和Linux**

```bash
# 打开终端，cd到虚拟环境所在目录，例如：
cd ~/QOS/qosvenv

# 然后删除虚拟环境，例如：
rm -rf qosvenv
```

### 如何安装Quarter OS？

请参见 [Quarter OS 安装帮助](Install_QuarterOS.md)

------

<div align="center">

Written by [ElofHew](https://github.com/ElofHew).

&copy; 2025 [Oak Studio](https://os.drevan.xyz/). All rights reserved.

</div>
