from typing import Any
import discord
from discord.flags import Intents
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
server_id = os.getenv('DISCORD_SERVER_ID')

#adding class based structure for discord client
class DiscordClient(discord.Client):
    def __init__(self, *, intents: Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.led_matrix = MatrixClass()
        self.lock = threading.Lock()
        self.t1 = threading.Thread(target=self.update_display)
        self.t1.setDaemon(True)
        self.t1.start()

    def update_display(self):
        while True:
            with self.lock:
                self.led_matrix.update_display()
                time.sleep(0.2)

    async def on_ready(self):
        print("Bot Ready")

    async def on_presence_update(self, before, after):
        if after.activities:
            activities = after.activities
            for act in activities:
                if isinstance(act, discord.Spotify) and after.id ==int(user_id):
                    song_name = act.title
                    song_artist =act.artists[0]
                    print(song_name, song_artist)
                    album_cover_url = act.album_cover_url
                    self.lock.acquire()
                    self.led_matrix.update_song(album_cover_url, str(song_name), str(song_artist))
                    self.lock.release()
    
class_client = DiscordClient(intents=intents)
class_client.run(token)


