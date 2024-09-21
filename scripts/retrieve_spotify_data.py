import json
import requests
from utils import utils
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values

#Set up config and credentials
scope = "user-library-read, user-top-read"

url_file_name = "config/urls.json"
with open(url_file_name) as f:
    urls = json.load(f)

# BASE_URL = 'https://api.spotify.com/v1'
# AUTH_URL = 'https://accounts.spotify.com/authorize'
# OAUTH_TOKEN_URL = 'https://accounts.spotify.com/api/token'

BASE_URL = urls['BASE_URL']
AUTH_URL = urls['AUTH_URL']
OAUTH_TOKEN_URL = urls['OAUTH_TOKEN_URL']
REDIRECT_URL = urls['REDIRECT_URL']

#Get credentials from env
client_id = dotenv_values("credentials/spotify-cred.env")['client-id']
client_secret = dotenv_values("credentials/spotify-cred.env")['client-secret']
# redirect_url = "http://localhost:8080/callback"

#Prepare header and payload to get access token
token_headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

token_payload = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}

#Post request to get Access token
response = requests.post(
    url = OAUTH_TOKEN_URL,
    headers= token_headers,
    data=token_payload
)

token = response.json()['access_token']

#The Weeknd
artist_id = "1Xyo4u8uXC1ZmMpatF05PJ"
artist_url = BASE_URL + "/artists/" + artist_id

#Prepare header to get artist
headers = {
    "Authorization":f"Bearer {token}"
}

response = requests.get(
    url=artist_url,
    headers=headers
)

print(json.dumps(response.json()))