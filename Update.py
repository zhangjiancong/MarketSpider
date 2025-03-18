# V1.1
import functools
import os
import time
import tkinter as tk
from tkinter import Variable, ttk
from tkinter.messagebox import showinfo, showerror
import json
import requests
from threading import Thread, local
from contextlib import closing

tableConfig = []
statusInfo = {"text": "", "progress": ""}
app = ""



def gui_func():
    global tableConfig
    global statusInfo
    global app
    app = tk.Tk()

    app.title("MarketSpider Updater")
    tk.Label(app, text="MarketSpider 更新程序", font=("Arial", 18)).pack()
    tk.Label(app, text="更新程序仅从main分支获取,如需其他文件请前往项目页面.").pack()
    versionTable = tk.Frame(app)
    versionTable.pack(padx=20)

    tk.Label(versionTable, text="组件文件").grid(column=0, row=1)
    tk.Label(versionTable, text="组件描述").grid(column=1, row=1)
    tk.Label(versionTable, text="本地版本").grid(column=2, row=1)
    tk.Label(versionTable, text="远程版本").grid(column=3, row=1)

    tableConfig = [
        {"comp": "Core", "description": "核心", "row": 2, "local": 1, "remote": 1},
        {
            "comp": "GetCookie",
            "description": "用于自动化获取登录cookie",
            "row": 3,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "taobaoSpider",
            "description": "淘宝网爬虫程序",
            "row": 4,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "Spider_jd",
            "description": "京东商城爬虫程序",
            "row": 5,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "1688Spider",
            "description": "阿里巴巴1688爬虫程序",
            "row": 6,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "jingxi_HAR_reader",
            "description": "京喜HAR读取程序",
            "row": 7,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "pdd_HAR_reader",
            "description": "拼多多HAR读取程序",
            "row": 8,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "Update",
            "description": "更新程序",
            "row": 9,
            "local": 1,
            "remote": 1,
        },
        {
            "comp": "Starter",
            "description": "启动器",
            "row": 10,
            "local": 1,
            "remote": 1,
        },
    ]

    for c in tableConfig:
        tk.Label(versionTable, text=c["comp"]).grid(column=0, row=c["row"], sticky="w")
        tk.Label(versionTable, text=c["description"]).grid(
            column=1, row=c["row"], sticky="w"
        )
        c["local"] = tk.Label(versionTable, text="正在获取...")
        c["local"].grid(column=2, row=c["row"], padx=6)
        c["var_remote"] = Variable()
        c["remote"] = tk.Label(versionTable, textvariable=c["var_remote"])
        c["remote"].grid(column=3, row=c["row"], padx=6)
        tk.Button(
            versionTable,
            text="更新",
            command=functools.partial(update_handler, c["comp"]),
        ).grid(column=4, row=c["row"], pady=4)
    linkText = tk.Label(
        app, text="项目地址:https://github.com/zhangjiancong/MarketSpider"
    )
    linkText.bind(
        "<Button-1>",
        lambda event: os.system("start https://github.com/zhangjiancong/MarketSpider"),
    )
    linkText.pack()
    statusInfo["progress"] = tk.ttk.Progressbar(app, mode="determinate")
    statusInfo["progress"].pack(fill=tk.X)
    statusInfo["text"] = tk.Label(
        app,
        text="请查看版本信息并点击对应的更新按钮",
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W,
    )
    statusInfo["text"].pack(fill=tk.X)
    app.mainloop()


def get_remote_version():
    global tableConfig
    try:
        get_release_version = requests.get(
            "https://zhangjiancong.github.io/MarketSpider/pages/version.json",
            timeout=10,
        )
        if get_release_version.status_code == 200:
            version_remote = get_release_version.json()
            if version_remote["notification"] != "":
                showinfo("通知 - MarketSpider 更新程序", version_remote["notification"])
            for index in version_remote:
                for comp in tableConfig:
                    if comp["comp"] == index:
                        comp["var_remote"].set(version_remote[index]['version'])
                        break

        else:
            showerror(
                "获取失败 - MarketSpider 更新程序",
                f"获取远程版本信息失败.请稍后再试.\nerr:network{get_release_version.status_code}",
            )
    except:
        showerror(
            "获取失败 - MarketSpider 更新程序",
            f"获取远程版本信息失败.\n网络超时,请稍后再试.\nerr:fail to connect to github",
        )


def get_local_version():
    global tableConfig
    time.sleep(5)
    for c in tableConfig:
        try:

            f = open(f"{c['comp']}.py", "r", encoding="utf8")
            g = f.readline().replace("# V", "").replace("\n", "")
            c["local"]["text"] = g
        except Exception as e:
            print(e)
            c["local"]["text"] = "获取失败"



def update_handler(target):
    global tableConfig
    global statusInfo
    global app

    url = "https://zhangjiancong.github.io/MarketSpider/" + target + ".py"
    with closing(requests.get(url, stream=True)) as response:
        global statusInfo
        total = int(response.headers["Content-Length"])  # 内容体总大小
        done = 0
        with open(target + ".py", "wb") as file:

            for data in response.iter_content():
                file.write(data)
                done = done + len(data)
                donePercent = int(done / total * 100)

                statusInfo["progress"]["value"] = donePercent
                statusInfo["text"]["text"] = f"{target}正在更新...{donePercent}%"
                app.update()
    statusInfo["text"]["text"] = f"更新{target}成功"
    showinfo("更新成功 - MarketSpider 更新程序", f"更新{target}成功,重新启动后生效.")



Thread(target=get_remote_version, daemon=True).start()
Thread(target=get_local_version, daemon=True).start()
gui_func()
