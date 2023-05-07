import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

class Spotipy_App():
    def __init__(self) -> None:
        client_id = os.getenv('CLIENT_ID')
        secret = os.getenv('CLIENT_SECRET')
        scope = 'user-read-currently-playing'

        creds = SpotifyOAuth(client_id=client_id, client_secret=secret, redirect_uri='https://www.google.com/', scope=scope, username='fre-sha-voca-do')
        self.sp = spotipy.Spotify(client_credentials_manager=creds)

    def get_current_song(self):
        return self.sp.current_user_playing_track()

