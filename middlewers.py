from telebot import TeleBot
from telebot.handler_backends import BaseMiddleware, CancelUpdate
from config import bot, API_TOKEN

# TeleBot obyektini yaratishda `use_class_middlewares=True` parametrini qo'shamiz
bot = TeleBot(API_TOKEN, use_class_middlewares=True)

class SimpleMiddleware(BaseMiddleware):
    def __init__(self, limit) -> None:
        super().__init__()
        self.last_time = {}
        self.limit = limit
        self.update_types = ['message']

    def pre_process(self, message, data):
        if not message.from_user.id in self.last_time:
            self.last_time[message.from_user.id] = message.date
            return
        if message.date - self.last_time[message.from_user.id] < self.limit:
            bot.send_message(message.chat.id, 'Siz bir oz vaqtda ko\'p so\'rov jo\'natyapsiz! ❗️')
            return CancelUpdate()
        self.last_time[message.from_user.id] = message.date

    def post_process(self, message, data, exception):
        pass

# Middleware'ni botga qo'shish
bot.setup_middleware(SimpleMiddleware(limit=2))  # 2 soniya cheklov vaqtini qo'ydim


