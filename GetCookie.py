import json
import time
VERSION='1.1'
print(f'程序版本{VERSION}\n最新程序下载地址:https://github.com/zhangjiancong/MarketSpider')
url=['https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F','https://www.jd.com','https://mobile.yangkeduo.com/login.html','https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Fspm%25253Da26352.13672862.pcnewalibar.d5.1fa67c26MSitx3&style=tao_custom&from=1688web']
filename=['taobao','jd','pinduoduo','1688']
print('操作流程:\n1-选择需要获取cookie的网站\n2-在弹出的窗口中手动操作进行登录\n3-登陆成功后无需操作，等待cookie自动保存')
print('\n输入数字打开网站\n0>淘宝\t1>京东\t2>拼多多(仅支持手机验证码登录)\t3>阿里巴巴1688')
user=int(input())
print('请在稍后打开的窗口中登录,限时60秒')
time.sleep(3)
from selenium import webdriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
driver=webdriver.Chrome(options=options)
driver.get(url[user])
print('请登录，请在60秒内完成！')
for delaytime in range(0,61):
    print(f'\r已等待:{delaytime}\t eta:{60-delaytime}', end="", flush=True)
    time.sleep(1)
with open(f'{filename[user]}.cookie','w') as file:
    if user==0:
        file.write(json.dumps(driver.get_cookies()))
    if user!=0:
        file.write(json.dumps(driver.get_cookies()))
driver.close()
driver.quit()
print('\nCookie已保存')
time.sleep(5)
