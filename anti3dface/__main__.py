import re
from tkinter import *
import pyscreenshot as ImageGrab
import time
from detectface import Anti3dface
import cv2
import numpy as np
from io import BytesIO
import threading
a3d = Anti3dface()

class gui(threading.Thread):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.tk = Tk()
        self.transcoloe = "gray"
        self.tk.wm_attributes("-transparentcolor", self.transcoloe)
        self.canvas = None
        self._stop_event = threading.Event()
    
    def stop(self):
        self.tk.destroy()
        self._stop_event.set()
    
    def stopped(self):
        return self._stop_event.is_set()


    def on_resize(self,event):
        self.tk.configure(width=event.width, height=event.height)
        self.canvas.create_rectangle(0,0,event.width,event.height,fill=self.transcoloe,outline=self.transcoloe)

    


    def createwindows(self,x,y,w,h):
        self.tk.title("Anti3DFace")
        self.tk.geometry(f"{w}x{h}+{x}+{y}")
        self.tk.resizable(0, 0)
        #tk.overrideredirect(1)

        self.canvas = Canvas(self.tk)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.create_rectangle(0,0,self.canvas.winfo_width(),self.canvas.winfo_height(),fill=self.transcoloe,outline=self.transcoloe)
        self.canvas.configure(highlightthickness = 0)
        self.tk.bind("<Configure>", self.on_resize)
        self.tk.mainloop()
        return self.tk


def main():
    works = []
    while True:
        #kill worls
        if works != []:
            for i in works:
                i.join()
        img = ImageGrab.grab()
        buffer = BytesIO()
        img.save(buffer, 'png')
        buffer.seek(0)
        array = np.asarray(bytearray(buffer.read()), dtype=np.uint8)
        img = cv2.imdecode(array, cv2.IMREAD_COLOR)
        grayimage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        try:
            faces = a3d._face_detect(grayimage)
            x = faces[0][0]
            y = faces[0][1]
            w = faces[0][2]
            h = faces[0][3]
            tmp = threading.Thread(target=gui().createwindows,args=(x,y,w,h))
            works.append(tmp)
            tmp.start()
        except:
            pass
        time.sleep(1)
main()