import os
import cv2
import numpy as np
import win32gui
import win32ui
from ctypes import windll
from PIL import Image
fontpath = os.path.abspath(os.path.dirname(__file__))
CASC_PATH = f'{fontpath}\haarcascade_frontalface_default.xml'

cascade_classifier = cv2.CascadeClassifier(CASC_PATH)

def getdc():

    windows = win32gui.GetWindowText(win32gui.GetForegroundWindow())
    hwnd = win32gui.FindWindow(None, windows)

    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bot - top

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)


    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    if result == 1:
        #return buffer
        return cv2.imencode('.png', np.array(im))[1].tostring()
    else:
        return None

def _face_detect(image):
    faces = cascade_classifier.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
    )
    if not len(faces) > 0:
        raise Exception('No faces found')
    else:
        return faces


def detect_image():
    image = getdc()
    if image is None:
        print([])
        return
    if isinstance(image, str):
        image = cv2.imread(image)
    else:
        image = np.fromstring(image, np.uint8)
        image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = _face_detect(grayimage)
    faceslist = []
    for (x, y, w, h) in faces:
        faceslist.append((x,y,w,h))
    print(faceslist)

if __name__ == '__main__':
    detect_image()
