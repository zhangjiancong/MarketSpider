# V2.0
import time
import Core

l = Core.Logger("GetCookie")
g = Core.Gui("GetCookie")
# 检查配置文件存在性并生成
if Core.check_configFile_exist():
    Core.show_error_box(
        "配置文件异常", "未找到配置文件.\n请打开<Starter.py>生成配置文件"
    )
driver = Core.BrowserControl(Core.pre_check_configFile(), g,l)
url = [
    "https://login.taobao.com/member/login.jhtml?redirectURL=http%3A%2F%2Fwww.taobao.com%2F",
    "https://www.jd.com",
    "https://mobile.yangkeduo.com/login.html",
    "https://login.taobao.com/?redirect_url=https%3A%2F%2Flogin.1688.com%2Fmember%2Fjump.htm%3Ftarget%3Dhttps%253A%252F%252Flogin.1688.com%252Fmember%252FmarketSigninJump.htm%253FDone%253Dhttps%25253A%25252F%25252Fwww.1688.com%25252F%25253Fspm%25253Da26352.13672862.pcnewalibar.d5.1fa67c26MSitx3&style=tao_custom&from=1688web",
]
filename = ["taobao", "jd", "pinduoduo", "1688"]
g.set_text("等待打开商城", g.COLOR_ATTENTION)
print(
    "操作流程:\n1-选择需要获取cookie的网站\n2-在弹出的窗口中手动操作进行登录\n3-登陆成功后无需操作，等待cookie自动保存"
)
print(
    "\n输入数字打开网站\n0>淘宝\t1>京东\t2>拼多多(仅支持手机验证码登录)\t3>阿里巴巴1688"
)
Core.show_info_box(
    "操作流程提示",
    "操作流程:\n1-选择需要获取cookie的网站\n2-在弹出的窗口中手动操作进行登录\n3-登陆成功后无需操作，等待cookie自动保存",
)
user = int(
    g.ask_string(
        "选择商城", "0>淘宝\t1>京东\t2>拼多多(仅支持手机验证码登录)\t3>阿里巴巴1688"
    )
)
print("请在稍后打开的窗口中登录,限时60秒")
g.set_text("请在稍后打开的窗口中登录")
time.sleep(3)
try:
    # 跳转网站
    driver.navi_to(url[user])
    print("请登录，请在60秒内完成！")
    g.set_text("请登录，请在60秒内完成！")
    g.set_status("请登录,登录成功后无需操作,等待倒计时结束")
    # 倒计时
    for delaytime in range(0, 61):
        g.set_progress(delaytime, 61)
        print(f"\r已等待:{delaytime}\t eta:{60-delaytime}", end="", flush=True)
        time.sleep(1)
    g.set_text("正在保存请稍后")
    err = driver.save_cookie(filename[user])
    try:
        driver.save_storage(filename[user])
    except:
        print('------------------------------err storage')
    if not err:
        g.set_text("保存成功", g.COLOR_RUNNING)
        g.set_status("保存成功，程序将稍后退出")
        print("\nCookie已成功保存")
    else:
        print("\nCookie 保存失败")
    driver.exit()
    time.sleep(5)
except Exception as e:
    print(e)
    l.write_error("保存Cookie时失败" + str(e), True)
