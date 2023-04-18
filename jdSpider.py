import json
import csv
import sys
import time
import random
import tkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
from playsound import playsound
import functions.jdSpiderDependence as jds
VERSION='1.0'
print(f'程序版本{VERSION}\n最新程序下载地址:https://github.com/zhangjiancong/MarketSpider')
# 全局变量状态文字
gui_text = {}
gui_label_now = {}
gui_label_eta = {}


# GUI函数
def guiFunc():
    global gui_text
    global gui_label_now
    global gui_label_eta
    gui = tkinter.Tk()
    gui.title('京东店铺信息爬取器 Powered by zjc')
    gui['background'] = '#eeeeee'
    gui.geometry("600x100-50+20")
    gui.attributes("-topmost", 1)
    gui_text = tkinter.Label(gui, text='初始化', font=('微软雅黑', '20'))
    gui_text.pack()
    gui_label_now = tkinter.Label(gui, text='?', font=('微软雅黑', '10'))
    gui_label_now.pack()
    gui_label_eta = tkinter.Label(gui, text='?', font=('微软雅黑', '10'))
    gui_label_eta.pack()
    gui.mainloop()


# GUI线程控制
Gui_thread = Thread(target=guiFunc, daemon=True)
Gui_thread.start()
time.sleep(2)

# 启动浏览器
gui_text['text'] = '☞等待搜索关键词'
keyword = input('输入搜索关键词:')
gui_text['text'] = '正在启动浏览器'
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get('https://www.jd.com')

# CSV相关
csvfile = open(f'{keyword}-jd-{time.strftime("%Y%m%d%H%M", time.localtime())}.csv', 'a', encoding='utf-8-sig',
               newline='')
csvWriter = csv.DictWriter(csvfile,
                           fieldnames=['item_name', 'item_price', 'item_shop', 'shop_link', 'item_link', 'jdshop_id'])
csvWriter.writerow(
    {'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'shop_link': '店铺链接', 'item_link': '商品链接',
     'jdshop_id': '京东店铺ID'})

# cookie相关
gui_text['text'] = '正在清空Cookie'
browser.delete_all_cookies()
gui_text['text'] = '正在注入Cookie'
try:
    with open('jd.cookie', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            browser.add_cookie(cookie)
except:
    print('未找到Cookie')
gui_text['text'] = '正在刷新浏览器'
browser.refresh()

# 搜索词与页数获取
gui_text['text'] = '正在操作'
browser.find_element(By.ID, 'key').send_keys(keyword)
browser.find_element(By.CLASS_NAME, 'button').click()
browser.implicitly_wait(10)
jdPage = browser.find_element(By.CSS_SELECTOR, '#J_bottomPage > span.p-skip > em:nth-child(1) > b').text
browser.execute_script("document.documentElement.scrollTop=100000")

# 爬取页数控制
gui_text['text'] = '☞等待爬取页数'
print(f'共计{jdPage}页，建议每2小时总计爬取不超过20页')
page_start = int(input('起始页数：'))
page_end = int(input('截止页数：')) + 1

for page in range(page_start, page_end):
    gui_text['text'] = f'当前正在获取第{page}页，还有{page_end - page_start - page}页'
    gui_text['bg'] = '#10d269'
    gui_label_now['text'] = '-'
    gui_label_eta['text'] = '-'
    browser.execute_script(f"SEARCH.page({2 * page - 1}, true)")
    time.sleep(5)
    browser.execute_script("document.documentElement.scrollTop=100000")
    time.sleep(2)
    browser.execute_script("document.documentElement.scrollTop=9959")
    # 每一页有60项
    for i in range(1, 61):
        try:
            gui_label_now['text'] = f'正在获取：当前页第{i}个，剩余{60 - i}个'
            item_name = browser.find_element(By.CSS_SELECTOR,
                                             f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-name.p-name-type-2 > a > em').text
            item_price = browser.find_element(By.CSS_SELECTOR,
                                              f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-price > strong > i').text
            item_shop = browser.find_element(By.CSS_SELECTOR,
                                             f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-shop > span > a').text
            shop_link = browser.find_element(By.CSS_SELECTOR,
                                             f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-shop > span > a').get_attribute(
                'href')
            item_link = browser.find_element(By.CSS_SELECTOR,
                                             f'#J_goodsList > ul > li:nth-child({i}) > div > div.p-img > a').get_attribute(
                'href')
            jdshop_id = jds.shop_id_get(shop_link)
            csvWriter.writerow(
                {'item_name': item_name, 'item_price': item_price, 'item_shop': item_shop, 'shop_link': shop_link,
                 'item_link': item_link, 'jdshop_id': jdshop_id})
            csvfile.flush()
        except:
            gui_text['text'] = f'出错：如有验证请验证。等待10秒'
            gui_text['bg'] = 'red'
            gui_label_eta['text'] = '-'
            gui_label_now['text'] = '-'
            playsound('error.wav')
            time.sleep(10)
    delay_time = random.randint(10, 30)
    for delay in range(delay_time):
        gui_label_now['text'] = '-'
        gui_text['bg'] = '#eeeeee'
        gui_label_eta['text'] = f'延时翻页：已延时{delay}秒，剩余{delay_time}秒'
        time.sleep(1)

print('程序结束')
gui_text['text'] = '程序结束正在保存文件'
csvfile.close()
gui_text['text'] = '保存文件完成，准备退出中'
time.sleep(5)
browser.close()
sys.exit()
