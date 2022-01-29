import cv2
import os
import mediapipe as mp
import time
import serial
import time
from datetime import datetime
from random import randint
from pymongo import MongoClient
from backend.database import add_data
from backend.model import Data
                                           

client = MongoClient('mongodb://localhost:27017')

#create database with the name dataList
database = client.CamEntries

#create table with the name data
collection = database.CamData

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Loaading the face recogniser and the trained data into the program
recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read("accepted_faces.yml")

labels = [] # dictionary
for user in os.listdir("faces"):
    labels.append(user)

print(labels)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawMeshSpecs = mpDraw.DrawingSpec(color=[0,255,0], thickness=1,circle_radius=1)

commPort = 'COM3'
ser = serial.Serial(commPort, baudrate = 9600, timeout = 1)
flag = True

while True:
    
    check, frame = video.read()
    h, w, c = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(rgb_frame)
    if results.multi_face_landmarks:
        if flag:
            start_timer = time.time()
        for faceLms in results.multi_face_landmarks:
            
            x_max = 0
            y_max = 0
            x_min = w
            y_min = h
            
            for id,lm in enumerate(faceLms.landmark):
                
                x, y = int(lm.x*w), int(lm.y*h)
                if x > x_max:
                    x_max = x
                if x < x_min:
                    x_min = x
                if y > y_max:
                    y_max = y
                if y < y_min:
                    y_min = y
            if x_min >=0 and x_max >= 0 and y_min >= 0 and y_max >= 0:
                gray_face = cv2.cvtColor(frame[y_min:y_max,x_min:x_max], cv2.COLOR_BGR2GRAY)
                id_, conf = recognise.predict(gray_face)
                if conf >= 4 and conf<= 85 :
                    if id_ and labels[int(id_)-1] != 'random_person':
                        if flag:
                            ser.write(b'o')
                            time.sleep(3)
                            flag = False
                            data_to_send = Data(entry_id = 0, camera_id = 1, person_id = id_, person_name = labels[int(id_)-1], time_recognised = datetime.now())
                            result = collection.insert_one({
                                "entry_id": data_to_send.entry_id,
                                "camera_id": data_to_send.camera_id,
                                "person_id": data_to_send.person_id,
                                "person_name": data_to_send.person_name,
                                "time_recognised": data_to_send.time_recognised})

                        timerecognised = time.time()
                        elsapsed_time = timerecognised - start_timer
                        if elsapsed_time > 10:
                            flag = True
                        cv2.putText(frame, labels[int(id_)-1], (x_max, y_min), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    else:
                        cv2.putText(frame, "Not recognised", (x_max, y_min), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)      
                else:
                    cv2.putText(frame, "Not recognised", (x_max, y_min), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
                    
                cv2.rectangle(frame, (x_min,y_min) ,(x_max,y_max), (0,255,0), 3)
    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)

    if (key == ord('q')):
        break

video.release()
cv2.destroyAllWindows()
