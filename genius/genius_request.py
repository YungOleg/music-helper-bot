from util.constants import GENIUS_TOKEN
from lyricsgenius import Genius

genius = Genius(GENIUS_TOKEN)

# async def search_song(song: str, artist: str):
#     song = genius.search_song(song, artist)
#     return song.lyrics

async def search_song(song: str):
    song = genius.search_song(song, "Friendly thug")
    return song.lyrics