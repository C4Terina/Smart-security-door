# import the required libraries
import cv2
import os
import numpy as np
from PIL import Image
import pickle


cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

names = []
paths = []
faces = []
ids = []

trainer = cv2.face.LBPHFaceRecognizer_create() #pip install opencv-contrib-python

for user in os.listdir("Captured_faces"):
    names.append(user)

for name in names:
    for image in os.listdir("Captured_faces/{}".format(name)):
        path_string = os.path.join("Captured_faces/{}/".format(name), image)
        paths.append(path_string)
print(paths)
for img_path in paths:
    
    image = Image.open(img_path).convert("L")
    
    imgNp = np.array(image,"uint8")
    faces.append(imgNp)
    id = int(img_path.split("/")[2].split("_")[1])
    ids.append(id)
    
ids = np.array(ids)

trainer.train(faces, ids)
trainer.write("accepted_faces.yml")
