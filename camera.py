import cv2
import threading
import numpy as np
from PIL import Image, ImageFilter , ImageDraw , ImageFont
import time
CASC_PATH = 'haarcascade_frontalface_default.xml'
font = ImageFont.truetype('GenWanMin-L.ttc', 20)

cv2.useOptimized()
video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)

cascade_classifier = cv2.CascadeClassifier(CASC_PATH)
def face_detect(image):
    faces = cascade_classifier.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
    )
    if not len(faces) > 0:
        return None
    else:
        return faces


def detect():
    while True:
        if not video_capture.isOpened():
            print('找不到相機')
            pass
        ret, frame = video_capture.read()
        grayimage = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detect(grayimage)
        if faces is not None:
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 0)
                pliimage = Image.fromarray(frame)
                blurimage = pliimage.crop((x,y,x+w,y+h))
                blurimage = blurimage.filter(ImageFilter.GaussianBlur(radius=10))
                im = Image.new('RGB', (pliimage.size[0], pliimage.size[1]), (255, 255, 255, 0))
                im.paste(pliimage, (0, 0))
                im.paste(blurimage, (x, y))
                imdraw = ImageDraw.Draw(im)
                text = '此圖違反數位中介法'
                w, _ = imdraw.textsize(text, font=font)
                imdraw.text((x+(w-w)/2, y+h/2), text, fill=(255, 255, 255),font=font)
                feame = np.array(im)
                

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        cv2.imshow('Video', frame)








if __name__ == '__main__':
    detect()
    video_capture.release()
    cv2.destroyAllWindows()