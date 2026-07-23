import requests
from fastapi import FastAPI
from urllib.parse import urlencode
import os
from dotenv import load_dotenv 

load_dotenv()

appKey = os.getenv("SCHWAB_APP_KEY")
appSecret = os.getenv("SCHWAB_APP_SECRET")
callbackUrl = os.getenv("SCHWAB_CALLBACK_URL")
authorizationURL= "https://api.schwabapi.com/v1/oauth/authorize?response_type=code&client_id=fnB6k1X6JSFlQHravRt6T9m86AZlkD04&scope=readonly&redirect_uri=https://developer.schwab.com/oauth2-redirect.html"
tokenURL = "https://api.schwabapi.com/v1/oauth/token"

def create_authorization_url():
    params = {
        "client_id": appKey,
        "redirect_url": callbackUrl,
        "response_type": "code"
    }

    return f"{authorizationURL}?{urlencode(params)}"

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}