import cv2
import os

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
img_counter = 0
users_ids = 0

path = "Captured_faces/Person2/"

if not os.path.exists(path):
    os.makedirs(path)
for user in os.listdir("Captured_faces/"):
    users_ids += 1

while True:
    check, frame = video.read()
    print ("check")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 10)
    print (type(face))

    for x,y,w,h in face:
        # img_name = "Captured_faces/Name{}.png".format(img_counter)
        img_name = path + "Person1" + "_" + str(users_ids) + "_" + str(img_counter) + ".png"
        captured_face = frame[y:y + h, x:x + w]
        gray_face = cv2.cvtColor(captured_face, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(img_name, gray_face)
        frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,255), 3)
        # cv2.imshow("img_name",frame)
        print("{} written!".format(img_name))
        img_counter += 1
    cv2.imshow("Video",frame)

    key = cv2.waitKey(1)

    if (key == ord('q')):
        break
video.release()
cv2.destroyAllWindows


