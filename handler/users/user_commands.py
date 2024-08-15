from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, ReplyKeyboardRemove
from config import bot, CHANNEL_LIST
from keyboards.admin_button.admin_inline import create_channel_buttons
from keyboards.user_button.user_keyboards import get_user_keyboard
from database import DataBase

# DataBase obyektini yaratish
db = DataBase()

def check_subscription(user_id, channel_name):
    try:
        member = bot.get_chat_member(channel_name, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Xatolik yuz berdi: {str(e)}")
        return False

def is_user_subscribed(user_id):
    return all(check_subscription(user_id, channel) for channel in CHANNEL_LIST)

@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id

    if is_user_subscribed(user_id):
        bot.send_message(message.chat.id, "Salom! Sizni ko'rganimizdan xursandmiz!", reply_markup=get_user_keyboard())
    else:
        markup = types.InlineKeyboardMarkup()
        for index, channel in enumerate(CHANNEL_LIST, start=1):
            markup.add(types.InlineKeyboardButton(text=f"{index}-kanal", url=f"https://t.me/{channel.lstrip('@')}"))
        markup.add(types.InlineKeyboardButton(text="Tasdiqlash", callback_data="confirm_channels"))
        bot.send_message(message.chat.id, "Iltimos, quyidagi kanallarga obuna bo'ling:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'confirm_channels')
def confirm_channel_subscription(call):
    user_id = call.from_user.id
    if is_user_subscribed(user_id):
        bot.send_message(call.message.chat.id, "Siz barcha kanallarga obuna bo'lgansiz!")
    else:
        markup = types.InlineKeyboardMarkup()
        for index, channel in enumerate(CHANNEL_LIST, start=1):
            markup.add(types.InlineKeyboardButton(text=f"{index}-kanal", url=f"https://t.me/{channel.lstrip('@')}"))
        markup.add(types.InlineKeyboardButton(text="Tasdiqlash", callback_data="confirm_channels"))
        bot.send_message(call.message.chat.id, "Siz hali ham quyidagi kanallarga obuna bo'lmagansiz:", reply_markup=markup)

# Admin bilan aloqa tugmasi uchun handler
@bot.message_handler(func=lambda message: message.text == "Murojaat uchun📞" and is_user_subscribed(message.from_user.id))
def contact_admin(message):
    bot.send_message(message.chat.id,
                     "Admin bilan bog'lanish uchun quyidagi ma'lumotlardan foydalaning:\n\nAdmin: @xisomiddin_546")

# Kino kodi tugmasi uchun handler
@bot.message_handler(func=lambda message: message.text == "Kino qidirish🔎" and is_user_subscribed(message.from_user.id))
def enter_kino_code(message):
    bot.send_message(message.chat.id, "Kino kodi kiriting👇🏻:")

# Kino kodini qayta ishlash
@bot.message_handler(func=lambda message: True)
def handle_movie_code(message):
    if not is_user_subscribed(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        for index, channel in enumerate(CHANNEL_LIST, start=1):
            markup.add(types.InlineKeyboardButton(text=f"{index}-kanal", url=f"https://t.me/{channel.lstrip('@')}"))
        markup.add(types.InlineKeyboardButton(text="Tasdiqlash", callback_data="confirm_channels"))
        bot.send_message(message.chat.id, "Iltimos, quyidagi kanallarga obuna bo'ling:", reply_markup=markup)
        return

    if message.text.isdigit():
        kino_kod = message.text

        # Qidiruv emojisini yuborish
        loading_message = bot.send_message(message.chat.id, "🔍", reply_markup=ReplyKeyboardRemove())

        # Kino ma'lumotlarini olish
        kino = db.get_kino_by_kod(kino_kod)

        # Qidiruv natijasini chiqarish
        if kino:
            # Kino ma'lumotlarini ajratish
            kino_id, kod, nomi, yili, janr, tili, video_file_id = kino
            # Kino haqida xabar tayyorlash
            caption = (
                f"🎥Nomi: {nomi}\n"
                f"🔢Kodi: {kod}\n"
                f"📅Yili: {yili}\n"
                f"🎞Janr: {janr}\n"
                f"🇺🇿Tili: {tili}"
            )
            # Qidiruv emojisini o'chirish
            bot.delete_message(message.chat.id, loading_message.message_id)
            # Kino videosini yuborish
            bot.send_video(message.chat.id, video_file_id, caption=caption)
        else:
            # Qidiruv emojisini o'chirish
            bot.delete_message(message.chat.id, loading_message.message_id)
            bot.send_message(message.chat.id,
                             "Kechirasiz, bunday kod bilan kino topilmadi. Iltimos, qayta urinib ko'ring😢.")
    else:
        bot.send_message(message.chat.id, "Iltimos, faqat raqam kiriting🔢.")
