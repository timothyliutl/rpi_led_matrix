import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from apps import spotify_app
import spotipy
import requests
from io import BytesIO

file_path = './images/seraphine.png'


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
options.gpio_slowdown=4


matrix = RGBMatrix(options = options)

spotify = spotify_app.Spotipy_App()


def update_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.thumbnail((matrix.width, matrix.height), Image.ANTIALIAS)
    img.convert('RGB')
    return img

#matrix.SetImage(image.convert('RGB'))
try:
    print("press ctrl-c to stop")
    global img
    counter = 0
    animation_counter = 0
    font = ImageFont.truetype('./fonts/Comme-VariableFont_wght.ttf', 8)
    while True:
        counter = counter%4
        animation_counter = animation_counter %32
        frame = Image.new("RGB", (matrix.width, matrix.height), (0,0,0))
        draw = ImageDraw.Draw(frame)

        if counter == 0:
            song_data = spotify.get_current_song()
            is_playing = song_data['is_playing']
            image_url = song_data['item']['album']['images'][0]['url']
            name = song_data['item']['name']
            artist = song_data['item']['artists'][0]['name']
            img = update_image(image_url)
        frame.paste(img)

        draw.text((34 ,0), name, font=font)
        draw.text((34 ,9), artist, font= font)

        if is_playing:
            draw.line((45,19,45,25))
            draw.line((46,19,46,25))
            draw.line((49,19,49,25))
            draw.line((50,19,50,25))
            
        else:
            draw.line((45,19,45,25))
            draw.line((46,20,46,24))
            draw.line((47,20,47,24))
            draw.line((48,21,48,23))
            draw.line((49,21,49,23))
            draw.line((50,22,50,22))

        matrix.SetImage(frame)

        time.sleep(0.5)
        counter += 1
        animation_counter+=1

        


except KeyboardInterrupt:
    sys.exit(0)