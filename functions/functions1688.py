import csv
import json
import tkinter

import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By


class Spider:
    def __init__(self, runtime, keywords):
        self.csvWriter = None
        self.csvStream = None
        self.runtime = runtime
        self.keywords = keywords

    def init_csv_file(self):
        self.csvStream = open(f'{self.keywords}-1688-{self.runtime}.csv', 'a', encoding='utf-8-sig', newline='')
        self.csvWriter = csv.DictWriter(self.csvStream,
                                        fieldnames=['item_name', 'item_price', 'item_shop', 'shop_link', 'item_link'])
        self.csvWriter.writerow(
            {'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'shop_link': '店铺链接', 'item_link': '商品链接'})

    def write_new_line(self, text):
        self.csvWriter.writerow(text)
        self.csvWriter.flush()

    def catch_err(self):
        winsound.PlaySound('error.wav', winsound.SND_FILENAME | winsound.SND_NOWAIT)

    def close_exit(self):
        self.csvStream.close()


class browserObj:
    def __init__(self):
        self.browserWin = webdriver.Chrome()

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

    def find_css_selector(self, css):
        return self.browserWin.find_element(By.CSS_SELECTOR, css)

    def close_exit(self):
        self.browserWin.close()


class tkGui():
    def __init__(self):
        self.tk = tkinter.Tk()
        self.tk.title('1688店铺信息获取器 Powered by zjc')
        self.tk['background'] = '#ffffff'
        self.tk.geometry("600x100-50+20")
        self.tk.attributes("-topmost", 1)
        self.status = tkinter.Label(self.tk, text='初始化', font=('微软雅黑', '20'))
        self.status.pack()
        self.label1 = tkinter.Label(self.tk, text='-', font=('微软雅黑', '10'))
        self.label2 = tkinter.Label(self.tk, text='-', font=('微软雅黑', '10'))
        self.label1.pack()
        self.label2.pack()

    def gui_loop(self):
        self.tk.mainloop()

    def write_statue(self, text, bgcolor='#fffff'):
        self.status['text'] = text
        if bgcolor == 'green':
            self.status['bg'] = '#10d269'
        if bgcolor == 'red':
            self.status['bg'] = 'red'
        self.status['bg'] = bgcolor

    def write_label(self, label1='-', label2='-'):
        self.label1['text'] = label1
        self.label2['text'] = label2
