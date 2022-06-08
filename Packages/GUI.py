import tkinter


class inputBox:
    def input_words(self, textType):
        res = 0
        root = tkinter.Tk()
        root.title(f'输入{textType}')
        root.geometry('300x100')
        tkinter.Label(root, text=f'输入{textType}').grid(row=0, column=0)
        s0 = tkinter.StringVar()
        inputEntry = tkinter.Entry(root, textvariable=s0)
        inputEntry.grid(row=0, column=1)

        def return_result(*args):
            global res
            res = inputEntry.get()
            print(res)
            root.destroy()
            return res

        tkinter.Button(root, text='确定', command=return_result).grid(row=1, column=0)
        root.mainloop()


box = inputBox()
gettes=box.input_words('s2')
print(f'R=>{gettes}')