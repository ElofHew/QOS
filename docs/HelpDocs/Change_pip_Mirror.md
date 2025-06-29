# pip 换源帮助

因为有些地区的网络环境连接到Pypi官方源不稳定或速度很慢（比如中国大陆），所以您可以根据您所在的网络环境**自行决定**是否换源以提升您在安装模块时的网络连接体验

## 常用镜像源

**Pypi官方源**：https://pypi.org/simple/ （用于切换回官方源）

**清华源**：https://pypi.tuna.tsinghua.edu.cn/simple/

**阿里源**：https://mirrors.aliyun.com/pypi/simple/

**华为源**： https://repo.huaweicloud.com/repository/pypi/simple/

**腾讯源**：https://mirrors.cloud.tencent.com/pypi/simple/

**中科大源**：https://pypi.mirrors.ustc.edu.cn/simple/

## 通用方法

### （下面的 `mirror_url` 请替换为镜像站的URL）

在**虚拟环境之外**，首先先更新一遍 pip：

```bash
python -m pip install --upgrade pip
```

如果网络质量不佳，可以先临时使用国内源更新pip：

```bash
python -m pip install -i <mirror_url> --upgrade pip
```

运行以下命令来切换默认镜像源：

```bash
pip config set global.index-url <mirror_url>
```

如果您只是想临时使用镜像源，可以运行以下命令：

```bash
pip install -i <mirror_url> <package_name>
# <package_name> 是你要安装的包的名称
```

如果你想同时保存多个镜像源，可以运行以下命令：

```bash
pip config set global.extra-index-url "<url1> <url2>..."
# <url1> <url2>... 是你要添加的镜像源的URL
# 注意，在本命令中，URL请加英文双引号

# 例如：
pip config set global.extra-index-url "https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple" "https://mirrors.aliyun.com/pypi/simple/"
# 这条命令会将清华源和阿里源添加到镜像源列表中
```

## 常见问题

### 如何查看当前的镜像源？

```bash
pip config list
```

### 如何清空已添加的镜像源列表？

```bash
pip config unset global.index-url
```
> [!WARNING]
>使用本命令后请重新设置镜像源，否则可能导致后续 pip 在安装包时出现错误。

------

<div align="center">

Written by [ElofHew](https://github.com/ElofHew).

&copy; 2025 [Oak Studio](https://t.me/oakstdcn). All rights reserved.

</div>