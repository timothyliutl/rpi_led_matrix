import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
from apps import spotify_app
import spotipy

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

matrix.SetImage(image.convert('RGB'))
try:
    print("press ctrl-c to stop")
    while True:
        #print(spotify.get_current_song())
        print('hello world')
        time.sleep(1000)


except KeyboardInterrupt:
    sys.exit(0)