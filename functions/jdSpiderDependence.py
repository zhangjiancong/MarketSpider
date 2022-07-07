import re


def shop_id_get(shopid):
    shopid = shopid.split('index-')[1]
    shopid = shopid.split('.html')[0]
    if bool(re.findall('^(?=1000)', shopid)):
        return '京东自营'
    return shopid
