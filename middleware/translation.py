from langdetect import detect 
from deep_translator import GoogleTranslator
from typing import Optional


async def translate_to_ru(text: str) -> str:
    from_lang = _detect_language(text)
    if from_lang is not None and from_lang != "ru":
        translated_text = GoogleTranslator(source=from_lang, target="ru").translate(text)
        return translated_text
    else:
        return text


async def _detect_language(text: str) -> Optional[str]:
    try:
        detected_lang = detect(text)
        return detected_lang
    except:
        return None