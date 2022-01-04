from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from database import (
    fetch_one_data,
    fecth_all_data,
    remove_data,
)
from model import Data
import os

app = FastAPI()
origins = ['http://localhost:3000/data', 'http://localhost:8000/data']

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

#get data 
@app.get("/data")
async def get_data():
    responce = await fecth_all_data()
    return responce

#get data with id
@app.get("/data/{entry_id}", response_model=Data)
async def get_data_by_id(entry_id):
    responce = await fetch_one_data(entry_id)
    print(f"the entry id is {entry_id}")
    if responce:
        return responce
    raise HTTPException(404, f"There is no entry with the id {entry_id}")

#delete data
@app.delete("/data/{entry_id}")
async def delete_data(entry_id):
    responce = await remove_data(entry_id)
    if responce:
        return "Succesfully deleted data item !"
    raise HTTPException(404, f"There is no entry with the id {entry_id}")
