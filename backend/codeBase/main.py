import requests
from fastapi import FastAPI
from urllib.parse import urlencode
import os
from dotenv import load_dotenv 

load_dotenv()

clientID = os.getenv("SCHWAB_APP_KEY")
clientSecret = os.getenv("SCHWAB_APP_SECRET")
callbackURL = os.getenv("SCHWAB_CALLBACK_URL")
tokenURL = "https://api.schwabapi.com/v1/oauth/token"

authorizationURL = (
    "https://api.schwabapi.com/v1/oauth/authorize"
    f"?response_type=code"
    f"&client_id={clientID}"
    f"&scope=readonly"
    f"&redirect_uri={callbackURL}"
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