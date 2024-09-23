# V2.0-beta
import csv
import json
import sys
import time
import tkinter
import re
import os
import random
import traceback

from threading import Thread
from tkinter import filedialog, messagebox
from tkinter.ttk import Progressbar


try:
    import requests
    from playsound import playsound
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except Exception as errors:
    print(f'[错误]导入模块失败,请通过“pip install -r requirements.txt”安装.\n{errors}')
    os.system('pause>nul')
    sys.exit()


class Gui:
    COLOR_RUNNING = '#3edf86'
    COLOR_DEFAULT = '#eeeeee'
    COLOR_ATTENTION = '#fdc285'

    def __init__(self, comp_name):
        self.new_window = None
        self.input_box = None
        self.ui_root = tkinter.Tk()
        self.ui_root.title(f'{comp_name} - MarketSpider')
        self.ui_root.geometry("-50+20")
        self.ui_root.attributes("-topmost", 1)
        self.ui_root['background'] = '#eeeeee'
        self.main_text = tkinter.Label(self.ui_root, text='程序正在准备', font=("微软雅黑", 20), width=20, height=2,
                                       wraplength=500, justify=tkinter.LEFT)
        self.main_text.pack()
        self.main_text['background'] = '#4eb5fb'
        self.status_text = tkinter.Label(self.ui_root, text='程序正在准备...', relief=tkinter.SUNKEN, anchor='w')
        self.status_text.pack(fill=tkinter.X, side=tkinter.BOTTOM)
        self.progress_bar = Progressbar(self.ui_root)
        self.progress_bar.pack(fill=tkinter.X, side=tkinter.BOTTOM)

    def set_progress(self, done: int, total=100):
        if total == 0:
            self.progress_bar['maximum'] = 50
            self.progress_bar['mode'] = 'indeterminate'
            self.progress_bar.start()
        else:
            self.progress_bar['mode'] = 'determinate'
            self.progress_bar.stop()
            self.progress_bar['value'] = done
            self.progress_bar['maximum'] = total
            self.ui_root.update()

    def set_status(self, text: str):
        self.status_text['text'] = text
        self.ui_root.update()

    def set_text(self, text: str, color=COLOR_DEFAULT):
        self.main_text['text'] = text
        self.main_text['background'] = color
        self.ui_root.update()

    def save_asked_string(self):
        self.new_window.destroy()

    def ask_string(self, title: str, description: str):
        """
        弹出新窗口获取字符串
        @param title 新窗口标题
        @param description 新窗口显示的提示文本
        @return 返回用户输入值String
        """
        x = int((self.ui_root.winfo_screenwidth() - self.ui_root.winfo_reqwidth()) / 2)
        y = int((self.ui_root.winfo_screenheight() - self.ui_root.winfo_reqheight()) / 2)
        self.new_window = tkinter.Toplevel(master=self.ui_root)
        self.new_window.title(title)
        self.new_window.geometry("+{}+{}".format(x, y))
        self.new_window.attributes("-toolwindow", 2)
        tkinter.Label(self.new_window, text=description, anchor='w', pady=10).pack(fill=tkinter.X)
        v = tkinter.StringVar()
        input_box = tkinter.Entry(self.new_window, textvariable=v)
        input_box.pack()
        tkinter.Button(self.new_window, text='确认', command=self.save_asked_string).pack()
        self.ui_root.wait_window(self.new_window)
        return v.get()

    def ui_loop(self):
        self.ui_root.mainloop()

    def ui_start(self):
        Thread(target=self.ui_loop, daemon=True).start()


class BrowserControl:
    def __init__(self):
        self.browser = webdriver.Edge()

    def set_web_browser(self, browser):
        """
        设置浏览器
        @param browser: [chrome,edge,firefox]浏览器类型
        """
        if browser != 'chrome' or browser != 'edge' or browser != 'firefox':
            raise RuntimeError('设置WebDriver失败,目前仅支持Chrome、Edge、Firefox')
        if browser == 'chrome':
            browser_option = webdriver.ChromeOptions()
            browser_option.add_argument("--disable-blink-features=AutomationControlled")
            browser_option.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.browser = webdriver.Chrome(options=browser_option)
            self.browser.implicitly_wait(8)

        if browser == 'edge':
            browser_option = webdriver.EdgeOptions()
            browser_option.add_argument("--disable-blink-features=AutomationControlled")
            browser_option.add_experimental_option('excludeSwitches', ['enable-logging'])
            self.browser = webdriver.Edge(options=browser_option)
            self.browser.implicitly_wait(8)

        if browser == 'firefox':
            browser_option = webdriver.FirefoxOptions()
            browser_option.add_argument("--disable-blink-features=AutomationControlled")
            self.browser = webdriver.Firefox(options=browser_option)
            self.browser.implicitly_wait(8)

    def inject_cookie(self, market):
        self.browser.delete_all_cookies()
        try:
            with open(f'cookie\\{market}.cookie', 'r') as f:
                cookie_list = json.load(f)
                for cookie in cookie_list:
                    self.browser.add_cookie(cookie)
        except:
            Gui.set_text(text='未找到Cookie')
            Logger.write_info('未找到登录Cookie,在抓取时可能因为跳转至登录界面导致爬取失败', True)
        self.browser.refresh()

    def save_cookie(self,market):
        if not os.path.exists('cookie'):
            os.mkdir('cookie')
        with open(f'cookie\\{market}.cookie','w') as file:
            file.write(json.dumps(self.browser.get_cookies()))


    def find_element_css(self,path,name=None):
        try:
            ele=self.browser.find_element(By.CSS_SELECTOR,path)
            return ele
        except:
            print(f'[Browser_CSS_finder]查找{path}失败')
            return 'error in finding this'



