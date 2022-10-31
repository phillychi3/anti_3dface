import re
from tkinter import *
import pyscreenshot as ImageGrab
import time
from detectface import Anti3dface
a3d = Anti3dface()

windows = []
tk = Tk()
transcoloe = "gray"
tk.wm_attributes("-transparentcolor", transcoloe)
def on_resize(event):
    tk.configure(width=event.width, height=event.height)
    canvas.create_rectangle(0,0,event.width,event.height,fill=transcoloe,outline=transcoloe)


def createwindows(x,y,w,h):
    global tk
    global canvas
    tk.title("Anti3DFace")
    tk.geometry(f"{x}x{y}+{w}+{h}")
    tk.resizable(0, 0)
    #tk.overrideredirect(1)

    canvas = Canvas(tk)
    canvas.pack(fill=BOTH, expand=YES)
    canvas.create_rectangle(0,0,canvas.winfo_width(),canvas.winfo_height(),fill=transcoloe,outline=transcoloe)
    canvas.configure(highlightthickness = 0)
    tk.bind("<Configure>", on_resize)
    tk.mainloop()
    return tk


def main():
    while True:
        if windows != []:
            windows[0].destroy()
            windows.clear()
        img = ImageGrab.grab()
        faces = a3d._face_detect(img)
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]
        newwindows = createwindows(x,y,w,h)
        windows.append(newwindows)
        time.sleep(1)
main()