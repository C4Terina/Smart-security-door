import socket, pickle
import time
from datetime import datetime
from random import randint
from model import Data


HOST = 'localhost'
PORT = 50007
# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
temp = 0
this_camera_id = randint(0,5)
while True:
    # Create an instance of Data() to send to server.
    # data_to_send = Data(0, this_camera_id, randint(0,5), "Bob", datetime.now())
    data_to_send = Data(entry_id = 0, camera_id = this_camera_id, person_id = randint(0,5), person_name = "Bob", time_recognised = datetime.now())
    # data_to_send.entry_id = 0
    # data_to_send.camera_id = this_camera_id
    # data_to_send.person_id = randint(0,5)
    # data_to_send.person_name = "Bob"
    # data_to_send.time_recognised = datetime.now()
    # Pickle the object and send it to the server
    data_string = pickle.dumps(data_to_send)
    s.send(data_string)
    print("Data sended to the server")
    if temp >= 2:
        s.close()
        print("Connection closed")
    else:
        time.sleep(2)
        temp += 1
    
