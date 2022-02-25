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

posts = []

# Post model
class Post(BaseModel):
    id: Optional[str]
    title: str
    author: str
    content: Text
    created_at: datetime =  datetime.now()
    published_at: Optional[datetime] 
    published: Optional[bool] = False

@app.get('/')
def read_root():
    return {"welcome": "Welcome to Trii app"}

@app.get('/character/{filter}')
def character(filter:str):
    url = 'https://rickandmortyapi.com/api/character/'
    response = requests.get(url)
    if response.status_code == 200:
        res = response.json()['results']
        if filter=='all':
            return res
        if filter=='male':
            return json.dump(list(filter(lambda x:x['gender']=='male'),res))
        else:
            return res

    else:
        return {"Data": "No data"}

@app.get("/zip")
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