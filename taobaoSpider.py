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
import re
import traceback

VERSION='1.1'
print(f'程序版本{VERSION}\n最新程序下载地址:https://github.com/zhangjiancong/MarketSpider')

# 全局变量状态文字
gui_text = {}
gui_label_now = {}
gui_label_eta = {}

# 淘宝页面版本 0旧 1新
tbPageVersion = 0


# GUI函数
def guiFunc():
    global gui_text
    global gui_label_now
    global gui_label_eta
    gui = tkinter.Tk()
    gui.title('淘宝店铺信息爬取器 Powered by zjc')
    gui['background'] = '#ffffff'
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
gui_text['background'] = '#f35315'
keyword = input('输入搜索关键词:')
gui_text['background'] = '#ffffff'
gui_text['text'] = '正在启动浏览器'
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=options)
browser.get('https://www.taobao.com')
gui_text['background'] = '#ffffff'

# CSV相关
csvfile = open(f'{keyword}_taobao_{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.csv', 'a', encoding='utf-8-sig',
               newline='')
csvWriter = csv.DictWriter(csvfile,
                           fieldnames=['item_name', 'item_price', 'item_shop', 'shop_link', 'item_link', 'bridge','item_paid'])
csvWriter.writerow(
    {'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'shop_link': '店铺链接',
     'item_link': '商品链接', 'bridge': '店铺id桥','item_paid':'付款人数(参考销量)'})

# cookie相关
gui_text['text'] = '正在清空Cookie'
browser.delete_all_cookies()
gui_text['text'] = '正在注入Cookie'
try:
    with open('taobao.cookie', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            browser.add_cookie(cookie)
except:
    print('未找到Cookie')
gui_text['text'] = '正在刷新浏览器'
browser.refresh()
# 搜索词与页数获取
gui_text['text'] = '正在操作'
browser.get(f'https://s.taobao.com/search?q={keyword}')
browser.implicitly_wait(10)
try:
    # 老版PC淘宝页面
    taobaoPage = browser.find_element(By.CSS_SELECTOR,
                                      '#J_relative > div.sort-row > div > div.pager > ul > li:nth-child(2)').text
    taobaoPage = re.findall('[^/]*$', taobaoPage)[0]
    tbPageVersion = 0
except:
    # 新版PC淘宝页面
    taobaoPage = browser.find_element(By.CSS_SELECTOR,
                                      '#sortBarWrap > div.SortBar--sortBarWrapTop--VgqKGi6 > div.SortBar--otherSelector--AGGxGw3 > div:nth-child(2) > div.next-pagination.next-small.next-simple.next-no-border > div > span').text
    taobaoPage = re.findall('[^/]*$', taobaoPage)[0]
    tbPageVersion = 1

# 爬取页数控制
gui_text['text'] = '☞等待爬取页数'
gui_text['background'] = '#f35315'
print(f'共计{taobaoPage}页,建议每2小时总计爬取不超过20页')
page_start = int(input('起始页数：'))
page_end = int(input('截止页数：')) + 1
gui_text['background'] = '#ffffff'

for page in range(page_start, page_end):
    gui_text['text'] = f'当前正在获取第{page}页，还有{page_end - page_start - page}页'
    gui_text['bg'] = '#10d269'
    gui_label_now['text'] = '-'
    gui_label_eta['text'] = '-'
    browser.get(f'https://s.taobao.com/search?q={keyword}&page={page}&_input_charset=utf-8&commend=all&search_type=item&source=suggest&sourceId=tb.index')
    if browser.title == '验证码拦截':
        gui_text['text'] = f'出错：如有验证请验证。等待20秒'
        gui_text['bg'] = 'red'
        gui_label_eta['text'] = '-'
        gui_label_now['text'] = f'-'
        playsound('error.wav')
        time.sleep(20)
    time.sleep(5)
    # 尝试获取商品列表
    try:
        gui_text['text'] = f'当前正在获取第{page}页，还有{page_end - page_start - page}页'
        gui_text['bg'] = '#10d269'
        goods_arr = browser.find_elements(By.CSS_SELECTOR, '#pageContent > div:nth-child(1) > div:nth-child(3) > div:nth-child(3) > div>div')
        goods_length = len(goods_arr)
        for i, goods in enumerate(goods_arr):
            try:
                i=i+1
                browser.execute_script("document.documentElement.scrollTop=1000")
                gui_label_now['text'] = f'正在获取第{i}个,共计{goods_length}个'
                item_name = goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a>div > div:nth-child(1) > div:nth-child(2) > div > span').text
                item_price= goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a>div > div:nth-child(1) > div:nth-child(4) > div').text
                item_shop = goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a>div> div:nth-child(3) > div>a').text
                shop_link = goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a>div> div:nth-child(3) > div>a').get_attribute(
        'href')
                item_link = goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a').get_attribute(
        'href')
                item_paid=goods.find_element(By.CSS_SELECTOR,
                                    f'div:nth-child({i})>a>div > div:nth-child(1) > div:nth-child(4) > span.Price--realSales--FhTZc7U').text
                try:
                    b = shop_link.split('https://store.taobao.com/shop/view_shop.htm?appUid=')[1]
                except:
                    b = shop_link
                csvWriter.writerow(
                    {'item_name': item_name, 'item_price': item_price, 'item_shop': item_shop, 'shop_link': shop_link,
                        'item_link': item_link, 'bridge': b,'item_paid':item_paid})
                csvfile.flush()
            except:
                print(f'第{i}个商品获取信息出错,跳过')
                traceback.print_exc()
    except Exception as e:
        print(f'在遍历商品时出错{e}')
        traceback.print_exc()
        # 拉取商品列表失败则提示需要验证
        gui_text['text'] = f'出错：如有验证请验证。等待20秒'
        gui_text['bg'] = 'red'
        gui_label_eta['text'] = '-'
        gui_label_now['text'] = f'注意:第<{page}>页将跳过如需获取请重新运行程序！'
        print(f'注意:第<{page}>页将跳过如需获取请重新运行程序！')
        playsound('error.wav')
        time.sleep(20)

    delay_time = random.randint(10, 30)
    for delay in range(delay_time):
        gui_label_now['text'] = '-'
        gui_text['bg'] = '#eeeeee'
        gui_text['text'] = f'第{page}页，还有{page_end - page_start - page}页'
        gui_label_eta['text'] = f'延时翻页：已延时{delay}秒，剩余{delay_time}秒'
        time.sleep(1)

print('程序结束')
gui_text['text'] = '程序结束正在保存文件'
csvfile.close()
gui_text['text'] = '保存文件完成，准备退出中'
time.sleep(5)
browser.close()
sys.exit()
