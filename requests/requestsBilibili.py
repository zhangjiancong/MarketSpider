import json
import re
import requests
import csv
import time
import random
with open('../tb.csv', 'w', encoding='ANSI', newline='') as filename:
    writer=csv.DictWriter(filename,fieldnames=['title'])
    for page in range(1,10):
        print(f'==Page{page}===')
        url =f'https://s.taobao.com/search?q=%E6%AF%9B%E7%BB%92%E7%8E%A9%E5%85%B7&commend=all&ssid=s5-e&search_type' \
             f'=item&sourceId=tb.index&spm=a21bo.jianhua.201856-taobao-item.2&ie=utf8&initiative_id=tbindexz_2017030' \
             f'6&&s={page*44} '
        header = {
            'cookie': 'lgc=zhangjiancong9315; tracknick=zhangjiancong9315; enc=o7wT9cXLMGQjofXyfAyICUyd7qfYU5tpRS3P3Puw57VsQC1du%2FkwcCsetxn9yEwIK75SJ7jF2NWPCz%2BrKbxdvg%3D%3D; thw=cn; cna=z03YGmazkF4CAa+sPgYgZXES; t=37eeff2e5ecea93ce9fd2293e9bc491d; xlly_s=1; _tb_token_=e8731b8e33330; _m_h5_tk=8a3c9565c175888cdaa91ffaafe3e292_1653319205122; _m_h5_tk_enc=f7e62fc880408a655e5eb7f7249412d8; cookie2=17d82fc3876ad65c7ed16481065bacbd; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=CDC536B0DE168B637CE2C4D0DA97C9BC; _samesite_flag_=true; sgcookie=E100BieccnnXIR3uLNuBezX2u9a2JnRIP5217iYpDEsamF8IAQGuRMy2UfZLPYmLPMOqRhqkFG%2FbNXCsfg7FzKl2KUSX1mSL%2FpkDh24emp4Ly6U%3D; unb=2816892760; uc3=vt3=F8dCvC%2B03SYd7ylvQMc%3D&nk2=GcAxdWUpHOoo%2Bd0iibIbzUU%3D&lg2=UtASsssmOIJ0bQ%3D%3D&id2=UUBZFxR7AdI2yg%3D%3D; csg=273ca6c8; cancelledSubSites=empty; cookie17=UUBZFxR7AdI2yg%3D%3D; dnk=zhangjiancong9315; skt=2a1421c83b78640f; existShop=MTY1MzMxMTgxNQ%3D%3D; uc4=nk4=0%40GwlAyxkZtpK4oiknSo9FmEaWx1MB%2Fc9C8g5y1A%3D%3D&id4=0%40U2LLFPWa4PBwceHqqruuoaw2RQUf; _cc_=VFC%2FuZ9ajQ%3D%3D; _l_g_=Ug%3D%3D; sg=508; _nk_=zhangjiancong9315; cookie1=B0T8J0EwZ%2B8puDrcxV4iEfqN%2Ft69wjCwhkfl4pl7NJo%3D; tfstk=caEGBFZBoPusQ-33PGi1cKc0787dZzxqZorQYOAZUyjbEoqFifYezDGAKff5_E1..; l=eBLyk2n4LRXZ5u35BOfZnurza77TsIRfguPzaNbMiOCP_kfp5bc1W6figC89CnGVnsAJ-3rk8yhLBPLaMyznQxv9-e_7XPQobdLh.; mt=ci=11_1; uc1=cookie21=UtASsssme%2BBq&cookie14=UoexMSyfqcml%2Fg%3D%3D&pas=0&cookie16=VT5L2FSpNgq6fDudInPRgavC%2BQ%3D%3D&cookie15=WqG3DMC9VAQiUQ%3D%3D&existShop=false; isg=BJGRxOmulyuWc_v9bBPSvaI2oJ0r_gVwtevyb3MmCth3GrNsu00cQFt4vO78Ep2o',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                      'application/signed-exchange;v=b3;q=0.9',
            'referer': 'https://www.taobao.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53'
        }
        res = requests.get(url=url, headers=header)
        print(len(res.text))
        aa = re.findall('g_page_config = (.*);', res.text)[0]
        json_data = json.loads(aa)
        aa = json_data['mods']['itemlist']['data']['auctions']
        for index in aa:
            dict = {'title': index['raw_title']}
            print(dict)
            writer.writerow(dict)

        time.sleep(random.randint(20,30))

