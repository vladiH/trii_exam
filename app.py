from ast import Lambda
from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime
import zipfile
import json
import uvicorn
from io import BytesIO

app = FastAPI()

@app.get('/')
def read_root():
    return {"welcome": "Welcome to Trii app"}

@app.get('/character')
def character():
    url = 'https://rickandmortyapi.com/api/character/'
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()['results']
        return res
    else:
        return {"Data": "No data"}

@app.get('/character/{name}/{gender}/{species}')
def character(name:str, gender:str, species:str):
    url = 'https://rickandmortyapi.com/api/character/?name={0}&gender={1}&species={2}'.format(name, gender, species)
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()['results']
        return res
    else:
        return {"Data": "No data"}

@app.get("/character/zip")
def zip():
    url = 'https://rickandmortyapi.com/api/character/'
    response = requests.get(url)
    if response.status_code == 200:
        return zip_file("character.json", response.json())
    else:
        return {"Data": "No data"}

def zip_file(file_name, data):
    zipped_file = BytesIO()
    with zipfile.ZipFile(zipped_file, 'a', zipfile.ZIP_DEFLATED) as zipped:
        zipped.writestr(file_name, json.dumps(data))
    zipped_file.seek(0)
    response = StreamingResponse(zipped_file, media_type="application/x-zip-compressed")
    response.headers["Content-Disposition"] = "attachment; filename=test.zip"
    return response