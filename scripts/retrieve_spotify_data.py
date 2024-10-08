import json
import base64
import requests
import logging
from utils import utils
from requests.auth import HTTPBasicAuth
from dotenv import dotenv_values
from pyspark.sql import SparkSession, Row

### Set up config and credentials ###
logger = logging.getLogger(__name__)
# scope = "user-library-read, user-top-read"
utils.set_logger()

#URLs
url_file_name = "config/urls.json"
with open(url_file_name) as f:
    urls = json.load(f)

#Configs
config_file_name = "config/config.json"
with open(config_file_name) as cf:
    config = json.load(cf)

BASE_URL = urls['BASE_URL']
AUTH_URL = urls['AUTH_URL']
OAUTH_TOKEN_URL = urls['OAUTH_TOKEN_URL']
REDIRECT_URL = urls['REDIRECT_URL']

#Get credentials from env
client_id = dotenv_values("credentials/spotify-cred.env")['client-id']
client_secret = dotenv_values("credentials/spotify-cred.env")['client-secret']

user_id = config["user_id"]
playlist_name = "Top 50 - Singapore"


### START ###

#Init SparkSession
spark = SparkSession \
        .builder \
        .appName("Spotify-project") \
        .getOrCreate()

# #The Weeknd
# artist_id = "1Xyo4u8uXC1ZmMpatF05PJ"

def main():

    #Spotify manager to perform API calls
    playlist_manager = utils.SpotifyPlaylistManager(client_id,client_secret,urls,user_id)
    with playlist_manager as pm:

        #Get list of playlist names
        playlist_list = pm.get_user_public_playlist()
        
        #Get playlist details based on playlist name
        playlist_details = pm.get_playlist_details(playlist_list, playlist_name)

        track_count = playlist_details["track_count"]
        playlist_id = playlist_details["id"]
        playlist_tracks_url = playlist_details["playlist_tracks_url"]
        
        # playlist_items_url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
        response = requests.get(
            url = playlist_tracks_url,
            headers= pm.headers
        )
        tracks = response.json()["items"]
        track_row_list = []

        for track in tracks:
            # track = tracks[0]
            album_artists = track['track']['album']['artists']
            if len(album_artists)==1:
                artist_name = album_artists[0]['name']
                artist_id = album_artists[0]['id']
            else:
                artist_name = ['']*len(album_artists)
                artist_id = ['']*len(album_artists)
                for artist_no in range(len(album_artists)):
                    artist_name[artist_no] = album_artists[artist_no]['name']
                    artist_id[artist_no] = album_artists[artist_no]['id']
                artist_name = str(artist_name)
                artist_id = str(artist_id)

            track_row = Row(
            added_at = track['added_at'],
            is_local = track['track']['is_local'],
            explicit = track["track"]['explicit'],
            album_id = track['track']['album']['id'],
            album_name = track['track']['album']['name'],
            album_release_date = track['track']['album']['release_date'],
            artist_name = artist_name,
            artist_id = artist_id,
            track_duration = track['track']['duration_ms'],
            track_name = track['track']['name'],
            track_popularity = track['track']['popularity'],
            )
            track_row_list.append(track_row)
        df = spark.createDataFrame(track_row_list)
        # df.show()

if __name__ == "__main__":
    main()