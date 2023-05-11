import discord
from dotenv import load_dotenv
import os
from discord.ext import tasks
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image, ImageDraw, ImageFont
from matrix_class import MatrixClass
import time
import threading


load_dotenv()
intents = discord.Intents.default()
intents.presences=True
intents.members = True
client = discord.Client(intents=intents)
token = os.getenv('DISCORD_TOKEN')
user_id = os.getenv('DISCORD_ID')
led_matrix = MatrixClass()
lock = threading.Lock()

def update_display():
    while True:
        with lock:
            led_matrix.update_display()
            time.sleep(0.2)


t1 = threading.Thread(target=update_display)
t1.setDaemon(True)
t1.start()

@client.event
async def on_ready():
    print("Bot Ready")
    # input function to check for current status

@client.event
async def on_presence_update(before, after):
    if after.activities:
        activities = after.activities
        for act in activities:
            if isinstance(act, discord.Spotify) and after.id ==int(user_id):
                song_name = act.title
                song_artist =act.artists[0]
                print(song_name, song_artist)
                album_cover_url = act.album_cover_url
                lock.acquire()
                led_matrix.update_song(album_cover_url, str(song_name), str(song_artist))
                lock.release()
client.run(token)


