# 如何获取Har文件?

> 准备  
> [1] 电脑  
> [2] 现代浏览器(包括但不限于Chrome、Edge、Firefox、Safari)

## 详细步骤

1. 打开浏览器
2. 前往目标网站
3. 点击搜索栏，跳转至搜索页面

<div align="center">
<img src="https://raw.githubusercontent.com/zhangjiancong/MarketSpider/7d0801c20fd18e34e873ceae0c6470b11ebbf097/docs/images/search_page.jpg" width="300px"/>
</div>

4. 输入搜索关键词，但不要发起搜索
5. 打开浏览器的开发人员工具，您可以使用如下任何一种方式打开

+ 浏览器快捷键`F12`
+ 在页面空白处右键，选择`检查`

<div align="center">
<img src="https://raw.githubusercontent.com/zhangjiancong/MarketSpider/main/docs/images/dev_tool1.jpg" width="300px"/>
</div>

+ 浏览器`设置或其他按钮`>`更多工具`>`开发人员工具`,名称可能略有不同

当您成功打开开发人员工具后,您将看到如下图所示面板
<div align="center">
<img src="https://raw.githubusercontent.com/zhangjiancong/MarketSpider/main/docs/images/dev_tool.jpg"/>
</div>

6. 在开发人员工具中，切换至 '网络'/'Network' 页面
7. 勾选 '保留日志' 选项

<div align="center">
<img src="https://raw.githubusercontent.com/zhangjiancong/MarketSpider/main/docs/images/dev_tool_network.jpg"/>
</div>

8. 在购物平台的页面上发起搜索
9. 可以使用 'End' 快捷键，快速翻页到页面底部便于网页继续向下加载
10. 当收集足够数据后，在开发人员工具中，在任意请求上右键，选择'将所有内容保存至HAR'

<div align="center">
<img src="https://raw.githubusercontent.com/zhangjiancong/MarketSpider/main/docs/images/save_har.jpg"/>
</div>
