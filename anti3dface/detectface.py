import os,io
import cv2
import numpy as np
from PIL import Image, ImageFilter, ImageDraw, ImageFont
fontpath = os.path.abspath(os.path.dirname(__file__))
CASC_PATH = f'{fontpath}\haarcascade_frontalface_default.xml'
font = ImageFont.truetype(f'{fontpath}/GenWanMin-L.ttc', 20)

cascade_classifier = cv2.CascadeClassifier(CASC_PATH)


class Anti3dface():


    def __init__(self,mode='vague',fimage = None,*args,**kwargs) -> None:
        self.mode = mode
        self.fimage = fimage
        self.text = kwargs.get('text','違反數位中介法')
        

    def _face_detect(self,image):
        faces = cascade_classifier.detectMultiScale(
            image,
            scaleFactor=1.1,
            minNeighbors=5,
        )
        if not len(faces) > 0:
            raise Exception('No faces found')
        else:
            return faces


    def _addvague(self,image, pos, size):
        pilimage = Image.fromarray(image)
        blurimage = pilimage.crop((pos[0], pos[1], pos[0]+size[0], pos[1]+size[1]))
        blurimage = blurimage.filter(ImageFilter.GaussianBlur(radius=10))
        im = Image.new(
            'RGB', (pilimage.size[0], pilimage.size[1]), (255, 255, 255, 0))
        im.paste(pilimage, (0, 0))
        im.paste(blurimage, (pos[0], pos[1]))
        imdraw = ImageDraw.Draw(im)
        text  = self.text
        w, _ = imdraw.textsize(text, font=font)
        imdraw.text((pos[0]+(size[0]-w)/2, pos[1]+size[1]/2),
                    text, fill=(255, 255, 255), font=font)
        return im

    def _addface(self,image, pos, size, fimage):
        pilimage = Image.fromarray(image)
        faceimage = Image.open(fimage)
        faceimage = faceimage.resize((size[0]+20, size[1]+20))
        im = Image.new(
            'RGBA', (pilimage.size[0], pilimage.size[1]), (255, 255, 255, 0))
        im.paste(pilimage, (0, 0))
        im.paste(faceimage, (pos[0]-10, pos[1]-10), faceimage)
        return im


    def detect_image(self,image):
        if isinstance(image, str):
            image = cv2.imread(image)
        else:
            image = np.fromstring(image, np.uint8)
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)


        grayimage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self._face_detect(grayimage)
        x = faces[0][0]
        y = faces[0][1]
        w = faces[0][2]
        h = faces[0][3]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if self.mode == 'vague':
            im = self._addvague(image, (x, y), (w, h))
        elif self.mode == 'image':
            im = self._addface(image, (x, y), (w, h),self.fimage)
        return im
