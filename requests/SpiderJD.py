import json
import re
import requests
import csv
import time
import random
from urllib import parse

keyword=input('输入京东关键词:')
keywords=parse.quote(keyword)
pages=input('预计爬几页:')
print('jd_key和jd_pin均通过浏览器获得，有效期一般为7天')
input('输入jd_key')
input('输入jd_pin')
waitTime=40


with open(f'{keyword}.csv', 'a', encoding='ANSI',newline='') as filename:
    writer=csv.DictWriter(filename, fieldnames=['title','price','shop','shopLink'])
    for page in range(1,int(pages)+1):
        print(f'\n==Page{page}===')
        url =f'https://s.taobao.com/search?q={keywords}&commend=all&ssid=s5-e&search_type' \
             f'=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_2017030' \
             f'6&&s={page*44} '
        header = {
            # 'cookie':'cna=7YSbFtKkxjICAXQCtKCjC0Os; _m_h5_tk=b3d89064c1b97fce3642df0e477fd606_1653394112399; _m_h5_tk_enc=c8676b6cbd081532eb941ad678138268; _samesite_flag_=true; cookie2=198e2e96a020c87700185d7fd3778d66; t=599d9e8844d95ce58cbc4f9c3d066964; _tb_token_=57e7a5e8b0ee0; xlly_s=1; sgcookie=E100XkigyBH7Gv%2Fwf61IX%2F8xP1jA%2B2lQEPJflMPSYNOqEz32bmeCoM8xTi87tH1L%2BRotfUK0sQGg8UbcGYGhCt4Q%2BYc%2BKuWs2G7%2B047ie7dvUNg%3D; unb=2208742011542; uc3=id2=UUphwoAZvNEgGQE7Jg%3D%3D&lg2=U%2BGCWk%2F75gdr5Q%3D%3D&vt3=F8dCvC%2B02g4YEI2hQuE%3D&nk2=F5RHpxIDKL0%2BbBM%3D; csg=b7199c22; lgc=tb266433023; cancelledSubSites=empty; cookie17=UUphwoAZvNEgGQE7Jg%3D%3D; dnk=tb266433023; skt=2dcedf8a552176ff; existShop=MTY1MzM4MzczNQ%3D%3D; uc4=id4=0%40U2grGRiBh2KB7Wd14F00OHSdVmyZxRID&nk4=0%40FY4Mta35DhGjkWYmlN5izUgVBddS9w%3D%3D; tracknick=tb266433023; _cc_=W5iHLLyFfA%3D%3D; _l_g_=Ug%3D%3D; sg=32b; _nk_=tb266433023; cookie1=VqxCmqCi5fw7a7KeTor%2BeLWtj86aL8qtYk38tcQ8KZo%3D; uc1=cookie15=V32FPkk%2Fw0dUvg%3D%3D&existShop=false&cookie21=WqG3DMC9Eman&pas=0&cookie16=WqG3DMC9UpAPBHGz5QBErFxlCA%3D%3D&cookie14=UoexMSyWRvURrg%3D%3D; alitrackid=i.taobao.com; lastalitrackid=i.taobao.com; enc=STvGX6CHbOi9BoYQgneV0gpPjRx1VWThwnMjGk1cX9gj6J%2FICKGyMYiUrPeWLWFDXbxULY2u%2F2uD2iu7mWsq50kmYRKOkf8xrjR9pXkL%2F2o%3D; x5sec=7b227365617263686170703b32223a223635396538623833386431363635376639356266396139393265393566323865434a585773705147454e486b36616d742f63573161426f504d6a49774f4463304d6a41784d5455304d6a73784b414977703457436e767a2f2f2f2f2f41513d3d227d; JSESSIONID=4C866A8FBDEE80C60407F0A59A9A5EDF; tfstk=cIklBiY12bP5ELVm1LwWdGvpAVdAatAzPvkq33bqa7BnAhH44sflg1yJMn4J5U5C.; l=eBTpRKeRLmjGyAEEBOfCnurza779xIRYouPzaNbMiOCP_WCp5l6lW6fKqNT9CnGVh6UpR3R7wXp0BeYBqiVBfdW22j-laQMmn; isg=BJGRzejLlyy0Fvs4QiB5p7lyoJ0r_gVwF_NCRHMmydh3GrFsu06mQC04vO78FJ2o',
            'cookie':inputCookie,
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.taobao.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
        }
        res = requests.get(url=url, headers=header)
        try:
            aa = re.findall('g_page_config = (.*);', res.text)[0]
        except:
            print(res.text)
            exit(400)
        json_data = json.loads(aa)
        aa = json_data['mods']['itemlist']['data']['auctions']
        for index in aa:
            dict = {'title': index['raw_title'],
                    'price':index['view_price'],
                    'shop':index['nick'],
                    'shopLink':index['shopLink']}
            writer.writerow(dict)

        timesleep=random.randint(20,waitTime+1)
        for times in range(0,timesleep):
            print(f'\r等待:{times}\t eta:{timesleep}',end="",flush=True)
            time.sleep(1)
