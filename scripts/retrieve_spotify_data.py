import json
import base64
import requests
import logging
from utils import utils
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values

#Set up config and credentials
logger = logging.getLogger(__name__)
# scope = "user-library-read, user-top-read"
utils.set_logger()

url_file_name = "config/urls.json"
with open(url_file_name) as f:
    urls = json.load(f)

BASE_URL = urls['BASE_URL']
AUTH_URL = urls['AUTH_URL']
OAUTH_TOKEN_URL = urls['OAUTH_TOKEN_URL']
REDIRECT_URL = urls['REDIRECT_URL']

#Get credentials from env
client_id = dotenv_values("credentials/spotify-cred.env")['client-id']
client_secret = dotenv_values("credentials/spotify-cred.env")['client-secret']

user_id = "nictomeetu"
playlist_name = "Top 50 - Singapore"
# playlist_name = "Family playlist"
# #The Weeknd
# artist_id = "1Xyo4u8uXC1ZmMpatF05PJ"

#Spotify manager to perform API calls
playlist_manager = utils.SpotifyPlaylistManager(client_id,client_secret,urls,user_id)
with playlist_manager as pm:

    playlist_list = pm.get_user_public_playlist()
    # print(playlist_list[0].keys())
    print(pm.get_playlist_details(playlist_list, playlist_name))
    # #Test playlist
    # test_playlist = playlist_list[1]
    # playlist_id = test_playlist['id']
    # playlist_items_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    # response = requests.get(
    #     url = playlist_items_url,
    #     headers= sm.headers
    # )

    # album_url = response.json()['items'][0]['track']["href"]
    # track_name = response.json()['items'][0]['track']["name"]
    # artist_id = response.json()['items'][0]['track']["artists"]