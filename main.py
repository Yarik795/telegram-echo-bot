#!/usr/bin/env python3
"""
Основной файл для запуска Telegram бота на Amvera
"""
import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Состояния для разговора
WAITING_NAME = 1

# Включаем логирование
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Получаем токен из переменной окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7052592700:AAEzgL-EsnETAuXhJZPBA6vSLHXgxkKIeOU')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    return WAITING_NAME

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    await update.message.reply_text(f"Привет, {name}!")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Разговор отменен.")
    return ConversationHandler.END

def main():
    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Настраиваем обработчики
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(conv_handler)
    
    # Запускаем бота в режиме polling
    application.run_polling()

if __name__ == '__main__':
    main() 