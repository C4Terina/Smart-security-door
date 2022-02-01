import numpy as np
import cv2
import os
import mediapipe as mp
from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions.drawing_utils import DrawingSpec
from PIL import Image


new_entry = str(input("Do you want a new person added(Y/N): ")).lower()
if(new_entry == 'y'):
    nameID = str(input("Enter Your Name: ")).lower()

    name_path = 'faces/'+nameID
    isExist = os.path.exists(name_path)
    if  isExist:
        while isExist:
            print("Name Already taken")
            nameID = str(input("Enter Again Your Name: ")).lower()
            name_path = 'faces/'+nameID
            isExist = os.path.exists(name_path)

    os.makedirs(name_path)
 
    
    cap = cv2.VideoCapture(0)
    color = (0, 255, 0) 
    stroke = 2

    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
    drawMeshSpecs = mpDraw.DrawingSpec(color=[0,255,0], thickness=1,circle_radius=1)


    img_counter=1
    not_done = True
    while (not_done):
        # Capture the frames
        ret, frame = cap.read()
        h, w, c = frame.shape
        # Convert the image to grayscale
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # Detect face
        results = faceMesh.process(frame)
        
        if results.multi_face_landmarks:
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
                captured_face = frame[y_min:y_max,x_min:x_max]
                img_name = name_path + "/{}.png".format(img_counter)
                cv2.imwrite(img_name,captured_face)
                
                cv2.rectangle(frame, (x_min,y_min),(x_max, y_max), color, stroke)
                if( img_counter == 1000):
                    not_done = False
                img_counter += 1
        
        # Display the frames
        cv2.imshow('frame', frame)

        # If the user presses 'q' end the while loop
        if cv2.waitKey(20) & 0xFF ==ord('q'):
            break

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()

cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

names = []
dictionary = {}
paths = []
faces = []
ids = []
trainer = cv2.face.LBPHFaceRecognizer_create() #pip install opencv-contrib-python
id = 1

for user in os.listdir("faces"):
    names.append(user)
    dictionary[user] = str(id)
    id += 1


for name in names:
    for image in os.listdir("faces/{}".format(name)):
        path_string = os.path.join("faces/{}/".format(name), image)
        paths.append(path_string)

for img_path in paths:
    
    image = Image.open(img_path).convert("L")
    
    imgNp = np.array(image,"uint8")
    faces.append(imgNp)
    usersName = str(img_path).split('/')[1]
    id = int(dictionary[usersName])
    ids.append(id)
    
ids = np.array(ids)

trainer.train(faces, ids)
trainer.write("accepted_faces.yml")
