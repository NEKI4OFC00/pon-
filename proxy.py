import telebot
import time
import requests
from telebot import types

TOKEN = '7073943018:AAGUteLIZxIHqVt9TWTYFhDgh0Zby_V-D8s'  # Замените на ваш токен бота
bot = telebot.TeleBot(TOKEN)

# Имя файла для прокси
PROXY_FILE_NAME = "proxies.txt"

# Словарь с ссылками на файлы
proxy_files = {
    "All": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all.txt",
    "All_No_Port": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/all_no_ports.txt",
    "Http": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/http.txt",
    "Https": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/https.txt",
    "Socks4": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks4.txt",
    "Socks5": "https://raw.githubusercontent.com/Tsprnay/Proxy-lists/master/proxies/socks5.txt",
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == 'private':
        bot.reply_to(message, "Добавьте меня в любой чат для начала работы🛠️, Создатели: @TALISOV_ONE , @arcteryx_team (кодер☕)")
    else:
        bot.reply_to(message, "Здравствуйте, я бот созданный для чата TwT по отправке прокси, и проверки скорости ответа телеграмм. Ссылка на наш проект: https://t.me/twtproject")
        # Предоставление прав администратора 
        admin_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

@bot.message_handler(commands=['ping'])
def send_ping(message):
    start_time = time.time()
    msg = bot.reply_to(message, "Проверка времени ответа⌛...")
    end_time = time.time()
    bot.edit_message_text(f"Ответ бота: {int((end_time - start_time) * 1000)} мс⚡", message.chat.id, msg.message_id)

@bot.message_handler(commands=['proxy'])
def send_proxy_choice(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*proxy_files.keys())
    # Используем reply_markup=types.ReplyKeyboardRemove() для удаления кнопок
    msg = bot.reply_to(message, "Выберите тип желаемых прокси и отправьте их ответным сообщением на это (All/Socks4/Socks5/Http/Https), так же не забывайте что все прокси обновляются каждые 20 минут!🕘", reply_markup=markup)
    # Используем message_id для последующего изменения сообщения
    bot.register_next_step_handler(msg, process_proxy_choice) 

def process_proxy_choice(message):
    chosen_proxy_type = message.text
    file_url = proxy_files.get(chosen_proxy_type)

    if file_url:
        bot.reply_to(message, "Ожидайте⏳")

        try:
            response = requests.get(file_url)
            response.raise_for_status()  # Проверка кода ответа (200 - OK)

            # Сохраняем полученные прокси в файл
            with open(PROXY_FILE_NAME, "wb") as f:
                f.write(response.content)

            # Отправляем файл пользователю
            with open(PROXY_FILE_NAME, "rb") as f:
                bot.send_document(chat_id=message.chat.id, document=f, caption=f"Вот ваши прокси в формате {chosen_proxy_type} ")

            # Убираем кнопки после отправки прокси
            bot.send_message(chat_id=message.chat.id, text="Готово! Чтобы выбрать другой тип прокси, напишите /proxy.", reply_markup=types.ReplyKeyboardRemove())

        except requests.exceptions.RequestException as e:
            bot.reply_to(message, f"Ошибка при получении прокси: {e}")

    else:
        bot.reply_to(message, "Неверный тип прокси. Пожалуйста, выберите из списка.")

@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for member in message.new_chat_members:
        bot.reply_to(message, f"Добропожаловать в чат, {member.first_name}! Прочитай лучше сразу правила❗")

@bot.message_handler(content_types=['left_chat_member'])
def goodbye_member(message):
    bot.reply_to(message, "Прощай")

bot.polling()