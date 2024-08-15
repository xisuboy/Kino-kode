import telebot

DB_NAME = 'NovaBot'
DB_USER = 'postgres'
DB_PASSWORD = '12345678'
DB_HOST = 'localhost'
API_TOKEN = '7269705182:AAEGQo62krmVtQGV01ZHuA9F2UzmxpYi1H4'
bot = telebot.TeleBot(API_TOKEN,  use_class_middlewares=True)

ADMINS = [6266979530]
CHANNEL_LIST = ['@NovaFilmUz', '@XISOMIDDIN_547']
