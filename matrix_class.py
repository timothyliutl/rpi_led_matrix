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
        self.image_data = None

        self.crunchyroll_data = {
            "show_name": None,
            "image_url": None,
            "timestamps": None,
            "episode_name": None,
            "season_episode": None
        }



    def update_song(self,album_img_url, song_name, artist_name):
        self.album_img_url = album_img_url
        self.artist_name = artist_name
        self.song_name = song_name
        self.animation_count_artist = 0
        self.animation_count_song = 0
        self.image_data = self.update_image(album_img_url)

    def update_crunchyroll(self,data):
        self.crunchyroll_data = data
        self.crunchyroll_data['img'] = self.update_image(data['image_url'])
        

    def update_crunchyroll_display(self):

        if self.crunchyroll_data['image_url']==None or self.crunchyroll_data['show_name'] == None or self.crunchyroll_data['season_episode'] == None:
            pass 
        else:
            spacer = "   "
            frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
            frame_text = Image.new("RGB", (40, 32), (0,0,0))
            img = self.crunchyroll_data['img']
            draw = ImageDraw.Draw(frame_text)

            show_name = self.crunchyroll_data['show_name']
            season_episode = self.crunchyroll_data['season_episode']
            
            if len(show_name)>7:
                draw.text((-self.animation_count_song,0), show_name + spacer + show_name,fill='white', font=self.font)
            else:
                draw.text((0,0), show_name,fill='white', font=self.font)
                
            if len(season_episode)>7:
                draw.text((-self.animation_count_artist,9), season_episode + spacer + season_episode,fill='white', font = self.font)
            else:
                draw.text((0,9), season_episode,fill='white', font = self.font)

            frame.paste(img)
            frame.paste(frame_text,(26,0))

            if (self.animation_count_artist) == self.font.getsize(season_episode + spacer)[0]:
                self.animation_count_artist = 0
            elif self.animation_count_artist == 0 and abs(self.animation_count_song - self.animation_count_artist) > 2:
                self.animation_count_artist = 0
            else:
                self.animation_count_artist += 1

            if (self.animation_count_song) == self.font.getsize(show_name + spacer)[0]:
                self.animation_count_song = 0
            elif self.animation_count_song == 0 and abs(self.animation_count_song - self.animation_count_artist) > 2:
                self.animation_count_song = 0
            else:
                self.animation_count_song += 1
            self.matrix.SetImage(frame)

    #TODO: make this code more modular

    def update_spotify_display(self):

        if self.album_img_url==None or self.song_name == None or self.artist_name == None or self.image_data == None:
            pass 
        else:
            spacer = "   "
            frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
            frame_text = Image.new("RGB", (32, 32), (0,0,0))
            img = self.image_data
            draw = ImageDraw.Draw(frame_text)
            
            if len(self.song_name)>7:
                draw.text((-self.animation_count_song,0), self.song_name + spacer + self.song_name,fill='white', font=self.font)
            else:
                draw.text((0,0), self.song_name,fill='white', font=self.font)
                
            if len(self.artist_name)>7:
                draw.text((-self.animation_count_artist,9), self.artist_name + spacer + self.artist_name,fill='white', font = self.font)
            else:
                draw.text((0,9), self.artist_name,fill='white', font = self.font)

            frame.paste(img)
            frame.paste(frame_text,(34,0))

            if (self.animation_count_artist) == self.font.getsize(self.artist_name + spacer)[0]:
                self.animation_count_artist = 0
            elif self.animation_count_artist == 0 and abs(self.animation_count_song - self.animation_count_artist) > 2:
                self.animation_count_artist = 0
            else:
                self.animation_count_artist += 1

            if (self.animation_count_song) == self.font.getsize(self.song_name + spacer)[0]:
                self.animation_count_song = 0
            elif self.animation_count_song == 0 and abs(self.animation_count_song - self.animation_count_artist) > 2:
                self.animation_count_song = 0
            else:
                self.animation_count_song += 1
            

            self.matrix.SetImage(frame)

        
    def turn_off_display(self):
        blank_frame = Image.new("RGB", (self.matrix.width, self.matrix.height), (0,0,0))
        self.matrix.SetImage(blank_frame)

    def update_image(self,url):
        #helper function
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img.thumbnail((32, 32), Image.ANTIALIAS)
        img.convert('RGB')
        return img
    
    def update_image_path(self,path, size):
        img = Image.open(path)
        img.thumbnail((size, size), Image.ANTIALIAS)
        img.convert('RGB')
        return img
    
    def splash_screen(self,activity_name):
        #splash screen for spotify
        screen = Image.new('RGB', (self.matrix.width, self.matrix.height), (0,0,0))
        
        if activity_name.lower() == 'spotify':
            img = self.update_image_path('images/Spotify_icon.png', 22)
            screen.paste(img, (5,4))
            draw = ImageDraw.Draw(screen)
            draw.text((30,10), "Spotify", fill='white', font=self.font)

        if activity_name.lower() == 'crunchyroll':
            img = self.update_image_path('images/crunchyroll.png', 15)
            screen.paste(img, (2,6))
            draw = ImageDraw.Draw(screen)
            draw.text((20,10), "Crunchyroll", fill='white', font=self.font)
        
        self.matrix.SetImage(screen)