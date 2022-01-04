import socket, pickle
import threading
from datetime import datetime
from random import randint
from starlette.responses import Response
from pymongo import MongoClient

import sys
sys.path.insert(0, 'backend/')
from backend import model


PORT = 50007
client = MongoClient('mongodb://localhost:27017')

#create database with the name dataList
database = client.CamEntries

#create table with the name data
collection = database.CamData

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 4096
        while True:
            try:
                
                number_of_items = collection.count_documents({})

                payload = client.recv(size)
                if payload:
                    # Set the response to echo back the recieved data 
                    data_recieved = pickle.loads(payload)
                    data_recieved.entry_id = number_of_items + 1
                    print(data_recieved.entry_id)
                    print(data_recieved.camera_id)
                    print(data_recieved.person_id)
                    print(data_recieved.person_name)
                    print(data_recieved.time_recognised)
                    result = collection.insert_one({
                       "entry_id": data_recieved.entry_id,
                       "camera_id": data_recieved.camera_id,
                       "person_id": data_recieved.person_id,
                       "person_name": data_recieved.person_name,
                       "time_recognised": data_recieved.time_recognised
                    })
            except:
                client.close()
                return False

if __name__ == "__main__":
    ThreadedServer('',PORT).listen()
    