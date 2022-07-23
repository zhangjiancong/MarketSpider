import csv
import json
import sys
import tkinter
from tkinter import filedialog
import time



def open_file_dialog(title='请打开HAR文件'):
    filePath = tkinter.filedialog.askopenfilename(title=title)
    if filePath == '':
        print('错误您没有打开任何har文件')
        sys.exit()
    return filePath


har = open_file_dialog()

har_file = open(har, 'r', encoding='utf-8')
har_file = har_file.read()
har_json = json.loads(har_file)
j_ahead = har_json['log']['entries']
nums = 0

csv_file = open(f'jingxi-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.csv', 'a', encoding='utf-8-sig',
                newline='')
csv_writer = csv.DictWriter(csv_file,
                            fieldnames=['item_id', 'item_url', 'item_name', 'item_pic', 'item_price', 'item_sales',
                                        'shop_url', 'shop_name'])
csv_writer.writerow(
    {'item_id': '商品ID', 'item_url': '商品链接', 'item_name': '商品名称', 'item_pic': '商品图片', 'item_price': '商品价格',
     'item_sales': '商品销量', 'shop_url': '店铺链接', 'shop_name': '店铺名称'})
csv_file.flush()


def read_json(req_text):
    json_data = json.loads(req_text)
    json_data = json_data['wareInfo']
    n=0
    for good in json_data:
        n=n+1
        print(f'\r  =>正在处理第 {n} 个商品', end="", flush=True)
        try:
            item_id = good["wareId"]
        except:
            item_id = ''
        try:
            item_url = good['toMURL']
        except:
            item_url = ''
        try:
            item_name = good['wname']
        except:
            item_name = ''
        try:
            item_pic = good['imageurl']
        except:
            item_pic = ''
        try:
            item_price = good['jdPrice']
        except:
            item_price = ''
        try:
            item_sales = good['reviews']
        except:
            item_sales = ''
        try:
            shop_url = good['toShopUrl']
        except:
            shop_url = ''
        try:
            shop_name = good['goodShop']['goodShopName']
        except:
            shop_name = ''

        csv_writer.writerow(
            {'item_id': item_id, 'item_url': item_url, 'item_name': item_name, 'item_pic': item_pic,
             'item_price': item_price, 'item_sales': item_sales, 'shop_url': shop_url, 'shop_name': shop_name})
        csv_file.flush()
    print('')

def read_html(html):
    try:
        html = html.split('\n')
        html_json = html[125].split('window._FIRST_PAGE_DATA =')
        jsons = html_json[1]
        read_json(jsons)
    except:
        return 0


for reqs in j_ahead:
    if reqs["_resourceType"] == 'xhr':
        if 'https://m.jingxi.com/searchv3/jxjson' in reqs['request']['url']:
            try:
                nums = nums + 1
                print(f'处理第 {nums} 个 类型:XHR')
                a = reqs['response']['content']['text']
                read_json(a)
            except:
                continue
    if reqs["_resourceType"] == 'document':
        if 'https://m.jingxi.com/searchv3/jxpage?' in reqs['request']['url']:
            try:
                nums = nums + 1
                print(f'处理第 {nums} 个 类型：Document')
                a = reqs['response']['content']['text']
                read_html(a)
            except:
                continue

print('\n\n\n========遍历完成===========\n\n')
csv_file.flush()
csv_file.flush()
csv_file.flush()
time.sleep(3)
