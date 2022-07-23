import os.path

from functions.marketSpider import *
import sys
import time
import random
import tkinter
from threading import Thread
import logging
import os
def mknewdir(dirname):
    if not os.path.exists(f'{dirname}'):
        nowdir=os.getcwd()
        os.mkdir(nowdir+f'\\{dirname}')




logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
mknewdir('logs')
file_handler = logging.FileHandler(os.path.join("./logs","1688.log"), mode='a+')
file_handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - Line:%(lineno)d - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.info('start')

# 全局GUI文字
status = tkinter.Label()
label1 = tkinter.Label()
label2 = tkinter.Label()


def gui_loop():
    global status
    global label1
    global label2
    root = tkinter.Tk()
    root.title('1688店铺信息获取器 Powered by zjc')
    root['background'] = '#ffffff'
    root.geometry("600x100-50+20")
    root.attributes("-topmost", 1)
    status = tkinter.Label(root, text='初始化', font=('微软雅黑', '20'), bg='#ffffff')
    status.pack()
    label1 = tkinter.Label(root, text='-', font=('微软雅黑', '10'), bg='#ffffff')
    label2 = tkinter.Label(root, text='-', font=('微软雅黑', '10'), bg='#ffffff')
    label1.pack()
    label2.pack()
    root.mainloop()


def write_statue(showtext, bgcolor='#ffffff'):
    status['text'] = showtext
    if bgcolor == 'green':
        status['bg'] = '#00f400'
        return 1
    if bgcolor == 'red':
        status['bg'] = 'red'
        return 1
    status['bg'] = bgcolor
    status['text'] = showtext
    return 0


def write_label(label1text='-', label2text='-'):
    label1['text'] = label1text
    label2['text'] = label2text


# GUI线程
Gui_thread = Thread(target=gui_loop)
Gui_thread.setDaemon(True)
Gui_thread.start()
time.sleep(3)

write_statue('☞等待搜索关键词', '#ffff99')
keywords = input('输入搜索关键词:')
logger.info(f'get keyword={keywords}')

browser = browserObj()
spider = Spider(keywords)

spider.init_csv_file('1688',['item_name', 'item_price', 'item_shop', 'shop_link', 'item_link'],{'item_name': '商品名', 'item_price': '商品价格', 'item_shop': '店铺名称', 'shop_link': '店铺链接', 'item_link': '商品链接'})
write_statue('启动浏览器中')
browser.navi_to('https://s.1688.com/selloffer/offer_search.htm')
write_statue('尝试添加Cookie')
browser.add_cookie()
write_statue('搜索商品中')
browser.find_css('#alisearch-input').send_keys(keywords)
browser.find_css(
    '#app > div > div.space-common-searchbox > div.header-container > div > div.searchbox-container > div > div > div.ali-search > form > fieldset > div > div.alisearch-action > button').click()
time.sleep(10)
getPage = browser.find_css(
    '#app > div > div.space-common-pagination > div > div > div > span.fui-paging-total > em').text
write_statue('☞等待获取页数', '#ffff99')
write_label(f'已找到{getPage}页', '输入起始页和终点页')
print(f'已找到{getPage}页，请按照提示输入页数')
logger.info(f'get 1688 have pages {getPage}')
StartPage = int(input('起始页数:'))
EndPage = int(input('截止页数:')) + 1
logger.info(f'get startPage{StartPage};get EndPage{EndPage - 1}')
searchUrl = browser.browserWin.current_url
exitSignal = False
for page in range(StartPage, EndPage):
    if page != 1:
        browser.navi_to(searchUrl + f'&beginPage={page}')
    write_statue(f'当前正在获取第{page}页，还有{EndPage - StartPage - page}页', 'green')
    write_label()
    for i in range(1, 5):
        browser.scroll_page()
        time.sleep(3)

    try:
        goods_arr = browser.browserWin.find_elements(By.CSS_SELECTOR, '#sm-offer-list>div')
        goods_length = len(goods_arr)
    except:
        try:
            notifimsg = browser.find_css(
                '#app > div > div.space-common-offerlist > div:nth-child(3) > div > div > div.noresult-content > h2').text
            if notifimsg == '没找到相关的商品':
                write_statue(f'{page}页开始无商品，程序退出', 'red')
                print(f'{page}页进入无相关商品页面，退出')
                logger.critical(f'fail get goods in page{page},return cannot found goods,exit')
                exitSignal = True
                break
        except:
            pass
        write_statue(f'出错：如有验证请验证。程序暂停30秒可供自由操作', 'red')
        write_label(f'注意：第{page}页获取将跳过，请重新运行获取该页！')
        print('获取商品列表出错')
        logger.warning(f'catch a error in page{page},maybe need to Captcha,this page will be jumped')
        spider.catch_err()
        time.sleep(30)
        continue
    if exitSignal == True:
        break
    for num in range(1, goods_length + 1):
        try:
            write_statue(f'当前正在获取第{page}页，还有{EndPage - StartPage - page}页', 'green')
            write_label(f'正在获取第{num}个，共计{goods_length}个')
            try:
                item_name = browser.find_css(
                    f'#sm-offer-list > div:nth-child({num}) > div > div.mojar-element-title.mojar-element-title-one-line > a > div').text
            except:
                item_name = browser.find_css(
                    f'#sm-offer-list > div:nth-child({num}) > div > div.mojar-element-title > a > div').text
            item_price = browser.find_css(
                f'#sm-offer-list > div:nth-child({num}) > div > div.mojar-element-price > div.showPricec > div.price').text
            item_shop = browser.find_css(
                f'#sm-offer-list > div:nth-child({num}) > div > div.mojar-element-company > div.company-name > a > div').text
            shop_link = browser.find_css(
                f'#sm-offer-list > div:nth-child({num}) > div > div.mojar-element-company > div.company-name > a').get_attribute(
                'href')
            item_link = browser.find_css(
                f'#sm-offer-list > div:nth-child({num}) > div > div.img-container > div > a').get_attribute('href')
            spider.write_new_line(
                {'item_name': item_name, 'item_price': item_price, 'item_shop': item_shop, 'shop_link': shop_link,
                 'item_link': item_link})
        except:
            logger.warning(f'get item{num} in page{page} failed,jump this goods')
            write_statue(f'出错：如有验证请验证。程序暂停5秒可供自由操作', 'red')
            write_label(f'item{num} in page{page}广告类商品或未知属性商品过滤')
            print(f'item{num} in page{page}广告类商品或未知属性商品过滤')
            spider.catch_err()
            time.sleep(5)
            continue

    if page == EndPage:
        break

    delay_time = random.randint(10, 30)
    for delay in range(delay_time):
        write_statue(f'已获取第{page}页，还有{EndPage - StartPage - page}页', '#ffffff')
        write_label('当前正在随机延时翻页', f'已延时{delay}秒，剩余{delay_time - delay}秒')
        time.sleep(1)

print('程序结束')
logger.info('exit')
write_statue('程序结束，正在保存文件')
browser.close_exit()
spider.close_exit()
write_statue('保存结束，准备退出')
time.sleep(5)
sys.exit(0)
