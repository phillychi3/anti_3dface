import cv2
import threading
import numpy as np
from PIL import Image, ImageFilter , ImageDraw , ImageFont
CASC_PATH = 'haarcascade_frontalface_default.xml'
font = ImageFont.truetype('GenWanMin-L.ttc', 20)
from detectface import test2


class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False
		
	#攝影機連接。
        self.video_capture =cv2.VideoCapture(0, cv2.CAP_DSHOW)
        #self.video_capture = cv2.VideoCapture(URL)
    def start(self):
	#把程式放進子執行緒
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
	#停止無限迴圈的開關。
        self.isstop = True
        print('ipcam stopped!')
   
    def getframe(self):
	#再回傳最新的影像。
        return self.Frame
        
    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.video_capture.read()
        
        self.video_capture.release()





ipcam = ipcamCapture(0)
ipcam.start()


while True:
    frame = ipcam.getframe()
    frame = test2(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        ipcam.stop()
        cv2.destroyAllWindows()
        break
    cv2.imshow('Video', frame)