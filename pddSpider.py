import json
import csv
import sys
import time
import random
import tkinter
from selenium import webdriver
from selenium.webdriver.common.by import By
from threading import Thread
import winsound

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
    gui.title('拼多多店铺信息爬取器 Powered by zjc')
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
gui_text['text'] = '等待搜索关键词'
keyword = input('输入搜索关键词:')
gui_text['text'] = '正在启动浏览器'
browser = webdriver.Chrome()
browser.get('https://mobile.yangkeduo.com/relative_goods.html?__rp_name=search_view&source=index')

# CSV相关
csvfile = open(f'{keyword}-pdd-{time.strftime("%Y%m%d%H%M", time.localtime())}.csv', 'a', encoding='utf-8-sig',
               newline='')
csvWriter = csv.DictWriter(csvfile, fieldnames=['item_name', 'item_price', 'item_shop', 'item_num'])
csvWriter.writerow({'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'item_num': '店铺成交'})

# cookie相关
gui_text['text'] = '正在清空Cookie'
browser.delete_all_cookies()
gui_text['text'] = '正在注入Cookie'
try:
    with open('pinduoduo.cookie', 'r') as f:
        cookie_list = json.load(f)
        for cookie in cookie_list:
            browser.add_cookie(cookie)
            gui_label_now['text'] = cookie
except:
    print('未找到Cookie')
gui_text['text'] = '正在刷新浏览器'
browser.refresh()

# 搜索词与页数获取
gui_text['text'] = '正在操作'
browser.find_element(By.CSS_SELECTOR, '#submit > input').send_keys(keyword)
browser.find_element(By.CSS_SELECTOR, '#main > div._1ip7BikD > div.bvZKYfsR > div > div.RuSDrtii').click()

# 爬取个数控制
gui_text['text'] = '等待爬取个数'
print(f'输入要爬取的起始个数和末尾个数')
page_start = int(input('起始个数：'))
page_end = int(input('截止个数：')) + 1


def safe_check():
    """验证码等待
    """
    gui_text['text'] = f'出错：如有验证请验证。等待20秒'
    gui_text['bg'] = 'red'
    gui_label_eta['text'] = '-'
    gui_label_now['text'] = '-'
    winsound.PlaySound('error.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
    winsound.PlaySound('error.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)
    time.sleep(20)


for page in range(page_start, page_end):
    gui_text['text'] = f'当前正在获取第{page}个，还有{page_end - page_start - page}个'
    gui_text['bg'] = '#10d269'
    gui_label_now['text'] = '-'
    gui_label_eta['text'] = '-'
    try:
        # 尝试查找元素
        itemele=browser.find_element(By.CSS_SELECTOR,
                             f'#main > div > div:nth-child(2) > div > div > div.iXkfc0sA > div.CCuvAuS- > div > '
                             f'div:nth-child({page}) > div > div > div.WXRcg5KA > div > img')
        webdriver.ActionChains(browser).move_to_element(itemele)
    except:
        # 拦截安全验证
        try:
            browser.find_element(By.CSS_SELECTOR,
                                 '#main > div > div._50ZyeK-4 > div > div')
        except:
            safe_check()

        # 尝试使用下翻页
        test = 0
        scr = 100000
        while True:
            gui_text['text'] =f'下翻页查找元素{page}中'
            gui_text['bg'] = 'red'

            browser.execute_script(f"document.documentElement.scrollTop={scr}")
            time.sleep(5)
            try:
                test = test + 1
                scr = scr * 1.3
                ele = browser.find_element(By.CSS_SELECTOR,
                                           f'#main > div > div:nth-child(2) > div > div > div.iXkfc0sA > div.CCuvAuS- > div > div:nth-child({page}) > div > div > div.PWKq3gf1 > div.fnpJrQyt.KbqLm0ek').text
            except:
                # 判断是否找到该元素
                gui_label_now['text'] = f'尝试翻页解决无法找到元素'
                gui_label_eta['text'] = f'尝试第{test}次'
                if test>10:
                    page=page+1
                    break
                continue

            gui_label_now['text'] = '-'
            break


    item_price = browser.find_element(By.CSS_SELECTOR,
                                      f'#main > div > div:nth-child(2) > div > div > div.iXkfc0sA > div.CCuvAuS- > div > div:nth-child({page}) > div > div > div.PWKq3gf1 > div.ra5v5UQi > div > div._9D91bFn1 > span').text
    # 找到元素即点击
    gui_text['text'] = f'当前正在获取第{page}个，还有{page_end - page_start - page}个'
    gui_text['bg'] = '#10d269'
    imgele = browser.find_element(By.CSS_SELECTOR,
                                  f'#main > div > div:nth-child(2) > div > div > div.iXkfc0sA > div.CCuvAuS- > div > '
                                  f'div:nth-child({page}) > div > div > div.WXRcg5KA > div > img')
    webdriver.ActionChains(browser).move_to_element(imgele).click(imgele).perform()
    time.sleep(5)

    try:
        ele = browser.find_element(By.CSS_SELECTOR, '#main > div')
    except:
        safe_check()
    browser.execute_script("document.documentElement.scrollTop=1000")
    try:
        item_shop = browser.find_element(By.CSS_SELECTOR,
                                         '#main > div > div._2atM6O_- > div._1FjFNQJx._1PWnfoXL > div > div.hSg2uwm_ > div._3c93sjBH > div').text
    except:
        item_shop = 'fail to get shop'
    try:
        item_name = browser.find_element(By.CSS_SELECTOR,
                                         '#main > div > div._2atM6O_- > div:nth-child(4) > div > span > span._1fdrZL9O.enable-select > span').text
        gui_label_now['text'] = item_name
    except:
        item_name = 'fail to get name'
    try:
        item_num = browser.find_element(By.CSS_SELECTOR,
                                        '#main > div > div._2atM6O_- > div._1FjFNQJx._1PWnfoXL > div > div.hSg2uwm_ > div._3_944v1t._2Tk2F56I > div._dS_ovUS > span').text
    except:
        item_num = 'fail to get num'
    csvWriter.writerow({'item_name': item_name, 'item_price': item_price, 'item_shop': item_shop, 'item_num': item_num})
    csvfile.flush()
    delay_time = random.randint(5, 15)
    for delay in range(delay_time):
        gui_text['bg'] = '#eeeeee'
        gui_label_eta['text'] = f'延时获取：已延时{delay}秒，剩余{delay_time}秒'
        time.sleep(1)
    browser.back()
    time.sleep(5)

print('程序结束')
gui_text['text'] = '程序结束正在保存文件'
csvfile.close()
gui_text['text'] = '保存文件完成，准备退出中'
time.sleep(5)
browser.close()
sys.exit()
