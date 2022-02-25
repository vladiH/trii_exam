from fastapi import FastAPI, HTTPException
import requests
from fastapi.responses import StreamingResponse
import zipfile
import json
import uvicorn
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()
stocks = [
"AAPL",
"GOOGL",
"AMZN",
"TSLA",
"FB",
"TWTR",
"UBER",
"LYFT",
"SNAP",
"SHOP"]
url = "https://financialmodelingprep.com/api/v3/quote-short/"

def get_url(url):
    return requests.get(url, timeout=30)

def compose_url():
    return [ url+stock+"?apikey=c13a5d2ecf7cc6b8c50c06d7e1dfce22" for stock in stocks]

@app.get('/')
def read_root():
    return {"welcome": "Welcome to Trii app"}

@app.get('/money_necessary')
def character():
    with ThreadPoolExecutor(max_workers=2) as pool:
        response_list = list(pool.map(get_url,compose_url()))
    return {"money_necessary":sum(map(lambda x: x.json()[0]['price'], response_list))}
    