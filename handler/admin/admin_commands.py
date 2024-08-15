import telebot
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import bot, ADMINS, CHANNEL_LIST
from database import DataBase
from keyboards.admin_button.admin_keyboards import get_admin_keyboard, get_reklama_keyboard

# DataBase obyektini yaratish
db = DataBase()

@bot.message_handler(commands=['admin'])
def handle_admin_start(message):
    user_id = message.from_user.id
    print(f"Received ID: {user_id}")
    if user_id in ADMINS:
        bot.send_message(message.chat.id, 'Admin paneliga xush kelibsiz!', reply_markup=get_admin_keyboard())
    else:
        bot.send_message(message.chat.id, "Sizda admin huquqlari yo'q.")

@bot.message_handler(func=lambda message: message.text == 'Reklama xabarini yuborish')
def reklama_xabar(message):
    bot.send_message(message.chat.id, 'Reklama xabarini qanday yubormoqchisiz?', reply_markup=get_reklama_keyboard())

@bot.message_handler(func=lambda message: message.text == 'Matn yuborish')
def reklama_matn(message):
    msg = bot.send_message(message.chat.id, 'Reklama matnini kiriting:')
    bot.register_next_step_handler(msg, process_reklama_matn)

def process_reklama_matn(message):
    reklama_text = message.text
    try:
        users = db.get_user_ids()
        for user in users:
            bot.send_message(user[0], reklama_text)
        bot.send_message(message.chat.id, 'Reklama matni muvaffaqiyatli yuborildi!')
    except Exception as e:
        bot.send_message(message.chat.id, f'Xatolik yuz berdi! Xabar yuborishda xatolik: {str(e)}')

@bot.message_handler(func=lambda message: message.text == 'Video yuborish')
def reklama_video(message):
    msg = bot.send_message(message.chat.id, 'Reklama videosini yuboring:')
    bot.register_next_step_handler(msg, receive_video)

def receive_video(message):
    if message.content_type == 'video':
        video_file_id = message.video.file_id
        msg = bot.reply_to(message, "Videoga qo'shiladigan matnni yozing (yoki 'skip' deb yozing):")
        bot.register_next_step_handler(msg, lambda msg: broadcast_message(msg, video_file_id, 'video'))
    else:
        bot.reply_to(message, "Iltimos, video fayl yuboring.")

@bot.message_handler(func=lambda message: message.text == 'Rasm yuborish')
def reklama_rasm(message):
    msg = bot.send_message(message.chat.id, 'Reklama rasmini yuboring:')
    bot.register_next_step_handler(msg, receive_image)

def receive_image(message):
    if message.content_type == 'photo':
        photo_file_id = message.photo[-1].file_id
        msg = bot.reply_to(message, "Rasmga qo'shiladigan matnni yozing (yoki 'skip' deb yozing):")
        bot.register_next_step_handler(msg, lambda msg: broadcast_message(msg, photo_file_id, 'photo'))
    else:
        bot.reply_to(message, "Iltimos, rasm fayl yuboring.")

@bot.message_handler(func=lambda message: message.text == 'Ovozli habar yuborish')
def reklama_ovoz(message):
    msg = bot.send_message(message.chat.id, 'Reklama ovozli habarnini yuboring:')
    bot.register_next_step_handler(msg, receive_voice)

def receive_voice(message):
    if message.content_type == 'voice':
        voice_file_id = message.voice.file_id
        msg = bot.reply_to(message, "Ovozli habarga qo'shiladigan matnni yozing (yoki 'skip' deb yozing):")
        bot.register_next_step_handler(msg, lambda msg: broadcast_message(msg, voice_file_id, 'voice'))
    else:
        bot.reply_to(message, "Iltimos, ovozli habar fayl yuboring.")

def broadcast_message(message, file_id, file_type):
    caption = message.text if message.text.lower() != 'skip' else None
    users = db.get_user_ids()
    for user in users:
        if file_type == 'video':
            bot.send_video(user[0], file_id, caption=caption)
        elif file_type == 'photo':
            bot.send_photo(user[0], file_id, caption=caption)
        elif file_type == 'voice':
            bot.send_voice(user[0], file_id, caption=caption)
    bot.reply_to(message, f"{file_type.capitalize()} barcha foydalanuvchilarga yuborildi!")

@bot.message_handler(func=lambda message: message.text == "Kino qo'shish")
def add_kino(message):
    msg = bot.send_message(message.chat.id, 'Kino nomini kiriting:')
    bot.register_next_step_handler(msg, process_add_kino_step_1)

def process_add_kino_step_1(message):
    kino_nomi = message.text
    msg = bot.send_message(message.chat.id, 'Kino kodini kiriting:')
    bot.register_next_step_handler(msg, process_add_kino_step_2, kino_nomi)

def process_add_kino_step_2(message, kino_nomi):
    kino_kodi = message.text
    msg = bot.send_message(message.chat.id, 'Kino yilini kiriting:')
    bot.register_next_step_handler(msg, process_add_kino_step_3, kino_nomi, kino_kodi)

def process_add_kino_step_3(message, kino_nomi, kino_kodi):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Iltimos, faqat raqam kiriting.")
        return
    kino_yili = message.text
    msg = bot.send_message(message.chat.id, 'Kino janrini kiriting:')
    bot.register_next_step_handler(msg, process_add_kino_step_4, kino_nomi, kino_kodi, kino_yili)

