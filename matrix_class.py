import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont
from apps import spotify_app
import spotipy
import requests
from io import BytesIO

class MatrixClass():
    def __init__(self) -> None:

        self.options = RGBMatrixOptions()
        self.options.rows = 32
        self.options.cols = 64
        self.options.chain_length = 1
        self.options.parallel = 1
        self.options.brightness = 100
        self.options.pwm_lsb_nanoseconds = 80
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.limit_refresh_rate_hz = 150
        self.options.drop_privileges = False
        self.options.gpio_slowdown=4
        self.matrix = RGBMatrix(options = self.options)
        self.font = ImageFont.truetype('fonts/tiny.otf', size=6)
        




    def update_song(self,album_img_url, song_name, artist_name):
        frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
        img = self.update_image(album_img_url)
        draw = ImageDraw.Draw(frame)
        draw.text((34,0), song_name,fill='white', font=self.font)
        draw.text((34,9), artist_name,fill='white', font = self.font)
        frame.paste(img)
        self.matrix.SetImage(frame)


    def update_image(self,url):
        #helper function
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((32, 32), Image.ANTIALIAS)
        img.convert('RGB')
        return img