from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_user_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Murojaat uchun📞"))
    markup.add(KeyboardButton("Kino qidirish🔎"))
    return markup
