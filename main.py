import os

import telebot
import qrcode
from io import BytesIO

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

# Вставьте сюда токен вашего бота
bot_token = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(bot_token)

# Функция для генерации QR-кода
def generate_qr_code(link: str):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')

    # Сохраняем изображение в буфер
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправь мне ссылку, и я сгенерирую QR-код для неё.")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    link = message.text
    if link.startswith("http://") or link.startswith("https://"):
        qr_code_buffer = generate_qr_code(link)

        # Отправляем QR-код в виде файла
        bot.send_document(message.chat.id, qr_code_buffer, caption="Вот ваш QR-код", visible_file_name="qrcode.png")
    else:
        bot.reply_to(message, "Пожалуйста, отправьте корректную ссылку (начиная с http:// или https://).")

# Запуск бота
if __name__ == '__main__':
    bot.polling()
