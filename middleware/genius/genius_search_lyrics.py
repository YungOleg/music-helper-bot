from init_bot import genius
from typing import Optional


async def get_lyrics_from_genius(artist_name: str, song_title: str) -> Optional[str]:
    song = genius.search_song(song_title, artist_name)
    if song:
        return song.lyrics
    else:
        return None