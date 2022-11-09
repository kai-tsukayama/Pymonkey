import tkinter as tk
from pyai import *
from datetime import datetime
import tkinter.messagebox


entry = None
response_area = None
lb = None
action = None
pyai = Pyai("pyai")
on_canvas=None
pysaru_images=[]
log=[]


def putlog(str):
    lb.insert(tk.END, str)
    log.append(str+"\n")


def prompt():
    p = pyai.name
    if (action.get()) == 0:
        p += ":"+ pyai.responder.name
        return p+">"

def chagImg(img):
    canvas.itemconfig(
        on_canvas,
        image=pysaru_images[img]
    )

def change_looks():
    em=pyai.emotion.mood
    if -5<=em<=5:
        chagImg(0)
    elif -10<=em<=-5:
        chagImg(1)
    elif -15<=em<=-10:
        chagImg(2)
    elif 5<=em<=10:
        chagImg(4)
    elif 10<=em<=15:
        chagImg(3)


def talk():
    value = entry.get()
    if not value:
        response_area.configure(text="なに？")
    else:
        response = pyai.dialogue(value)
        response_area.configure(text=response)
        putlog(">"+value)
        putlog(prompt()+response)
        entry.delete(0, tk.END)

    change_looks()    

def writeLog():
    now="Pyai System Dialogue Log:"+datetime.now().strftime(
        "%Y-%m-%d %H:%m::%s"+"\n"
    )
    log.insert(0,now)
    with open("log.txt","a",encoding="utf_8") as f:
        f.writelines(log)

# ここから画面の設定


def run():
    global entry, response_area, lb, action,canvas,on_canvas,pysaru_images

    root = tk.Tk()
    root.geometry("880x560")
    root.title("Intelligent Agent : ")
    font = ("Helevetica", 14)
    font_log = ("Helevetica", 11)

    def callback():
        if tkinter.messagebox.askyesno(
            "Quit?","ランダム辞書を更新してもいいですか？"
            ):
            pyai.save()
            writeLog()
            root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW",callback)

    # メニューバー
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    # ファイルメニュー
    filemenu = tk.Menu(menubar)
    menubar.add_cascade(label="ファイル", menu=filemenu)
    filemenu.add_command(label="閉じる", command=callback)
    # オプションメニュー
    action = tk.IntVar()
    optionmenu = tk.Menu(menubar)
    menubar.add_cascade(label="オプション", menu=optionmenu)
    optionmenu.add_radiobutton(
        label="Responderを表示",
        variable=action,
        value=0
    )
    optionmenu.add_radiobutton(
        label="Responderを表示しない",
        variable=action,
        value=1
    )
    # キャンバスの作成
    canvas = tk.Canvas(
                root,
                width=500,
                height=300,
                relief=tk.RIDGE,
                bd=2
            )
    canvas.place(x=370, y=0)

    pysaru_images.append(tk.PhotoImage(file="nomal.gif"))
    pysaru_images.append(tk.PhotoImage(file="non.gif"))
    pysaru_images.append(tk.PhotoImage(file="oko.gif"))
    pysaru_images.append(tk.PhotoImage(file="tere.gif"))
    pysaru_images.append(tk.PhotoImage(file="wara.gif"))

    on_canvas=canvas.create_image(
        0,
        0,
        image=pysaru_images[0],
        anchor=tk.NW
    )
    # 応答エリアの作成
    response_area = tk.Label(
        root,
        width=50,
        height=10,
        bg="green",
        font=font,
        relief=tk.RIDGE,
        bd=2
    )
    response_area.place(x=370, y=305)
    # フレームの作成
    frame = tk.Frame(
        root,
        relief=tk.RIDGE,
        borderwidth=4
    )
    entry = tk.Entry(
        frame,
        width=70,
        font=font
    )
    entry.pack(side=tk.LEFT)
    entry.focus_set()
    # ボタンの作成
    button = tk.Button(
        frame,
        width=15,
        text="話す",
        command=talk
    )
    button.pack(side=tk.LEFT)
    frame.place(x=30, y=520)
    # リストボックスの作成
    lb = tk.Listbox(
            root,
            width=42,
            height=30,
            font=font_log
        )
    # 縦のスクロールバーの作成
    sb1 = tk.Scrollbar(
            root,
            orient=tk.VERTICAL,
            command=lb.yview
        )
    # 横のスクロールバーの作成
    sb2 = tk.Scrollbar(
            root,
            orient=tk.HORIZONTAL,
            command=lb.xview
        )
    # リストボックスとスクロールバーの連動
    lb.configure(yscrollcommand=sb1.set)
    lb.configure(xscrollcommand=sb2.set)
    lb.grid(row=0, column=0)
    sb1.grid(row=0, column=1, sticky=tk.NS)
    sb2.grid(row=1, column=0, sticky=tk.EW)
    # メインループ
    root.mainloop()


# プログラムの起点
if __name__ == '__main__':
    run()