def process_add_kino_step_4(message, kino_nomi, kino_kodi, kino_yili):
    kino_janri = message.text
    msg = bot.send_message(message.chat.id, 'Kino tilini kiriting:')
    bot.register_next_step_handler(msg, process_add_kino_step_5, kino_nomi, kino_kodi, kino_yili, kino_janri)

def process_add_kino_step_5(message, kino_nomi, kino_kodi, kino_yili, kino_janri):
    kino_tili = message.text
    msg = bot.send_message(message.chat.id, 'Kino videosini yuboring:')
    bot.register_next_step_handler(msg, process_add_kino_step_6, kino_nomi, kino_kodi, kino_yili, kino_janri, kino_tili)

def process_add_kino_step_6(message, kino_nomi, kino_kodi, kino_yili, kino_janri, kino_tili):
    if message.content_type == 'video':
        video_file_id = message.video.file_id
        try:
            db.insert_kino(kino_nomi, kino_kodi, kino_yili, kino_janri, kino_tili, video_file_id)
            bot.send_message(message.chat.id, 'Kino muvaffaqiyatli qo\'shildi!')
        except Exception as e:
            bot.send_message(message.chat.id, f'Xatolik yuz berdi: {str(e)}')
    else:
        bot.reply_to(message, "Iltimos, video fayl yuboring.")

@bot.message_handler(func=lambda message: message.text == 'Kanal qo\'shish')
def add_channel(message):
    msg = bot.send_message(message.chat.id, 'Kanal nomini kiriting:')
    bot.register_next_step_handler(msg, process_add_channel)

def process_add_channel(message):
    channel_name = message.text
    try:
        # Kanalni CHANNEL_LIST ga qo'shish
        if channel_name not in CHANNEL_LIST:
            CHANNEL_LIST.append(channel_name)
            db.add_channel(channel_name)  # Database ga kanalni qo'shamiz
            bot.send_message(message.chat.id, f'Kanal "{channel_name}" muvaffaqiyatli qo\'shildi!')
        else:
            bot.send_message(message.chat.id, f'Kanal "{channel_name}" allaqachon mavjud.')
    except Exception as e:
        bot.send_message(message.chat.id, f'Xatolik yuz berdi: {str(e)}')
# Kanal o'chirish
@bot.message_handler(func=lambda message: message.text == "Kanal o'chirish")
def delete_channel(message):
    if CHANNEL_LIST:
        markup = types.InlineKeyboardMarkup()
        for channel in CHANNEL_LIST:
            markup.add(types.InlineKeyboardButton(text=channel, callback_data=f"delete_channel_{channel}"))
        bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan kanalingizni tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hech qanday kanal topilmadi.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_channel_'))
def confirm_delete_channel(call):
    channel_name = call.data.split('_')[2]
    if channel_name in CHANNEL_LIST:
        CHANNEL_LIST.remove(channel_name)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f"Kanal '{channel_name}' muvaffaqiyatli o'chirildi!")
    else:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text="Kanal topilmadi.")

@bot.message_handler(func=lambda message: message.text == "Kino o'chirish")
def delete_kino(message):
    kino_list = db.get_all_kino()  # Database'dan barcha kinolarni olish
    if kino_list:
        markup = InlineKeyboardMarkup()
        for kino in kino_list:
            markup.add(InlineKeyboardButton(kino[1], callback_data=f"delete_kino_{kino[0]}"))
        bot.send_message(message.chat.id, "O'chirmoqchi bo'lgan kinoingizni tanlang:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Hech qanday kino topilmadi.")

@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_kino_'))
def confirm_delete_kino(call):
    kino_kod = call.data.split('_')[2]

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Ha", callback_data=f"confirm_delete_kino_{kino_kod}"))
    markup.add(InlineKeyboardButton("Yo'q", callback_data="cancel_delete_kino"))
    bot.send_message(call.message.chat.id, f'Siz haqiqatdan ham ushbu kinoni o\'chirmoqchimisiz?', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith('confirm_delete_kino_'))
def delete_kino_confirmed(call):
    kino_kod = call.data.split('_')[3]
    try:
        db.delete_kino_by_kod(kino_kod)  # Database'dan kino'ni o'chirish
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                              text=f'Kino "{kino_kod}" muvaffaqiyatli o\'chirildi!')
    except Exception as e:
        bot.send_message(call.message.chat.id, f'Xatolik yuz berdi: {str(e)}')

@bot.callback_query_handler(func=lambda call: call.data == 'cancel_delete_kino')
def cancel_delete_kino(call):
    bot.send_message(call.message.chat.id, "Kino o'chirish bekor qilindi.")

@bot.message_handler(func=lambda message: message.text == 'Statistika')
def show_statistics(message):
    user_id = message.from_user.id
    if user_id in ADMINS:
        try:
            user_count = db.get_user_count()
            kino_count = db.get_kino_count()
            channel_count = len(CHANNEL_LIST)
            stats_message = (
                f"Foydalanuvchilar soni: {user_count}\n"
                f"Kino soni: {kino_count}\n"
                f"Kanal soni: {channel_count}"
            )
            bot.send_message(message.chat.id, stats_message)
        except Exception as e:
            bot.send_message(message.chat.id, f'Xatolik yuz berdi! Statistikani olishda xatolik: {str(e)}')
    else:
        bot.send_message(message.chat.id, "Sizda admin huquqlari yo'q.")



@bot.message_handler(func=lambda message:message.text == 'Orqaga')
def Orqaga(message:Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Asosiy menyu', reply_markup=get_admin_keyboard())
