import cv2
import numpy as np
from PIL import Image, ImageFilter , ImageDraw , ImageFont
CASC_PATH = 'haarcascade_frontalface_default.xml'
font = ImageFont.truetype('GenWanMin-L.ttc', 20)

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
    blurimage = pilimage.crop((pos[0],pos[1],pos[0]+size[0],pos[1]+size[1]))
    blurimage = blurimage.filter(ImageFilter.GaussianBlur(radius=10))
    im = Image.new('RGB', (pilimage.size[0], pilimage.size[1]), (255, 255, 255, 0))
    im.paste(pilimage, (0, 0))
    im.paste(blurimage, (pos[0], pos[1]))
    imdraw = ImageDraw.Draw(im)
    text = '此圖違反數位中介法'
    w, _ = imdraw.textsize(text, font=font)
    imdraw.text((pos[0]+(size[0]-w)/2, pos[1]+size[1]/2), text, fill=(255, 255, 255),font=font)
    im.save('result.jpg')


def test(image):
    image = cv2.imread(image)
    grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detect(grayimage)
    print(faces)
    x = faces[0][0]
    y = faces[0][1]
    w = faces[0][2]
    h = faces[0][3]
    # for (x, y, w, h) in faces:
    #     cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 0)
    cv2.imwrite("head.jpg", image)
    print(x,y)
    addimage("head.jpg", (x, y),(w,h))




test('166491955843109_P18818914.jpg')

