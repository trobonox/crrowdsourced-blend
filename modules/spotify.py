import logging, discord, datetime
import re
from discord.ext import commands
from utils import config, db

import spotipy
from spotipy.oauth2 import SpotifyOAuth

config = config.config()
connection, _ = db.get_db_connection()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=config.spotify_client_id,
        client_secret=config.spotify_client_secret,
        redirect_uri=config.spotify_redirect_url,
        scope="playlist-modify-private",
        open_browser=False
    )
)

class spotify(commands.Cog):
    def __init__(self, client):
        logging.info(f"Loaded {self.__class__.__name__.title()} module.")

        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if not (message.channel.id == config.blend_thread_id and isinstance(message.channel, discord.Thread)):
            return

        urls = re.findall(r"\b(https:\/\/open\.spotify\.com\/track\/[A-z0-9]{22})\b", message.content)

        if len(urls) == 0: return

        if len(urls) > 3:
            return await message.reply("You cannot submit more than three picks!")
        
        user_records = db.get_records("SELECT * FROM picks WHERE user_id = ?", message.author.id)

        this_month_counter = 0
        if len(user_records) >= 3:
            for record in user_records:
                if record[2][:7] == datetime.datetime.now().strftime("%Y-%m"):
                    this_month_counter += 1
            
            if this_month_counter >= 3:
                return await message.reply("You have already submitted your 3 picks. If you want to change your picks, please notify an admin to reset your picks for this month.")
        
        for url in urls:
            await self.addPick(url, message.author.id)
        connection.commit()
        
        sp.playlist_add_items(config.spotify_blend_playlist_url, urls)
        await message.add_reaction("✅")
        

    async def addPick(self, url: str, user_id: int) -> int:
        db.execute("INSERT INTO picks(user_id, pick_url) VALUES(?, ?)", user_id, url)

async def setup(client):
    await client.add_cog(spotify(client))