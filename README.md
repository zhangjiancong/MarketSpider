# MarketSpider

[![OSCS Status](https://www.oscs1024.com/platform/badge/zhangjiancong/MarketSpider.svg?size=small)](https://www.oscs1024.com/project/zhangjiancong/MarketSpider?ref=badge_small)  
淘宝、京东、拼多多、1688、京喜信息爬虫。方便自动化的获取指定关键词的商品链接、商品价格、商品名称、店铺名称、店铺链接等信息。配合Tkinter的GUI界面，可以清晰监测运行状态。  
不是专业程序员，仅为Python和web自动化爱好者，欢迎提供建议和程序改进！

**📢 2023年4月18日 淘宝貌似灰度上线了新版UI，程序代码很乱但是新版UI和旧版都能用，等淘宝彻底切换完重构那个文件**

> **免责声明**
> 1. 本程序仅供用于交流学习原理使用。禁止用于商业活动或其他非法用途。
> 2. 对于被爬虫网站请遵守robots协议指引爬取数据。
> 3. 对于不遵守以上规定的，程序编写者不承担任何责任。



## 快速指引

#### 1、Python与Python包配置

1. 正确安装Python3，建议安装Python3.8以上环境。
2. (可选)建立Venv环境
3. 在终端下运行`pip install -r requirements.txt`，安装所需包。

#### 2、WebDriver配置

通过使用WebDriver，Selenium可以操作市场上主流浏览器。通过以下链接可以前往下载站点。下载后将其放置在本程序文件夹内即可。  
注意需要使用与您浏览器安装版本相对应的WebDriver。  
[Google Chrome](https://chromedriver.storage.googleapis.com/index.html) |
[MS Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) |
[Selenium-Install Drivers指引](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)  
程序默认使用Google Chrome浏览器，如果您需要使用其他浏览器，请按照下方指引更改代码。

+ 程序文件中的`options = webdriver.ChromeOptions()`更改为对应浏览器，如Edge则更改为`options = webdriver.EdgeOptions()`
+ 程序文件中的`driver=webdriver.Chrome(options=options)`更改为对应浏览器，如Edge则更改为`driver=webdriver.Edge(options=options)`

详细的指引可以参阅Selenium的Webdriver文档，[点击此处跳转](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)
#### 3、启动对应程序开始使用

## 拼多多、京喜平台特别说明
拼多多、京喜平台因技术原因，使用半自动化方案，手动保存浏览器的请求，使用对应程序进行读取并保存成为CSV文件。无需使用Selenium环境。如何获取HAR文件可至[HAR文件获取](https://github.com/zhangjiancong/MarketSpider/wiki)

## 文件功能和最新版本
| 文件名                  | 最新版本和发布时间              | 用途              |
|----------------------|------------------------|-----------------|
| \ functions          |                        | 自定义包            |
| GetCookie.py         | **1.1** <br> 2023-4-18 | 用于自动化获取登录cookie |
| jdSpider.py          | **1.0** <br> 2022-7-28 | 京东商城爬虫程序        |
| taobaoSpider.py      | **1.1** <br> 2023-4-18 | 淘宝网爬虫程序         |
| 1688Spider.py        | **1.0** <br> 2022-7-28 | 阿里巴巴1688爬虫程序    |
| error.wav            |                        | 错误提示音乐          |
| requirements.txt     |                        | pip依赖列表         |
| jingxi_HAR_reader.py | **1.0** <br> 2022-7-28 | 京喜HAR读取程序       |
| pdd_HAR_reader.py    | **1.0** <br> 2022-7-28 | 拼多多HAR读取程序      |


## 使用教程
[Github Wiki](https://github.com/zhangjiancong/MarketSpider/wiki)
