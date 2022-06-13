import json
import time
url=['https://www.taobao.com','https://www.jd.com','https://mobile.yangkeduo.com/login.html']
filename=['taobao','jd','pinduoduo']
print('操作流程:\n1-选择需要获取cookie的网站\n2-在弹出的窗口中手动操作进行登录\n3-cookie将自动保存')
print('\n输入数字打开网站\n0>淘宝[不能用！]\t1>京东\t2>拼多多(仅支持手机验证码登录)')
user=int(input())
print('请在稍后打开的窗口中登录,限时60秒')
from selenium import webdriver
driver=webdriver.Chrome()
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
