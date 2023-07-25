import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from lyricsgenius import Genius
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from util.constants import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, TELEGRAM_TOKEN, GENIUS_TOKEN


storage = MemoryStorage()
bot = Bot(TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=storage)


client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


genius = Genius(GENIUS_TOKEN)