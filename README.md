# MarketSpider
淘宝、京东、拼多多信息爬虫。方便自动化的获取指定关键词的商品链接、商品价格、商品名称、店铺名称、店铺链接等信息。配合Tkinter的GUI界面，可以清晰监测运行状态。

> **免责声明**  
> 1. 本程序仅供用于交流学习原理使用。禁止用于商业活动或其他非法用途。  
> 2. 对于被爬虫网站请遵守robots协议指引爬取数据。  
> 3. 对于不遵守以上规定的，程序编写者不承担任何责任。

## 环境配置
1. 正确安装Python3，建议安装Python3.8以上环境。
2. (可选)建立Venv环境
3. 在终端下运行`pip install -r requirements.txt`，安装所需包。

## 文件树
+ GetCookie.py       用于自动化获取登录cookie
+ jdSpider.py        京东商城爬虫程序
+ taobaoSpider.py    淘宝网爬虫程序
+ ~~pddSpider.py     拼多多爬虫程序~~(修复中，暂不可用
+ error.wav          错误提示音乐
+ \ WebDrivers       Chrome和Edge最近版本WebDriver驱动程序
+ \ venv             venv环境，可使用此环境直接运行
+ \ functions        辅助变量、函数、对象

## 使用教程


### taobaoSpider.py
+ 无GUI
+ demo版本
+ Cookie需要从Browser获取
### jdSpider.py
+ 基于selenium
+ 需要安装tkinter
### pddSpider.py
+ 基于selenium
+ 需要安装tkinter
+ 强Cookie务必现场生成
### GetCookie.py
Cookie生成器
+ 基于selenium