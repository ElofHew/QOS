# Quarter OS Biscuit 软件包管理器 - 第三方软件源搭建

自Quarter OS Alpha 0.2.1 版本起，Quarter OS 软件包管理器支持第三方软件源，用户可以直接从软件源获取qap包并安装第三方软件。

## 1.软件源架构解释

Quarter OS 软件包管理器的软件源架构如下面所示：

(root为服务器根目录)

```txt
root
├── repo
│   ├── apps.json
│   ├── games
│   │   ├── package.json
│   │   ├── app1
│   │   │   ├── xxx_1.0.qap
│   │   │   ├── xxx_1.1.qap
│   │   │   └──...
│   │   ├── app2
│   │   │   ├── xxx_1.0.qap
│   │   │   ├── xxx_1.1.qap
│   │   │   └──...
│   │   └──...
│   ├── tools
│   │   ├── package.json
│   │   ├── tool1
│   │   │   ├── xxx_1.0.qap
│   │   │   ├── xxx_1.1.qap
│   │   │   └──...
│   │   ├── tool2
│   │   │   ├── xxx_1.0.qap
│   │   │   ├── xxx_1.1.qap
│   │   │   └──...
│   │   └──...
│   └──...
```

由上图可看出，软件源URL格式为 `http://xxx.xxx.xxx/repo` (以repo为仓库目录)

其中，`apps.json` 文件用于定位软件包分类，返回软件包所在的类文件夹名称。

```json
{
    "app1": {
        "category": "games", 
        "latest_version_code": "2000"
    },
    "app2": {
        "category": "tools", 
        "latest_version_code": "1000"
    },
    ...
}
```

定位到软件包的类文件夹后，在对应名称的类文件夹下，有一个 `package.json` 文件，用于记录该下的软件包的基本信息：

```json
{
    "app1": {
        "category": "games",
        "version": ["1.0", "1.1", "2.0"],
        "version_code": ["1000", "1100", "2000"],
        "latest_version": "2.0",
        "latest_version_code": "2000",
        "author": "NAME",
        "description": "An App"
    },
    ...
}
```

其中，`version` 字段记录了软件包的版本号，`version_code` 字段记录了软件包的版本号对应的版本号码，`latest_version` 字段记录了最新版本号，`latest_version_code` 字段记录了最新版本号对应的版本号码。

如果用户端命令没有指明版本，比如：`biscuit get app1`，则自动匹配最新版本(latest_version)。

反之，如果用户端命令指明了版本，比如：`biscuit get app1 1.0`，则匹配指定版本(version)。

然后用户端就会在软件仓库中查找对应版本的软件包，并下载到本地。

## 2.搭建第三方软件源

搭建第三方软件源，需要以下步骤：

1. 准备一台服务器，安装好Web服务器软件（如Apache、Nginx等）。
2. 在服务器根目录下创建一个目录，如 `repo` 目录，用于存放软件包。
3. 根据上文介绍的软件源架构，在 `repo` 目录下创建 `apps.json` 文件，用于记录软件包分类。
4. 在 `repo` 目录下创建各类软件包目录，如 `games`、`tools` 等。
5. 在各类软件包目录下创建 `package.json` 文件，用于记录软件包基本信息。
6. 在各类软件包目录下创建各版本软件包，如 `xxx_1.0.qap`、`xxx_1.1.qap` 等（可使用QAP软件包封装工具制作，工具会自动生成 `name_version.qap` 格式的软件包文件）。
7. 启动Web服务器，将 `repo` 目录作为Web服务器的根目录，并设置好Web服务器的权限。
8. 在Quarter OS客户端设置中，添加软件源URL，如 `http://xxx.xxx.xxx/repo`，并保存设置（`biscuit mirror "https://xxx.xxx.xxx/repo"`）。

然后您就成功地搭建了自己的Biscuit第三方软件源。

## 3.免费搭建方案

另外，考虑到并不是所有人都能有足够的资金购买服务器，所以Biscuit软件仓库**允许纯前端HTTP协议的软件源**，只需要搞一个免费的纯前端的页面托管服务（比如GitHub Pages），然后按照上文的仓库结构搭建即可。

1. 准备一个GitHub账号，创建一个仓库，如 `biscuit-repo`。
2. 在仓库根目录下创建一个 `index.html` 文件，用于启动GitHub Pages服务。
3. 在仓库根目录下创建一个 `repo` 目录，用于存放软件包。
4. 根据上文介绍的软件源架构，在 `repo` 目录下创建 `apps.json` 文件，用于记录软件包分类。
5. 在 `repo` 目录下创建各类软件包目录，如 `games`、`tools` 等。
6. 在各类软件包目录下创建 `package.json` 文件，用于记录软件包基本信息。
7. 在各类软件包目录下创建各版本软件包，如 `xxx_1.0.qap`、`xxx_1.1.qap` 等（可使用QAP软件包封装工具制作，工具会自动生成 `name_version.qap` 格式的软件包文件）。
8. 将 `repo` 目录上传到GitHub仓库。
9. 在GitHub仓库设置中，点击"Pages"，然后设置好分支和目录，开启GitHub Pages服务。
10. 在Quarter OS客户端设置中，添加软件源URL，如 `https://xxx.github.io/biscuit-repo/repo`，并保存设置（`biscuit mirror "https://xxx.github.io/biscuit-repo/repo"`）。

这样，您就成功地搭建了自己的Biscuit第三方软件源，而且完全免费！

## 4.注意事项

### 1.更新和上传软件包

- 如果您是使用纯前端HTTP协议的软件源，则需要手动更新和上传软件包。

> [!TIP]
> 比如GitHub Pages服务，则需要在GitHub仓库网页端手动上传软件包，并手动更新相关的json文件。或者使用git，在本地仓库进行软件包的更新，然后推送到GitHub仓库。

- 如果您是使用Web服务器的软件源，则可以通过FTP、SSH等方式上传软件包，并更新相关的json文件，或者直接在后端编写相关脚本，实现上传软件包自动更新相关json文件的功能。

### 2.软件包审核

作为软件源仓库的维护者，您需要对上传的软件包进行审核，确保软件包的安全性和完整性。

1. 软件包的安全性：软件包必须经过严格的安全测试，确保其安全性。
2. 软件包的完整性：软件包必须经过严格的测试，确保其完整性。
3. 基本信息文件的正确性：软件包的基本信息文件（如 `package.json` 文件）必须正确填写，包括软件包名称、版本号、作者、描述等。

### 3.软件包的分类

为了方便用户查找软件包，您需要对软件包进行分类，并在 `apps.json` 文件中记录分类信息。

目前拟定这几个分类：

- `games`：游戏类软件包。
- `tools`：工具类软件包。
- `amusement`：娱乐类软件包。
- `education`：教育类软件包。

### 4.软件包的版本号

为了方便用户查找软件包，您需要为软件包的不同版本号分配不同的版本号码。

但请注意，用户端需要的是软件包的版本**代号**（如 `1.0`、`1.1`、`2.0`），而在仓库中还需要记录软件包的**版本号**（如 `1000`、`1100`、`2000`）。真正意义上的**版本号码**用于比较新版旧版软件包。

---

<div align="center">

Written by [ElofHew](https://github.com/ElofHew)

&copy; 2025 Oak Studio. All rights reserved.

</div>