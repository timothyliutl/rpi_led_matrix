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
from discord.ext import commands


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
        self.current_activity = None
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.screens = ['spotify', 'crunchyroll', 'clock']
        self.active_flag = True
        self.activity_data = {}

        self.t1 = threading.Thread(target=self.update_display)
        self.t1.setDaemon(True)
        self.t1.start()

    #helper functions
    def update_display(self):
        while True:
            if self.active_flag:
                with self.lock:
                    if self.current_activity == 'spotify':
                        #spotify screen
                        self.led_matrix.update_spotify_display() 
                        time.sleep(0.2)
                    if self.current_activity == 'crunchyroll':
                        pass
    
    def update_activity_data(self,activities):
        for act in activities:
            if isinstance(act, discord.Spotify):
                song_name = act.title
                song_artist =act.artists[0]
                album_cover_url = act.album_cover_url
                self.activity_data['spotify'] = {'song_name':song_name,
                                                 'song_artist': song_artist,
                                                 'album_cover_url': album_cover_url,
                                                 "start": act.start,
                                                 "end": act.end}
            elif act.name.lower() == 'crunchyroll':
                self.activity_data['crunchyroll'] = {
                    "show_name":act.details,
                    "image_url": act.large_image_url,
                    "timestamps": act.timestamps
                    #TODO: figure out how to get anime image url from this
                }
                
                
    #decorator functions
    async def on_message(self, message):
        author = message.author.id
        message_content = message.content

        if author == int(user_id):
            if str(message_content).lower() == "activate":

                if self.active_flag:
                    await message.channel.send("Already Activated")
                else:
                    await message.channel.send("Turning On LED Matrix")
                    self.active_flag = True

            elif str(message_content).lower() == "deactivate":
                if not self.active_flag:
                    await message.channel.send("Already deactivated")
                else:
                    await message.channel.send("Turning off LED Matrix")
                    self.active_flag = False
                    time.sleep(0.2)
                    self.led_matrix.turn_off_display()

            #yeah i know i could have used case and switch but whatever
            elif str(message_content).lower() == 'spotify':
                await message.channel.send("Setting Screen to Spotify")
                
                self.lock.acquire()
                self.active_flag = not self.active_flag
                self.led_matrix.splash_screen('spotify')
                self.current_activity = 'spotify'
                time.sleep(2)
                self.active_flag = not self.active_flag
                self.led_matrix.turn_off_display()
                self.lock.release()

            elif str(message_content).lower() == 'crunchyroll':
                await message.channel.send("Setting Screen to Crunchyroll")

                self.lock.acquire()
                self.active_flag = not self.active_flag
                self.current_activity = 'crunchyroll'
                self.led_matrix.splash_screen('crunchyroll')
                time.sleep(2)
                self.active_flag = not self.active_flag
                self.led_matrix.turn_off_display()
                self.lock.release()

            elif str(message_content).lower() == 'clock':
                await message.channel.send("Setting Screen to Clock")
                self.current_activity = 'clock'
            

    async def on_ready(self):
        print("Bot Ready")

    async def on_presence_update(self, before, after):

        if after.activities and self.active_flag and after.id ==int(user_id):
            activities = after.activities
            self.update_activity_data(activities)


        if self.active_flag and self.current_activity == 'spotify' and 'spotify' in self.activity_data.keys():
            self.lock.acquire()
            self.led_matrix.update_song(self.activity_data['spotify']['album_cover_url'],
                                         self.activity_data['spotify']['song_name'], 
                                         self.activity_data['spotify']['song_artist'])
            self.lock.release()
    
class_client = DiscordClient(intents=intents)
class_client.run(token)


