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
        self.frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
        self.draw = ImageDraw.Draw(self.frame)
        self.font = ImageFont.load_default()
        




    def update_song(self,album_img_url, song_name, artist_name):
        self.frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
        img = self.update_image(album_img_url)
        self.frame.paste(img)
        self.draw.text((0,0), song_name,fill='white', font=self.font)
        self.draw.text((34,9), artist_name, )
        self.matrix.SetImage(self.frame)


    def update_image(self,url):
        #helper function
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((self.matrix.width, self.matrix.height), Image.ANTIALIAS)
        img.convert('RGB')
        return img