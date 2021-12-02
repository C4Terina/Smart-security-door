import cv2
import os
import mediapipe as mp

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Loaading the face recogniser and the trained data into the program
recognise = cv2.face.LBPHFaceRecognizer_create()
recognise.read("accepted_faces.yml")

labels = [] # dictionary
for user in os.listdir("Captured_faces"):
    labels.append(user)

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawMeshSpecs = mpDraw.DrawingSpec(color=[0,255,0], thickness=1,circle_radius=1)

while True:
    check, frame = video.read()
    # print ("check")
    h, w, c = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = faceMesh.process(rgb_frame)
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
            # print(f"Y min = {y_min} - Y max = {y_max} - X min = {y_max} - X max = {y_max}")
            if x_min >=0 and x_max >= 0 and y_min >= 0 and y_max >= 0:
                gray_face = cv2.cvtColor(frame[y_min:y_max,x_min:x_max], cv2.COLOR_BGR2GRAY)
                person_id, conf = recognise.predict(gray_face)
                print(person_id)
                if conf >= 4 and conf <= 85:
                    if person_id:
                        cv2.putText(frame, labels[int(person_id)-1], (x_max, y_min), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 1, cv2.LINE_AA)
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
