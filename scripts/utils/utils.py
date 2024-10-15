import sys
import logging
import requests
from dataclasses import dataclass
from functools import cached_property

logger = logging.getLogger(__name__)

#Setup logger
def set_logger() -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(levelname)s] %(name)s - %(asctime)s : %(message)s', \
                                  datefmt = "%Y-%m-%dT%H:%M:%S%z")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
    return

# Generic function to search through a list of dictionaries and return the dict with corresponding name
def inner_search(object,name):
    for obj in object:
        if obj["name"]==name:
            return obj

@dataclass
class SpotifyManager:
    client_id: str
    client_secret: str
    urls: dict

    @cached_property
    def _token_headers(self)->dict:
        return {
        "Content-Type": "application/x-www-form-urlencoded"
        }

    @cached_property
    def _token_payload(self)->dict:
        return {
        'grant_type': 'client_credentials',
        'client_id': self.client_id,
        'client_secret': self.client_secret
        }
    
    def __enter__(self):
        '''
        When we initiate a Spotify Manager client, retrieve an access token.
        
        '''
        logger.info("Instantiated a Spotify Manager Client.")
        logger.info("Retrieving access token")
        try:
            response = requests.post(
                url = self.urls['OAUTH_TOKEN_URL'],
                headers= self._token_headers,
                data=self._token_payload
            )
        except:
            logger.error("Post request failed.")

        if response.status_code != 200:
            logger.error(f"Failed to retrieve token with error code: {response.status_code}")
        else:
            token = response.json()['access_token']
            self.headers = {
                "Authorization":f"Bearer {token}"
            }
            logger.info("Retrieved token successfully.")
            return self

    def __exit__(self, type, value, traceback):
        logger.info("Closing Spotify Manager Client.")
        

    def user_profile(
            self, 
            user_id:str
            )->dict[str, any]:
        
        """
            Parameters
            ----------
            user_id : str
                id of the spotify user

            Returns
            -------
            dict [key: str, value: any]
        
        """
        user_url = f'https://api.spotify.com/v1/users/{user_id}'
        response = requests.get(
            url = user_url,
            headers= self.headers
        )
        user_json = response.json()
        user_profile = {
            "display_name":f"{user_json['display_name']}",
            "spotify_url":f"{user_json['external_urls']['spotify']}",
            "follower_count":f"{user_json['followers']['total']}"
        }
        logger.info(f"User {user_profile['display_name']} has \
                    {user_profile['follower_count']} number of followers.")
        return


@dataclass
class SpotifyPlaylistManager(SpotifyManager):
    user_id:str

    def get_user_public_playlist(self)->list:
        """
            Function to get a user's publicly available playlists

            Returns
            -------
            list
        """
        playlist_url = f'https://api.spotify.com/v1/users/{self.user_id}/playlists'
        response = requests.get(
        url = playlist_url,
        headers= self.headers
        )
        playlist_list = response.json()["items"]
        return playlist_list
    
    def get_playlist_details(
            self, 
            playlist_list:list, 
            playlist_name:str
            )->dict[str,any]:
        """
            Function to retrieve relevant details about the playlist

            Parameters
            ----------
            playlist_list : list
            playlist_name : str

            Returns
            -------
            dict [key: str, value: any]
        """
        playlist = inner_search(playlist_list, playlist_name)
        playlist_details = {
            "id": playlist["id"],
            "playlist_tracks_url": playlist["tracks"]['href'],
            'track_count': playlist["tracks"]["total"],
            "description": playlist["description"] if playlist["description"]!="" else "No description"
        }
        logger.info(f"Playlist {playlist_name} has {playlist_details['track_count']} tracks. Description of playlist: {playlist_details['description']}")
        return playlist_details
    
