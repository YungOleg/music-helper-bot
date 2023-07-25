from lyricsgenius import Genius
from util.constants import GENIUS_TOKEN

genius = Genius(GENIUS_TOKEN)


async def search_song(song: str, artist: str):
    try:
        song = genius.search_song(song, artist)
        return song.lyrics
    except Exception as e:
        return "Ошибка поиска трека"