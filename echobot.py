#!/usr/bin/env python3
"""
Простой эхо-бот для Telegram
Основан на примере python-telegram-bot и адаптирован для Amvera
"""

import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Настройка логирования для Amvera
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    await update.message.reply_html(
        f"Привет, {user.mention_html()}! 👋\n\n"
        "Я простой эхо-бот. Просто отправь мне любое сообщение, "
        "и я повторю его тебе! 🎯"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🤖 <b>Эхо-бот - Справка</b>

<b>Доступные команды:</b>
/start - Начать работу с ботом
/help - Показать эту справку

<b>Как использовать:</b>
Просто отправь мне любое сообщение, и я повторю его тебе! 🎯
    """
    await update.message.reply_html(help_text)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех остальных сообщений - эхо"""
    await update.message.reply_text(update.message.text)

def main() -> None:
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    
    # Добавляем обработчик сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # Запускаем бота
    logger.info("Запуск эхо-бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 