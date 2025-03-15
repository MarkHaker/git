import telebot 
from config import token 

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: 
        chat_id = message.chat.id 
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
       
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) 
            bot.reply_to(message, f"Отдыхай @{message.reply_to_message.from_user.username} .")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(func=lambda message: True) 
def check_links(message):
    if "https://" in message.text or "http://" in message.text:
        # Запрещаем ссылки
        chat_id = message.chat.id
        user_id = message.from_user.id
        try:
            username = message.from_user.username
        except:
            username = "Пользователь без имени пользователя"
        with open("banned_users.txt", "a") as f:
            f.write(f"User ID: {user_id}, Username: {username}, Message: {message.text}\n")

        bot.ban_chat_member(chat_id, user_id)
        bot.reply_to(message, f"@{username} забанен за публикацию ссылки.")

bot.infinity_polling(none_stop=True)
