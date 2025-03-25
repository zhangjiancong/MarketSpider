# V1.1
import json
import os
import time


def check_requirements_isinstalled():
    try:
        import requests
        from playsound import playsound
        from selenium import webdriver

        return True
    except:
        return False


def fix_requirements():
    with open("requirements.txt", "r") as fp:
        list = fp.readlines()
        for index, packages in enumerate(list):
            packages = packages.replace("\n", "")
            print(
                f'\n{"="*24}\n\n-> 正在尝试安装 ({index+1}/{len(list)}) {packages} \n\n{"="*24}\n'
            )
            os.system(f"pip install {packages}")


def check_configFile_exist():
    try:
        config_file = open("config.json", "r")
        config_file = json.load(config_file)
        b = config_file["browser"]
        return False
    except:
        return True


def create_configFile():
    config = {}
    print("您可以输入对应选项前的数字,并按下回车键确认")
    print("\n" + "=" * 30)
    print("? 选择使用的浏览器")
    print("-> 1 Chrome \n-> 2 Edge \n-> 3 Firefox")
    match input(""):
        case "1":
            config["browser"] = "chrome"
        case "2":
            config["browser"] = "edge"
        case "3":
            config["browser"] = "firefox"
        case "_":
            print("输入不合法")
            return
    config["create_time"] = int(time.time())
    with open("config.json", "w") as fp:
        fp.write(json.dumps(config))


def scan_all_cookie():
    if not os.path.exists("cookie"):
        os.mkdir("cookie")
    cookie = os.listdir("cookie")
    return cookie


def runtime_check():
    total = 2
    print("正在运行前检查\r", end="")
    if not check_requirements_isinstalled():
        print("[!] 未通过: 运行依赖")
        total -= 1
    if check_configFile_exist():
        print("[!] 未通过: 配置文件")
        total -= 1
    if total == 2:
        print(" " * 14)
        return False
    else:
        return True

def toLocaleTimeString(timestamp):
    if isinstance(timestamp, time.struct_time):
        return time.strftime("%Y-%m-%d %H:%M:%S", timestamp)
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(timestamp))


while runtime_check():
    print("  1   修复 [运行依赖]")
    print("  2   修复 [配置文件]")
    print("\n\n")
    match input("输入数字执行对应修复:"):
        case "1":
            fix_requirements()
        case "2":
            create_configFile()

while True:
    print("-" * 20 + "MarketSpider Starter 启动器" + "-" * 20 + "\n")
    configFile = json.loads(open("config.json", "r").read())
    print(
        f"<配置文件>\n - 浏览器\t{configFile['browser']}\n - 建立时间\t{toLocaleTimeString(configFile['create_time'])}"
    )
    print("\n<已保存的Cookie>")
    cookie = scan_all_cookie()
    for c in cookie:
        maketime = time.localtime(os.stat("cookie\\" + c).st_mtime)
        print(f"{toLocaleTimeString(maketime)}\t {c}")
    print("[!] 大于3个月的Cookie可能失效,建议您重新保存")
    print("\n" + "-" * 20)
    print("1 编辑配置文件\t\t2 获取Cookie")
    print("3 更新工具")
    print("4 淘宝\t\t5 京东")
    print("6 1688\t\t")
    match input("输入序号打开对应功能:"):
        case "1":
            create_configFile()
        case "2":
            os.system("python GetCookie.py")
        case "3":
            os.system("python Update.py")
        case "4":
            os.system("python Spider_taobao.py")
        case "5":
            os.system("python Spider_jd.py")
        case "6":
            os.system("python Spider_1688.py")
        case "_":
            print("这个数字暂无功能")
