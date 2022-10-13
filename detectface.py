import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
CASC_PATH = 'haarcascade_frontalface_default.xml'


cascade_classifier = cv2.CascadeClassifier(CASC_PATH)
def face_detect(image):
    faces = cascade_classifier.detectMultiScale(
        image,
        scaleFactor=1.1,
        minNeighbors=5,
    )
    if not len(faces) > 0:
        print('no face')
        exit()
    else:
        return faces

def addimage(image,pos,size):
    pilimage = Image.open(image)
    antiimage = Image.open('antiface.jpg')
    antiimage = antiimage.resize((size[0]+20,size[1]+20))
    im = Image.new('RGB', (pilimage.size[0], pilimage.size[1]), (255, 255, 255, 0))
    im.paste(pilimage, (0, 0))
    im.paste(antiimage, (pos[0]-10, pos[1]-10))
    im.save('result.jpg')

def test(image):
    image = cv2.imread(image)
    grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detect(grayimage)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 0)
    cv2.imwrite("head.jpg", image)
    print(x,y)
    addimage("head.jpg", (x, y),(w,h))




test('20220916-112550_U1085_M793595_eb55.jpg')

