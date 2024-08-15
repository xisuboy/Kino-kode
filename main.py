import telebot
from config import bot, ADMINS
from database import *
from config import bot
from middlewers import SimpleMiddleware

bot.setup_middleware(SimpleMiddleware(0.6))


import handler


if __name__ == "__main__":
    print('Bot ishladi...')

    bot.infinity_polling()
