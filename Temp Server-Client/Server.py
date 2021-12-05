
import socket, cv2, pickle, struct, imutils

# Socket Create
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print('HOST IP:', host_ip)
port = 1234
socket_address = (host_ip, port)

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:", socket_address)

Dir_path = "./swarmlab-hybrid/scr-local/instance/poc-datacollector"
os.system("./tools/poc-dummy-create camera_1")
# Socket Accept
while True:
    client_socket, addr = server_socket.accept()
    print('GOT CONNECTION FROM:', addr)
    if client_socket:
        vid = cv2.VideoCapture(0)
        
        while (vid.isOpened()):
            img, frame = vid.read()

        # In this part the program will use the face_recognition.py
        # to recognice the faces that are in the cameraw view 
        # If a face is recogniced

            if face_id :
                # Writes the person that entered the door and the time/day
                os.system("./tools/poc-dummy-send [data]")
            else: # If the face is not recogniced then the camera video 
                # will be viewable for the client 
                frame = imutils.resize(frame, width=320)
                a = pickle.dumps(frame) #serialize frame to bytes
                message = struct.pack("Q", len(a)) + a # pack the serialized data
                # print(message)
                try:
                    client_socket.sendall(message) #send message or data frames to client
                except Exception as e:
                    print(e)
                    raise Exception(e)

                # This part will have the face recognition
                face_id = "ID"


                cv2.imshow('Camera view from the Server', frame) # will show video frame on server side.

                #key = cv2.waitKey(1) & 0xFF
                #if key == ord('q'):
                    #client_socket.close()
