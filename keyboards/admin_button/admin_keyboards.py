from telebot import types

def get_admin_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Reklama xabarini yuborish"))
    markup.add(types.KeyboardButton("Kino qo'shish"), types.KeyboardButton("Kino o'chirish"))
    markup.add(types.KeyboardButton("Kanal qo'shish"), types.KeyboardButton("Kanal o'chirish"))
    markup.add(types.KeyboardButton("Statistika"))


    return markup

def get_reklama_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Matn yuborish"), types.KeyboardButton("Video yuborish"))
    markup.add(types.KeyboardButton("Rasm yuborish"), types.KeyboardButton("Ovozli habar yuborish"))
    markup.add(types.KeyboardButton("Orqaga"))
    return markup
