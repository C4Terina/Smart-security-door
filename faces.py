from matplotlib.style import use
import numpy as np
import cv2
import os
import pickle
import mediapipe as mp
from mediapipe.python.solutions import face_mesh
from mediapipe.python.solutions.drawing_utils import DrawingSpec
import tensorflow as tf
from sklearn.model_selection import train_test_split
from keras import layers,callbacks,utils,applications,optimizers
from keras.models import Sequential,Model,load_model
from PIL import Image

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

new_entry = str(input("Do you want a new person added(Y/N): ")).lower()
if(new_entry == 'y'):
    nameID = str(input("Enter Your Name: ")).lower()

    name_path = 'faces/save'+nameID
    isExist = os.path.exists(name_path)
    if  isExist:
        while isExist:
            print("Name Already taken")
            nameID = str(input("Enter Again Your Name: ")).lower()
            name_path = 'faces/save'+nameID
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
        # faces = face_cascade.detectMultiScale(gray,scaleFactor=2, minNeighbors=2)
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

recognizer = cv2.face.LBPHFaceRecognizer_create()

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

# for img_path in paths:
#     usersName = str(img_path).split('/')[1]
#     # print(usersName)
#     print()
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

# current_id = 0
# # label_ids = {}
# label_array=[]
# image_array=[]
# x_train = []
# y_labels = []
# label_counter = 0
# path = "faces/"
# files=os.listdir("faces/")
# print(files)
# for i in range(len(files)):
#     # files in sub-folder
#     file_sub=os.listdir(path+files[i])
#     for j in range(len(file_sub)):
#         img=cv2.imread(path+files[i]+"/"+file_sub[j])
#         img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
#         img=cv2.resize(img,(96,96))
#         image_array.append(img)
#         label_array.append(i)


# image_array=np.array(image_array)/255.0
# label_array=np.array(label_array)
            
# X_train,X_test,Y_train,Y_test=train_test_split(image_array,label_array,test_size=0.15)
# len(files)
# model=Sequential()
# # I will use MobileNetV2 as an pretrained model 
# pretrained_model=tf.keras.applications.EfficientNetB0(input_shape=(96,96,3),include_top=False,
#                                          weights="imagenet")
# model.add(pretrained_model)
# model.add(layers.GlobalAveragePooling2D())
# # add dropout to increase accuracy by not overfitting
# model.add(layers.Dropout(0.3))
# # add dense layer as final output
# model.add(layers.Dense(1))
# model.summary()
# model.compile(optimizer="adam",loss="mean_squared_error",metrics=["mae"])

# ckp_path="trained_model/model"
# model_checkpoint=tf.keras.callbacks.ModelCheckpoint(filepath=ckp_path,
#                                                    monitor="val_mae",
#                                                    mode="auto",
#                                                    save_best_only=True,
#                                                    save_weights_only=True)

# # create a lr reducer which decrease learning rate when accuarcy does not increase
# reduce_lr=tf.keras.callbacks.ReduceLROnPlateau(factor=0.9,monitor="val_mae",
#                                              mode="auto",cooldown=0,
#                                              patience=5,verbose=1,min_lr=1e-6)
# # patience : wait till 5 epoch
# # verbose : show accuracy every 1 epoch
# # min_lr=minimum learning rate
# #

# EPOCHS=300
# BATCH_SIZE=64

# history=model.fit(X_train,
#                  Y_train,
#                  validation_data=(X_test,Y_test),
#                  batch_size=BATCH_SIZE,
#                  epochs=EPOCHS,
#                  callbacks=[model_checkpoint,reduce_lr]
#                  )

# model.load_weights(ckp_path)
# model.save("model")
# for root, dirs, files, in os.walk(image_dir):
#     for file in files:
#         if file.endswith(".png") or file.endswith(".jpg"):
#             path = os.path.join(root, file)
#             label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()

#             if not label in label_ids:
#                 label_ids[label] = current_id
#                 current_id += 1
#             id_ = label_ids[label]
        
#             pil_image = Image.open(path).convert('L')
#             image_array =  np.array(pil_image, "uint8")
#             faces = face_cascade.detectMultiScale(image_array,scaleFactor=2, minNeighbors=2)

#             for (x,y,w,h) in faces:
#                 roi = image_array[y:y+h, x:x+w]
#                 x_train.append(roi)
#                 y_labels.append(id_)

# with open("labels.pickle", "wb") as f:
#     pickle.dump(label_ids, f)

# recognizer.train(x_train, np.array(y_labels))
# recognizer.save("trainner.yml")




