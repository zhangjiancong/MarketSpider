import csv
import json
import sys
import time
import tkinter
from threading import Thread
from tkinter import filedialog, messagebox
from playsound import playsound
from selenium import webdriver
from selenium.webdriver.common.by import By


class Spider:
    def __init__(self, keywords):
        self.csvWriter = None
        self.csvStream = None
        self.runtime = time.strftime("%Y-%m-%d_%H-%M", time.localtime())
        self.keywords = keywords

    def init_csv_file(self):
        self.csvStream = open(f'{self.keywords}-1688-{self.runtime}.csv', 'a', encoding='utf-8-sig', newline='')
        self.csvWriter = csv.DictWriter(self.csvStream,
                                        fieldnames=['item_name', 'item_price', 'item_shop', 'shop_link', 'item_link'])
        self.csvWriter.writerow(
            {'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'shop_link': '店铺链接', 'item_link': '商品链接'})
        self.csvStream.flush()

    def write_new_line(self, text):
        self.csvWriter.writerow(text)
        self.csvStream.flush()

    def catch_err(self):
        playsound('error.wav')

    def close_exit(self):
        self.csvStream.close()


class browserObj:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.browserWin = webdriver.Chrome(options=self.options)
        self.browserWin.implicitly_wait(8)

    def add_cookie(self):
        self.browserWin.delete_all_cookies()
        try:
            with open('1688.cookie', 'r') as f:
                cookie_list = json.load(f)
                for cookie in cookie_list:
                    self.browserWin.add_cookie(cookie)
        except:
            print('未找到Cookie')
        self.browserWin.refresh()

    def navi_to(self, url):
        self.browserWin.get(url)

    def scroll_page(self):
        self.browserWin.execute_script("document.documentElement.scrollTop=100000")

    def find_css(self, css):
        return self.browserWin.find_element(By.CSS_SELECTOR, css)

    def close_exit(self):
        self.browserWin.close()


class MyGUI():
    def __init__(self,title='MarketSpider 状态监视工具'):
        self.root = tkinter.Tk()
        self.root.title(title)
        self.root['background'] = '#ffffff'
        self.root.geometry('600x150-50+20')
        self.root.attributes("-topmost", -1)
        self.statue = tkinter.Label(self.root, text='初始化', font=('微软雅黑', '18'), background='#e3e3e3',
                                    wraplength=195)
        self.statue.place(x=0, y=0, height=150, width=200)
        self.btn_store = tkinter.Button(self.root, text='保存信息(F8)')
        self.btn_store.place(x=230, y=65, height=30, width=100)
        self.btn_next = tkinter.Button(self.root, text='下一个店铺(F9)')
        self.btn_next.place(x=342, y=65, height=30, width=100)
        self.btn_1 = tkinter.Button(self.root, text='备用')
        self.btn_1.place(x=454, y=65, height=30, width=100)
        self.total = tkinter.Label(self.root, text='已完成:  -  总计:  -', font=('微软雅黑', '10'), background='#ffffff')
        self.total.place(x=230, y=9, height=20)
        self.label_1 = tkinter.Label(self.root, text='', font=('微软雅黑', '10'), background='#ffffff')
        self.label_1.place(x=230, y=37, height=20)

    def run(self):
        # Gui_thread = Thread(target=self.root.mainloop, daemon=True)
        # Gui_thread.start()
        self.root.mainloop()

    def autowork(self):
        self.statue['background'] = '#fffa65'
        self.statue['text'] = f'自动化操作中'

    def needcode(self, shopid):
        self.statue['background'] = '#7bed9f'
        self.statue['text'] = f'请输入验证码!\n店:{shopid}'

    def warning(self, reason):
        self.statue['background'] = '#ff4757'
        self.statue['text'] = f'出错\n异常:{reason}'

    def progresscontrol(self, now, total):
        self.total['text'] = f'已完成： {now}   总计： {total}'

    def custom_statue(self, text, color='#e3e3e3'):
        self.statue['text'] = text
        self.statue['background'] = color

    def custom_label0(self, text, color='#FFFFFF'):
        self.total['text'] = text
        self.total['background'] = color

    def custom_label1(self, text, color='#FFFFFF'):
        self.label_1['text'] = text
        self.label_1['background'] = color

    def open_file_dialog(self,title='请打开CSV文件'):
        filePath=tkinter.filedialog.askopenfilename(title=title)
        if filePath=='':
            tkinter.messagebox.showerror('错误','您没有打开任何CSV文件')
            sys.exit()
        return filePath

