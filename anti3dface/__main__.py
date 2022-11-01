import pyscreenshot as ImageGrab
from detectface import Anti3dface
import cv2
import numpy as np
from io import BytesIO
import tkinter as tk
import time
import asyncio

a3d = Anti3dface()





class App():
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.transcoloe = "gray"
        self.root.wm_attributes("-transparentcolor", self.transcoloe)
        self.root.title('Anti3dface')
        self.root.geometry('300x200')
        self.root.resizable(0, 0)
        self.canvas = tk.Canvas(self.root)
        self.canvas.pack(fill=tk.BOTH, expand=tk.YES)
        self.canvas.create_rectangle(0,0,self.canvas.winfo_width(),self.canvas.winfo_height(),fill=self.transcoloe,outline=self.transcoloe)
        self.canvas.configure(highlightthickness = 0)
        self.root.bind("<Configure>", self.on_resize)
        self.image = tk.PhotoImage(file=r"C:\Users\phill\Pictures\1.png")
        self.la = tk.Label(image=self.image)
        self.la.place(x=0,y=0)

        self.get()
        
        

    def on_resize(self,event):
        self.root.configure(width=event.width, height=event.height)
        self.canvas.create_rectangle(0,0,event.width,event.height,fill=self.transcoloe,outline=self.transcoloe)


    def update_geometry(self,x,y,w,h):
        self.root.geometry(f'{w}x{h}+{x}+{y}')
        self.root.resizable(0, 0)
        self.root.update()




    def get(self):
        while True:
            print("running")
            img = ImageGrab.grab()
            buffer = BytesIO()
            img.save(buffer, 'png')
            buffer.seek(0)
            array = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
            img = cv2.imdecode(array, cv2.IMREAD_COLOR)
            grayimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            try:
                faces = a3d._face_detect(grayimage)
                for (x, y, w, h) in faces:
                    self.update_geometry(x,y,w,h)
            except:
                pass
                time.sleep(0.1)

App()
