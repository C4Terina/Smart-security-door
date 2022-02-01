import socket, pickle
import threading
from datetime import datetime
from random import randint
from starlette.responses import Response
from pymongo import MongoClient
from model import Data


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
        size = 5120
        while True:

            try:     

                payload = client.recv(size)
                number_of_items = collection.count_documents({})
                if payload:
                    data_recieved = pickle.loads(payload)
                    camera_id = data_recieved.split('/')[0]
                    person_id = data_recieved.split('/')[1]
                    person_name = data_recieved.split('/')[2]
                    time = data_recieved.split('/')[3]

                    entry_id = number_of_items + 1

                    result = collection.insert_one({
                       "entry_id": entry_id,
                       "camera_id": int(camera_id),
                       "person_id":  int(person_id),
                       "person_name":  person_name,
                       "time_recognised": time
                    })
            except:
                client.close()
                return False

if __name__ == "__main__":
    ThreadedServer('',PORT).listen()
    