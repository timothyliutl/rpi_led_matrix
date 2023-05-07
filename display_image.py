import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from apps import spotify_app
import spotipy
import requests
from io import BytesIO

file_path = './images/seraphine.png'

image = Image.open(file_path)

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.brightness = 100
options.pwm_lsb_nanoseconds = 80
options.hardware_mapping = 'adafruit-hat'
options.limit_refresh_rate_hz = 150
options.drop_privileges = False

matrix = RGBMatrix(options = options)

image.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
spotify = spotify_app.Spotipy_App()


def update_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    matrix.SetImage(img.convert('RGB'))

def write_artist_name(artist_name):
    pass

def write_song_name(song_name):
    pass

#matrix.SetImage(image.convert('RGB'))
try:
    print("press ctrl-c to stop")
    while True:
        song_data = spotify.get_current_song()
        is_playing = song_data['is_playing']
        current_image_url = None

        if is_playing:
            image_url = song_data['item']['album']['images'][0]['url']
            name = song_data['item']['name']
            artist = song_data['item']['artists'][0]['name']

            if current_image_url != image_url:
                update_image(image_url)
                current_image_url = image_url

        time.sleep(2)
        


except KeyboardInterrupt:
    sys.exit(0)