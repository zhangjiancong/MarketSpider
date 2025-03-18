# V2.0.0
import sys
import time
import random
import traceback
from selenium.webdriver.common.by import By
import Core


try:
    ilog = Core.Logger("jd")
    bot_gui = Core.Gui("京东")

    # 获取商品关键词
    bot_gui.set_text("请输入商品关键词", bot_gui.COLOR_ATTENTION)
    keyword = bot_gui.ask_string("请输入商品关键词", "输入商品关键词")
    if len(keyword) < 1:
        bot_gui.set_text("ERROR：商品关键词为空", bot_gui.COLOR_ERROR)
        ilog.write_error("商品关键词为空请检查您的输入.", dialog=True)
        sys.exit(1)

    # 初始化浏览器
    bot_gui.set_text("程序正在准备", bot_gui.COLOR_DEFAULT)
    bot_gui.set_status("正在初始化csv...")
    csv = Core.CsvWriter(keyword, "jd")
    browser = Core.BrowserControl(Core.pre_check_configFile(), bot_gui, ilog)
    # 注入Cookie
    browser.navi_to("https://www.jd.com")
    browser.inject_cookie("jd")
    # 发起搜索
    bot_gui.set_text("发起搜索")
    browser.navi_to(f"https://search.jd.com/Search?keyword={keyword}")

    page_total = browser.find_element_css("#J_topPage > span > i").text
    bot_gui.set_text("范围设定", bot_gui.COLOR_ATTENTION)
    bot_gui.set_status(f"共计{page_total}页,请在弹出的窗口中输入范围")
    page_start = int(
        bot_gui.ask_string("爬取范围设定 - 开始页数", f"输入爬取范围的开始页数,最小值1")
    )
    page_end = int(
        bot_gui.ask_string(
            "爬取范围设定 - 结束页数", f"输入爬取范围的结束页数,最大页数为{page_total}"
        )
    )
    ilog.write_info(f"spider search range:{page_start}->{page_end} total:{page_total}")

    for page in range(page_start, page_end + 1):
        try:
            bot_gui.set_text("正在运行", bot_gui.COLOR_RUNNING)
            # browser.browser.execute_script(f"SEARCH.page({2 * page - 1}, true)")
            browser.navi_to(
                f"https://search.jd.com/Search?keyword={keyword}&page={2 * page - 1}"
            )
            bot_gui.set_progress(page - page_start, page_end - page_start + 1)
            time.sleep(2)
            browser.scroll_page_end()
            goods_array = browser.browser.find_elements(
                By.CSS_SELECTOR, "#J_goodsList > ul > li"
            )
            for index, good in enumerate(goods_array):
                bot_gui.set_status(f"正在保存商品数据...{index}/{len(goods_array)}")
                try:
                    data = {}
                    data["item_link"] = browser.find_element_css(
                        "div>div.p-img>a", good
                    ).get_attribute("href")
                    data["item_name"] = browser.find_element_css(
                        "div>div.p-name>a>em", good
                    ).text
                    data["item_price"] = browser.find_element_css(
                        "div>div.p-price>strong>i", good
                    ).text
                    data["item_image"] = browser.find_element_css(
                        "div>div.p-img>a>img", good
                    ).get_attribute("src")
                    data["item_rates"] = browser.find_element_css(
                        "div>div.p-commit>strong>a", good
                    ).text
                    data["item_shop"] = browser.find_element_css(
                        "div>div.p-shop>span>a", good
                    ).text
                    data["shop_link"] = browser.find_element_css(
                        "div>div.p-shop>span>a", good
                    ).get_attribute("href")
                    csv.write_new_line(data)
                except Exception as e:
                    ilog.write_error(f"获取单个商品信息时出错:{e}")
            bot_gui.set_text("正在延时", bot_gui.COLOR_DEFAULT)
            browser.setTimeout(random.randint(1, 10), "反机器人验证")

        except:
            bot_gui.set_text(
                f"在爬取页面{page}时异常.\n如有人机验证请验证", bot_gui.COLOR_ERROR
            )
            ilog.write_error(f"在爬取页面{page}时异常.\n如有人机验证请验证", True)
            browser.setTimeout(20, "异常,可能您正在操作人机验证")

    ilog.write_info("Spider Successful")
    bot_gui.set_text("程序结束!", bot_gui.COLOR_ATTENTION)
    bot_gui.set_status("正在进行最后处理,请稍后...")
    csv.close_csv()
    browser.exit()
    ilog.write_info("Exit...")
    bot_gui.set_text("即将退出", bot_gui.COLOR_DEFAULT)
    browser.setTimeout(5, "保存文件完成,即将退出...")
    sys.exit(0)

except Exception as e:
    print(f"未捕获的错误:{e}")
    print(traceback.format_stack())
    input("---Error---")
