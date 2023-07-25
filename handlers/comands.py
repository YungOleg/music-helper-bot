from init_bot import dp, bot
from aiogram.dispatcher import FSMContext
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from middleware.genius.genius_search_lyrics import get_lyrics_from_genius
from middleware.spotify.spotify_download import *
from middleware.spotify.spotify_search import *
from middleware.lyrics_cleaner import lyrics_cleaner
from middleware.translation import translate_to_ru
from handlers.states import Find_album
from logger import log


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('find_album'))
async def find_album(callback_query: types.CallbackQuery):
    await callback_query.message.answer("Введите имя артиста для поиска его альбомов.")
    await callback_query.message.delete()
    await callback_query.answer()
    await Find_album.wait_artist.set()

@dp.message_handler(state=Find_album.wait_artist)
async def search_artist_albums(message: types.Message, state: FSMContext):
    try:
        artist_name = message.text
        results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
        artist = results['artists']['items'][0]
        artist_image_url = artist['images'][0]['url']
        artist = results['artists']['items'][0]
        artist_id = artist['id']
        albums = sp.artist_albums(artist_id=artist_id, album_type='album')
        if artist_image_url is not None:
            try:
                album_buttons = []
                for album in albums['items']:
                    album_name = album['name']
                    album_id = album['id']
                    button = InlineKeyboardButton(text=album_name, callback_data=f'album::{album_id}')
                    album_buttons.append([button])
                album_buttons.append([InlineKeyboardButton(text="Выход", callback_data="close")])
                album_keyboard = InlineKeyboardMarkup(inline_keyboard=album_buttons)
                caption = f"Выберите альбом «{artist_name.capitalize()}»"
                await bot.send_photo(chat_id=message.from_user.id, photo=artist_image_url, caption=caption, reply_markup=album_keyboard)
                await message.delete()
            except Exception as e:
                log.error(e)
        else:
            await message.answer(f"Артист '{artist_name}' не найден.")
    except Exception as e:
        await message.answer(f"Артист '{artist_name}' не найден.")
    await state.finish()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('album::'))
async def album_tracks_callback(callback_query: types.CallbackQuery):
    album_id = callback_query.data.split('::')[1]
    tracks = sp.album_tracks(album_id=album_id)
    album_info = sp.album(album_id)
    album_name = album_info['name']
    album_artist = album_info['artists'][0]['name']
    try:
        track_buttons = []
        for track in tracks['items']:
            track_name = track['name']
            track_id = track['id']
            button = InlineKeyboardButton(text=track_name, callback_data=f'track::{track_id}')
            track_buttons.append([button])
        track_buttons.append([InlineKeyboardButton(text="← Назад", callback_data=f"back/./{album_artist}")])
        track_keyboard = InlineKeyboardMarkup(inline_keyboard=track_buttons)
        photo = await get_album_cover(album_id)
        caption = f"«{album_name}» by {album_artist}"
        await callback_query.message.edit_media(
            reply_markup=track_keyboard, 
            media=types.InputMediaPhoto(media=photo, caption=caption)
        )
        await callback_query.answer()
    except Exception as e:
        log.error(e)

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('back/./'))
async def back_to_albums(callback_query: types.CallbackQuery):
    data = callback_query.data.split('/./')
    artist_name = data[1]
    results = sp.search(q='artist:' + artist_name, type='artist', limit=1)
    artist = results['artists']['items'][0]
    artist_id = artist['id']
    artist_image_url = artist['images'][0]['url']
    albums = sp.artist_albums(artist_id=artist_id, album_type='album')
    album_buttons = []
    for album in albums['items']:
        album_name = album['name']
        album_id = album['id']
        button = InlineKeyboardButton(text=album_name, callback_data=f'album::{album_id}')
        album_buttons.append([button])
    album_buttons.append([InlineKeyboardButton(text="Выход", callback_data="close")])
    album_keyboard = InlineKeyboardMarkup(inline_keyboard=album_buttons)
    caption = f"Выберите альбом «{artist_name}»"
    await callback_query.message.edit_media(
            reply_markup=album_keyboard, 
            media=types.InputMediaPhoto(media=artist_image_url, caption=caption)
        )
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('close'))
async def close(callback_query: types.CallbackQuery):
    await callback_query.message.delete()
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('track::'))
async def track_callback(callback_query: types.CallbackQuery):
    track_id = callback_query.data.split('::')[1]
    
    track_keyboard = types.InlineKeyboardMarkup(row_width=1)
    get_lyrics_button = types.InlineKeyboardButton("Получить текст", callback_data=f"get_lyrics::{track_id}")
    get_translate_lyrics_button = types.InlineKeyboardButton("Получить перевод", callback_data=f"get_translate_lyrics::{track_id}")
    download_button = types.InlineKeyboardButton("Скачать трек", callback_data=f"download_track::{track_id}")
    close_track_button = types.InlineKeyboardButton("Закрыть", callback_data="close")
    track_keyboard.add(get_lyrics_button)
    track_keyboard.add(get_translate_lyrics_button)
    track_keyboard.add(download_button)
    track_keyboard.add(close_track_button)
    
    track_info = sp.track(track_id)
    track_name = track_info['name']
    caption = f"Выбран трек: {track_name}."
    await bot.send_message(text=caption, chat_id=callback_query.from_user.id, reply_markup=track_keyboard)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('download_track::'))
async def download_track(callback_query: types.CallbackQuery):
    track_id = callback_query.data.split('::')[1]
    track_info = sp.track(track_id)
    track_url = track_info["external_urls"]["spotify"]
    try:
        await callback_query.message.answer("Трек скачивается...")
        #? await download_track_from_spotify(track_url)
        track_name = await find_track_name_by_id(track_id)
        with open(track_name, "rb") as audio_file:
            await bot.send_audio(callback_query.from_user.id, audio=audio_file, caption=track_name)
        #? await remove_track_from_directory(track_name)
    except Exception as e:
        pass
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('get_lyrics::'))
async def get_lyrics(callback_query: types.CallbackQuery):
    track_id = callback_query.data.split('::')[1]
    track_name, artist_name = await find_track_and_artist_by_id(track_id)
    lyrics = await get_lyrics_from_genius(artist_name=artist_name, song_title=track_name)
    if lyrics is not None:
        clean_lyrics = await lyrics_cleaner(lyrics)
        for l in clean_lyrics:
            await bot.send_message(text=l, chat_id=callback_query.from_user.id)
    else:
        await bot.send_message(text=f"Текст «{track_name}» не найден", chat_id=callback_query.from_user.id)
    await callback_query.answer()

@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('get_translate_lyrics::'))
async def get_translate_lyrics(callback_query: types.CallbackQuery):
    track_id = callback_query.data.split('::')[1]
    track_name, artist_name = await find_track_and_artist_by_id(track_id)
    lyrics = await get_lyrics_from_genius(artist_name=artist_name, song_title=track_name)
    if lyrics is not None:
        clean_lyrics = await lyrics_cleaner(lyrics)
        clean_lyrics = "\n\n".join(clean_lyrics)
        translated_lyrics = await translate_to_ru(clean_lyrics)
        # formatted_lyrics = await format_translation(original_text=clean_lyrics, translated_text=translated_lyrics)
        # for l in clean_lyrics:
        #     await bot.send_message(text=l, chat_id=callback_query.from_user.id, parse_mode = 'html')
    else:
        await bot.send_message(text=f"Текст «{track_name}» не найден", chat_id=callback_query.from_user.id)
    await callback_query.answer()