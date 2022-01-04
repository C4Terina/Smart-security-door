from typing import Collection

from motor import docstrings
from model import Data 
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://localhost:27017')

#create database with the name dataList
database = client.CamEntries

#create table with the name data
collection = database.CamData

number_of_items = collection.count_documents({})


async def fetch_one_data(entry_id):
    document = await collection.find_one({"entry_id": int(entry_id)})
    return document

async def fecth_all_data():
    data = []
    cursor = collection.find({})
    
    async for document in cursor:
        data.append(Data(**document))
    return data


async def remove_data(entry_id):
    print("Delete was called")
    # print(f"Database file {entry_id}. Type {type(entry_id)}")
    await collection.delete_one({"entry_id":int(entry_id)})
    return True
