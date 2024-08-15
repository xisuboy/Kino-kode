# Fayl: keyboards/admin_button/admininline.py
from config import CHANNEL_LIST
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_kino_delete_buttons(kino_list):
    markup = InlineKeyboardMarkup()
    for kino in kino_list:
        markup.add(InlineKeyboardButton(kino[1], callback_data=f"delete_kino_{kino[0]}"))
    return markup

def create_confirmation_buttons(kino_kodi):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Ha✅", callback_data=f"confirm_delete_{kino_kodi}"))
    markup.add(InlineKeyboardButton("Yo'q❌", callback_data="cancel_delete"))
    return markup

def create_channel_delete_buttons():
    markup = InlineKeyboardMarkup()
    for i, channel in enumerate(CHANNEL_LIST, start=1):
        markup.add(InlineKeyboardButton(f"{i}-kanal", callback_data=f"delete_channel_{i}"))
    return markup


def create_channel_buttons():
    markup = InlineKeyboardMarkup()
    for index, channel in enumerate(CHANNEL_LIST, start=1):
        channel_url = f"https://t.me/{channel.lstrip('@')}"  # Telegram uchun URL yaratish
        markup.add(InlineKeyboardButton(f"{index}-kanal", url=channel_url))  # Tugmani URL bilan yaratish
    markup.add(InlineKeyboardButton("Tasdiqlash✅", callback_data="confirm_channels"))
    return markup


