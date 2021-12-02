import cv2
import os
import mediapipe as mp
from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions.drawing_utils import DrawingSpec

video = cv2.VideoCapture(0)
# cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
img_counter = 1
users_ids = 1

mpDraw = mp.solutions.drawing_utils
mpFaceMesh = mp.solutions.face_mesh
faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)
drawMeshSpecs = mpDraw.DrawingSpec(color=[0,255,0], thickness=1,circle_radius=1)

path = "Captured_faces/Person1/"

if not os.path.exists(path):
    os.makedirs(path)
for user in os.listdir("Captured_faces/"):
    users_ids += 1

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
            captured_face = frame[y_min:y_max,x_min:x_max]
            gray_face = cv2.cvtColor(captured_face, cv2.COLOR_BGR2GRAY)
            img_name = path + "Person" + "_" + str(users_ids) + "_" + str(img_counter) + ".png"
            cv2.imwrite(img_name, gray_face)
            if( img_counter == 500):
                break
            img_counter += 1
            mpDraw.draw_landmarks(frame, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawMeshSpecs, drawMeshSpecs)

    cv2.imshow("Video",frame)

    key = cv2.waitKey(1)

    if (key == ord('q')):
        break
video.release()
cv2.destroyAllWindows


