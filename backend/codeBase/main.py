import requests
from fastapi import FastAPI
import os
from dotenv import load_dotenv 

load_dotenv()

app_key = os.getenv("SCHWAB_APP_KEY")
app_secret = os.getenv("SCHWAB_APP_SECRET")

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}