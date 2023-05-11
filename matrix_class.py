import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from PIL import Image, ImageDraw, ImageFont
from apps import spotify_app
import spotipy
import requests
from io import BytesIO
from multiprocess import Process


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
        self.font = ImageFont.truetype('fonts/tiny.otf', size=5)

        self.album_img_url = None
        self.song_name = None
        self.artist_name = None
        self.animation_count_artist = 0
        self.animation_count_song=0
        
        process = Process(target=self.update_display)
        process.start()



    def update_song(self,album_img_url, song_name, artist_name):
        self.album_img_url = album_img_url
        self.artist_name = artist_name
        self.song_name = song_name

    def update_display(self):

        if self.album_img_url==None or self.song_name == None or self.artist_name == None:
            pass 
        else:
            spacer = "   "
            frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
            frame_text = Image.new("RGB", (32, 32), (0,0,0))
            img = self.update_image(self.album_img_url)
            draw = ImageDraw.Draw(frame_text)
            
            if len(self.song_name)>7:
                draw.text((-self.animation_count_song,0), self.song_name + spacer + self.song_name,fill='white', font=self.font)
            else:
                draw.text((0,0), self.song_name,fill='white', font=self.font)
                
            if len(self.artist_name)>7:
                draw.text((-self.animation_count_artist,9), self.artist_name + spacer + self.song_name,fill='white', font = self.font)
            else:
                draw.text((0,9), self.artist_name,fill='white', font = self.font)

            frame.paste(img)
            frame.paste(frame_text,(34,0))

            if (self.animation_count_artist) == self.font.getsize(self.artist_name + spacer)[0]:
                self.animation_count_artist = 0
            else:
                self.animation_count_artist += 1

            if (self.animation_count_song) == self.font.getsize(self.song_name + spacer)[0]:
                self.animation_count_song = 0
            else:
                self.animation_count_song += 1
            

            self.matrix.SetImage(frame)
        


    def update_image(self,url):
        #helper function
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((32, 32), Image.ANTIALIAS)
        img.convert('RGB')
        return img