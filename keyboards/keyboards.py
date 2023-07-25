from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

menu_keyboard =InlineKeyboardMarkup(row_width=1)

find_album_button = InlineKeyboardButton("Найти альбом", callback_data="find_album")
translate_track_button = InlineKeyboardButton("Перевести трек", callback_data="translate_track")
download_track_button = InlineKeyboardButton("Скачать трек", callback_data="download_track")
close_menu_button = InlineKeyboardButton("Закрыть меню", callback_data="close")

menu_keyboard.add(find_album_button)
menu_keyboard.add(translate_track_button)
menu_keyboard.add(download_track_button)
menu_keyboard.add(close_menu_button)


open_menu_button = KeyboardButton("Открыть меню")
open_menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
open_menu_keyboard.add(open_menu_button)