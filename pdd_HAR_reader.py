import csv
import json
import tkinter
import sys
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

csv_file = open(f'PDD-{time.strftime("%Y-%m-%d_%H-%M", time.localtime())}.csv', 'a', encoding='utf-8-sig', newline='')
csv_writer = csv.DictWriter(csv_file,
                            fieldnames=['goods_id', 'goods_name', 'goods_pic', 'mall_id', 'price', 'has_saled'])
csv_writer.writerow({'goods_id': '商品ID', 'goods_name': '商品名', 'goods_pic': '商品图片', 'mall_id': '店铺ID', 'price': '价格',
                     'has_saled': '参考销售量'})
csv_file.flush()


def read_json(Reqtext):
    json_data = json.loads(Reqtext)
    json_data = json_data['items']
    for good in json_data:
        info = good['item_data']['goods_model']
        try:
            ss = info['sales']
        except:
            try:
                ss = info['sales_tip']
            except:
                ss = '未知'
        csv_writer.writerow(
            {'goods_id': info['goods_id'], 'goods_name': info['goods_name'], 'goods_pic': info['hd_thumb_url'],
             'mall_id': info['mall_id'], 'price': info['price_info'],
             'has_saled': ss})
        csv_file.flush()


for reqs in j_ahead:
    if reqs["_resourceType"] == 'xhr':
        if 'proxy/api/search?' in reqs['request']['url']:
            nums = nums + 1
            print(nums)
            try:
                a = reqs['response']['content']['text']
                read_json(a)
            except:
                continue

print('========遍历完成===========')
csv_file.flush()
csv_file.flush()
csv_file.flush()
time.sleep(3)
