import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyClientCredentials

scope = "user-library-read"

#Set up config and credentials
#Get credentials from env
client_id = dotenv_values("credentials/spotify-cred.env")['client-id']
client_secret = dotenv_values("credentials/spotify-cred.env")['client-secret']

client_cred_manager = SpotifyClientCredentials(
    client_id=client_id,
    client_secret=client_secret
    )

#Initialize spotify client
sp = spotipy.Spotify(
    client_credentials_manager=client_cred_manager
)

weeknd_artist_id = "1Xyo4u8uXC1ZmMpatF05PJ"
artist_uri_prefix = "spotify:artist:"
full_uri = artist_uri_prefix + weeknd_artist_id
results = sp.artist_albums(full_uri,album_type="album")
albums = results['items']
while results['next']:
    results = sp.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])