# MarketSpider
![Python Version >3.8](https://img.shields.io/badge/Python-%3E3.8-blue)

[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/zhangjiancong/MarketSpider.svg)](http://isitmaintained.com/project/zhangjiancong/MarketSpider "Average time to resolve an issue")
[![Percentage of issues still open](http://isitmaintained.com/badge/open/zhangjiancong/MarketSpider.svg)](http://isitmaintained.com/project/zhangjiancong/MarketSpider "Percentage of issues still open")

淘宝、京东、1688商品信息爬虫。方便自动化的获取指定关键词的商品链接、商品价格、商品名称、店铺名称、店铺链接等信息。配合Tkinter的GUI界面，可以清晰监测运行状态。  
不是专业程序员，仅为Python和web自动化爱好者，欢迎提供建议和程序改进！


> **免责声明**
> 1. 本程序仅供用于交流学习原理使用。禁止用于商业活动或其他非法用途。
> 2. 对于被爬虫网站请遵守robots协议指引爬取数据。
> 3. 对于不遵守以上规定的，程序编写者不承担任何责任。
> 4. 因使用本程序造成的账户封禁、限制，程序编写者不承担任何责任。  
> 如您不认可以上免责声明，请不要使用本程序。



## 快速指引
完整使用教程请您前往:
[Github Wiki](https://github.com/zhangjiancong/MarketSpider/wiki)
#### 1、Python配置

1. 正确安装Python3，建议安装Python3.8以上环境。
2. (可选)建立Venv环境

#### 2、WebDriver配置

通过使用WebDriver，Selenium可以操作市场上主流浏览器。通过以下链接可以前往下载站点。下载后将其放置在本程序文件夹内即可。  
注意需要使用与您浏览器安装版本相对应的WebDriver。  
[Google Chrome](https://chromedriver.chromium.org/downloads) |
[MS Edge](https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/) |
[Selenium-Install Drivers指引](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)  
详细的指引可以参阅Selenium的Webdriver文档，[点击此处跳转](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/)

#### 3、启动对应程序开始使用
`Starter.py`是一个友好的启动器工具.使用此工具帮助您快速进行首次运行配置,及各程序启动.


## 用户隐私说明
+ 程序本身没有上传数据的代码和功能。
+ 程序使用者(您)是隐私数据保护的第一人,您应保护您的计算机不受病毒、木马程序感染，连接安全可信任的网络，保护您计算机上的文件安全性。
+ 程序运行时会保存网站Cookie、LocalStorage、SessionStorage数据到`cookie`文件夹,这些数据可能包含您的商城账户名称、电话、邮箱、历史购买记录、历史搜索记录、历史登录记录等信息,其种类、加密情况与商城网站有关，与本程序无关。
+ 为了方便异常分析，程序将保存一些日志信息到`Logs`。日志信息可能包含但不限于您的搜索关键词、浏览器名称、浏览器版本等信息。在过往实践中发现可能包含您的操作系统用户名等信息。在您提交Issue或将日志交由其他人分析时，注意此情况。

## 文件功能和最新版本
版本号定义:[主版本].[程序版本].[选择器版本]
| 文件名                  | 最新版本和发布时间                    | 用途              |
|----------------------|------------------------------|-----------------|
| Core.py              | **2.0-beta1** <br> 2025-03-18 | 核心库             |
| Update.py            | **1.1** <br> 2025-03-18      | 版本更新工具          |
| Starter.py            | **1.0** <br> 2025-03-16      | 程序启动器          |
| GetCookie.py         | **2.0** <br> 2025-03-18       | 用于自动化获取登录cookie |
| Spider_jd.py          | **2.0.0** <br> 2025-03-18       | 京东商城爬虫程序        |
| taobaoSpider.py      | **1.2** <br> 2024-04-22       | 淘宝网爬虫程序         |
| 1688Spider.py        | **1.0** <br> 2022-07-28       | 阿里巴巴1688爬虫程序    |
| error.wav            |                              | 错误提示音乐          |
| requirements.txt     |                              | pip依赖列表         |

## 打赏
如果本程序对您有帮助或您认为该程序不错,欢迎通过以下渠道打赏,无论金额都不胜感激！  
*为便于展示建议您备注用户名或联系方式*
![打赏二维码](https://zhangjiancong.github.io/MarketSpider/pages/sponser.jpg)