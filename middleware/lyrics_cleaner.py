import re 
from typing import List

async def lyrics_cleaner(lyrics: str) -> List[str]:
    lyrics_list = lyrics.split("\n\n")
    pattern = r"\d+Embed" 
    replaced_string = re.sub(pattern, "", lyrics_list[-1])
    bracket_index = lyrics_list[0].find('[')
    if bracket_index != -1:
        lyrics_list[0] = lyrics_list[0][bracket_index:]
    lyrics_list[-1] = replaced_string.strip()
    return lyrics_list