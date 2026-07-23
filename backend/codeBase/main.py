import requests
from fastapi import FastAPI
from urllib.parse import urlencode
import os
from dotenv import load_dotenv 
from pathlib import Path

env_path = Path(__file__).resolve().parent.parent.parent / ".env"

load_dotenv(dotenv_path = env_path)

clientID = os.getenv("SCHWAB_APP_KEY")
clientSecret = os.getenv("SCHWAB_APP_SECRET")
callbackURL = os.getenv("SCHWAB_CALLBACK_URL")
tokenURL = "https://api.schwabapi.com/v1/oauth/token"
SCHWAB_API_BASE = "https://api.schwabapi.com/marketdata/v1"
accesstoken = os.getenv("SCHWAB_ACCESS_TOKEN")

params = {
    "response_type": "code",
    "client_id": clientID,
    "redirect_uri": callbackURL
}

authorizationURL = (
    "https://api.schwabapi.com/v1/oauth/authorize?"
    + urlencode(params)
)

def get_tokens(auth_code):

    response = requests.post(
        tokenURL,
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": callbackURL
        },
        auth=(
            clientID,
            clientSecret
        )
    )

    return response.json()

def get_schwab_quote(symbol, access_token):

    url = f"{SCHWAB_API_BASE}/quotes"

    params = {
        "symbols": symbol
    }

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(
        url,
        headers=headers,
        params=params
    )

    response.raise_for_status()

    return response.json()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/auth/login")
def login():
    return {
        "authorization_url": authorizationURL
    }

@app.get("/callback")
def callback(code: str):

    tokens = get_tokens(code)

    return tokens

@app.get("/stock/{symbol}")
def stock(symbol: str):

    access_token = accesstoken
    print("ACCESS TOKEN:", access_token)

    data = get_schwab_quote(
        symbol,
        access_token
    )

    return data