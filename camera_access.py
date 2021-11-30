import cv2

video = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
img_counter = 0
while True:
    check, frame = video.read()
    print ("check")

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    face = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 6)
    print (type(face))

    for x,y,w,h in face:
        img_name = "opencv_frame_{}.png".format(img_counter)
        captured_face = frame[y:y + h, x:x + w]
        cv2.imwrite(img_name, captured_face)
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


