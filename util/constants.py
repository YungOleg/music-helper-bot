import os
from dotenv import load_dotenv
from typing import Final

load_dotenv()

TELEGRAM_TOKEN: Final = os.getenv("TELEGRAM_TOKEN") 
GENIUS_TOKEN: Final = os.getenv("GENIUS_TOKEN") 
ADMIN_ID: Final = os.getenv("ADMIN_ID")
SPOTIFY_CLIENT_ID: Final = os.getenv("SPOTIFY_CLIENT_ID") 
SPOTIFY_CLIENT_SECRET: Final  =os.getenv("SPOTIFY_CLIENT_SECRET")