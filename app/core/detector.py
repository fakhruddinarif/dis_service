from io import BytesIO
from PIL import Image
from fastapi import UploadFile
from mtcnn import MTCNN
import numpy as np

class FaceDetector:
    def __init__(self):
        self.detector = MTCNN()

    def read_image(self, image: UploadFile):
        image = Image.open(BytesIO(image.file.read()))
        image = image.convert("RGB")
        return np.array(image)

    def detect_faces(self, image: UploadFile):
        image = self.read_image(image)
        detections = self.detector.detect_faces(image)
        faces = []
        for detection in detections:
            x, y, width, height = detection["box"]
            x, y = max(x, 0), max(y, 0)
            face = image[y:y + height, x:x + width]
            faces.append((face, (x, y, width, height)))
        return faces

face_detector = FaceDetector()