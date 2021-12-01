# import the required libraries
import cv2
import pickle
import os

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Loaading the face recogniser and the trained data into the program
recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read("accepted_faces.yml")

labels = [] # dictionary
for user in os.listdir("Captured_faces"):
    labels.append(user)


while True:
    check,frame = video.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(gray, scaleFactor = 1.2, minNeighbors = 5)
    #print(face)

    for x,y,w,h in face:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,255), 3)
        id, conf = recognise.predict(gray[y:y+h, x:x+w])
        print (id)
        
        if id:
            if conf >= 4 and conf <= 85:
                cv2.putText(frame, labels[int(id)-1], (x, y-4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
            else:
                cv2.putText(frame, "Not recognised", (x, y-4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
        else:
            cv2.putText(frame, "Not recognised", (x, y-4), cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 0.8, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)

    if (key == ord('q')):
        break

video.release()
cv2.destroyAllWindows()
