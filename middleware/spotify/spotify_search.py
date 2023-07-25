from typing import Tuple
from init_bot import spotify as sp


async def find_track_and_artist_by_id(track_id: str) -> Tuple[str, str]:
    track_info = sp.track(track_id)
    track_name = track_info.get("name")
    artists = track_info.get("artists")
    artist_name = artists[0].get("name")
    return track_name, artist_name


async def find_track_name_by_id(track_id: str) -> str:
    track_info = sp.track(track_id)
    track_name = track_info.get("name")
    artists = track_info.get("artists")
    artist_names = [artist.get("name") for artist in artists]
    return f"{', '.join(artist_names)} - {track_name}.mp3"


async def get_album_cover(album_id: str) -> str:
    album = sp.album(album_id)
    cover_url = album['images'][0]['url'] if album['images'] else None
    return cover_url