class Logger:
    def __init__(self, comp: str):
        """
        日志记录器
        @param comp 记录根名称
        """
        self.comp = comp
        if not os.path.exists('logs'):
            os.mkdir('Logs')
        log_file_name = time.strftime('%Y_%m_%d', time.localtime())
        self.log_file = open(f'logs\\{log_file_name}.log', 'a', encoding='utf8')

    def write_info(self, info: str, dialog=False):
        happened_time = time.strftime('%H:%M:%S', time.localtime())
        self.log_file.write(f'[INFO] {happened_time} [{self.comp}] {info}\n')
        self.log_file.flush()
        if dialog:
            messagebox.showinfo(f'提示 - {self.comp}', info)

    def write_warn(self, warn: str, dialog=False):
        """
        @param warn 友好提示文本
        @param dialog 是否弹出窗体
        """
        happened_time = time.strftime('%H:%M:%S', time.localtime())
        self.log_file.write(f'[WARN] {happened_time} [{self.comp}] {warn}\n')
        self.log_file.flush()
        if dialog:
            messagebox.showwarning(f'注意 - {self.comp}', warn)

    def write_error(self, error_text: str, dialog=False):
        """
        记录一个错误.函数自动写入异常和调用链
        @param error_text 友好提示文本
        @param dialog 是否弹出窗体
        """
        err_exc = traceback.format_exc()
        err_stack = traceback.format_stack()
        happened_time = time.strftime('%H:%M:%S', time.localtime())
        self.log_file.write(f'[ERROR] {happened_time} [{self.comp}] {error_text}\n{err_exc}')
        self.log_file.flush()
        for s in err_stack:
            self.log_file.write(s)
            self.log_file.flush()
        if dialog:
            messagebox.showerror(f'出错 - {self.comp}', f'{error_text}\n{err_exc}')


class CsvWriter:
    def __init__(self,keyword,market):
        fieldnames = ['item_link', 'item_name', 'item_price', 'item_image', 'item_payment', 'item_rates', 'item_sales',
                      'item_shop', 'shop_link','remarks']
        cn_name = {'item_link': '商品链接', 'item_name': '商品名称', 'item_price': '商品价格', 'item_image': '商品图片',
                   'item_payment': '已付款人数', 'item_rates': '已评价数', 'item_sales': '商品销量',
                   'item_shop': '店铺名称', 'shop_link': '店铺链接','remarks':'备注'}
        if not os.path.exists('result'):
            os.mkdir('result')
        self.csvStream = open(f'result\\{keyword}-{market}-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.csv', 'a', encoding='utf-8-sig', newline='')
        self.csvWriter = csv.DictWriter(self.csvStream, fieldnames=fieldnames)
        self.csvWriter.writerow(cn_name)
        self.csvStream.flush()


    def write_new_line(self, item_link='', item_name='', item_price='', item_image='', item_payment='', item_rates='',
                       item_sales='', item_shop='', shop_link='',remarks=''):
        """
        在CSV中插入一条数据
        Args:
            item_link:商品链接
            item_name:商品名称
            item_price:商品价格
            item_image:图片链接
            item_payment:商品已支付人数
            item_rates:商品已评价人数
            item_sales:商品销量
            item_shop:店铺名称
            shop_link:店铺链接
            remarks:其他备注信息
        """
        self.csvWriter.writerow(
            {'item_link': item_link, 'item_name': item_name, 'item_price': item_price, 'item_image': item_image,
             'item_payment': item_payment, 'item_rates': item_rates, 'item_sales': item_sales, 'item_shop': item_shop,
             'shop_link': shop_link,'remarks':remarks})
        self.csvStream.flush()
        

    def close_csv(self):
        self.csvStream.close()





class Main(Gui, BrowserControl,CsvWriter):
    def __init__(self, keyword, market, browser):
        Gui.__init__(self,comp_name=market)
        CsvWriter.__init__(self,keyword,market='aaaa')

    def run(self):
        pass


aks=Main('121','taobao','Edge')