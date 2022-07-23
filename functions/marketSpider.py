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

    def init_csv_file(self,market, fieldnames, cn_name):
        self.csvStream = open(f'{self.keywords}-{market}-{self.runtime}.csv', 'a', encoding='utf-8-sig', newline='')
        self.csvWriter = csv.DictWriter(self.csvStream,fieldnames=fieldnames)
        self.csvWriter.writerow(cn_name)
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

    def return_javascript(self, command):
        js_return = self.browserWin.execute_script(f'return {command}')
        return js_return

    def scroll_page(self):
        self.browserWin.execute_script("document.documentElement.scrollTop=100000")

    def find_css(self, css):
        return self.browserWin.find_element(By.CSS_SELECTOR, css)

    def close_exit(self):
        self.browserWin.close()
