import os
import subprocess
import sys
from spotdl import __main__ as spotdl


async def download_track_from_spotify(url: str) -> None:
    subprocess.check_call([sys.executable, spotdl.__file__, url])


async def remove_track_from_directory(track_name: str) -> None:
    os.remove(track_name)