# novel-crawler

一个可拓展的小说下载工具  

> 本项目最初是个人用途，只能下载番茄小说，想下载其他平台的请寻找别的项目

## 特色
1. 三种下载模式：`API`,`Browser`, `Requests`
2. 支持下载网页端插图
3. 配置灵活，针对不同网站做不同配置
4. 支持断点续传
5. 分组导出小说文件
6. 跨三大平台
7. WebUI

## 功能

- **搜索** — 关键词搜索小说
- **下载** — 多线程并发下载章节正文和插图
- **更新** — 扫描已下载小说，自动检查并下载新章节
- **导出** — 支持 TXT、EPUB、IMG（图片）三种格式

## 下载模式

### API

API模式采用 **第三方API服务** 下载小说，它简单高效，但是需要`key`作为下载凭证。  

#### 获取key方式

| 网站 | API名称 | 提供商(PROVIDER)            | 获取key方式                                           | 备注                           |
|------|---------|-----------------------------|-------------------------------------------------------|--------------------------------|
| 番茄 | OIAPI   | [OIAPI](https://oiapi.net/) | [访问网站](https://oiapi.net/)，将会弹出获取key的方式 | 下载次数有限，每天签到获取额度 |
| ...  |

将获取到的 key 填写到配置文件`app_data/config/sites/{website}.yaml` 的 key 字段之中

### Browser

通过操作浏览器访问网站下载小说，它比较吃内存，如果要下载插图它是不二之选。  
网站一般有反爬虫机制，比如弹出验证码等。通过降低访问频率有效降低触发频率。  
目前支持的浏览器类型只有Chrome。**使用此模式时请检查电脑上有没有安装Chrome**  
**该模式需要您解锁相关章节，不可以获取未解锁的章节**

### Requests

最基本的下载模式，也是访问目标网站下载。  
此模式也是访问目标网站来下载的，也会被反制。没有代理不建议使用它。  
**该模式需要您解锁相关章节，不可以获取未解锁的章节**  

## 安装

在开始之前请先检查电脑是否有：
- git
- python3.10+

```bash
git clone https://github.com/volcyano42/novel-crawler.git
cd novel-crawler
pip install -r requirements.txt
# 本项目使用的是PlayWright，所以您需要安装内置的浏览器才可以使用Browser模式
playwright install chromium
```

## 快速开始

本项目提供了三种模式：CLI，非CLI，WebUI

### 交互式模式(非CLI)

```bash
python main.py
```

启动后进入交互菜单：

```text
分组: default    并发: 3
1. 🔍 搜索下载
2. 🔄 更新已有小说
3. 📤 导出小说
4. 🔁 重新导出
5. 🗑️  删除小说
6. ⚙️  设置
7. 🌐 访问网站
0. 🚪 退出
```

### 非交互式模式(CLI)

```bash
python cli.py -h
```
```text
usage: cli.py [-h] {search,download,update,export,delete,novel,sources,info,dev} ...

novelbase — 小说下载器命令行

positional arguments:
  {search,download,update,export,delete,novel,sources,info,dev}
    search              搜索小说
    download            下载小说
    update              更新已下载小说
    export              重新导出已下载小说
    delete              删除已下载小说
    novel               已下载小说管理
    sources             书源管理
    info                查看小说信息
    dev                 开发工具

options:
  -h, --help            show this help message and exit
```

### WebUI模式

```bash
python app.py
```

#### 如何使用

搜索书籍关键词可以直接下载
或者获取小说的目录页链接，然后填写就可以下载了  

# 环境变量

- `NLD_APP_DATA`: app_data 数据目录
- `NLD_PRIVATE_SOURCES`: 外部私有源目录
- `NLD_PRIVATE_EXPORTERS`: 外部自定义导出格式目录
- `{PROVIDER_API_KEY}`: 提供商(PROVIDER)API密钥，优先级高于配置文件里的key

# 添加书源

[查看文档](docs/add_source.md)

# 关于打包程序的说明

本项目使用的是nuitka打包，打包程序的行为模式与病毒非常相似，所以容易误报。  
如果对本项目不放心，请使用其他同类型的产品。

# 免责声明

本项目以兴趣和研究为目的，使用者请在遵守相关法律法规下下载。**不过度采集或售卖，引发的风险和后果，违者需自行承担**

# 联系方式

作者：volcyano42  
QQ: 739137680
邮箱：1542804683@qq.com
