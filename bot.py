import os
import openai
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Настройки
API_KEY = 'КЛЮЧ БОТА В ТГ'
OPENAI_API_KEY = 'КЛЮЧ ДЛЯ ИИ'
ALLOWED_USER_ID = 'ВАШ АЙДИ'
OPENAI_API_BASE = 'СЕРВЕР ГДЕ РАБОТАЕТ МОДЕЛЬ ИЛИ ПРОКСИ' # Сервер Github Models: https://models.inference.ai.azure.com

# Инициализация OpenAI
openai.api_key = OPENAI_API_KEY
openai.api_base = OPENAI_API_BASE

# Инициализация бота
updater = Updater(API_KEY, use_context=True)
dispatcher = updater.dispatcher

# Сохранение истории
history = []

# Команда /start
def start(update, context):
    if str(update.message.chat_id) == ALLOWED_USER_ID:
        update.message.reply_text('Привет! Я бот, использующий *ChatGPT*. Чем могу помочь?', parse_mode='Markdown')
    else:
        update.message.reply_text('Извините, этот бот доступен только для определенного пользователя.', parse_mode='Markdown')

# Команда /reset
def reset(update, context):
    global history
    if str(update.message.chat_id) == ALLOWED_USER_ID:
        history = []
        update.message.reply_text('История очищена.', parse_mode='Markdown')
    else:
        update.message.reply_text('Извините, этот бот доступен только для определенного пользователя.', parse_mode='Markdown')

# Обработка сообщений
def handle_message(update, context):
    global history
    if str(update.message.chat_id) == ALLOWED_USER_ID:
        user_message = update.message.text
        history.append({"role": "user", "content": user_message})

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=history
        )

        bot_message = response['choices'][0]['message']['content']
        history.append({"role": "assistant", "content": bot_message})

        update.message.reply_text(bot_message, parse_mode='Markdown')  # Добавлен parse_mode
    else:
        update.message.reply_text('Извините, этот бот доступен только для определенного пользователя.', parse_mode='Markdown')

# Обработчики команд
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(CommandHandler('reset', reset))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

# Запуск бота
def main():
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
