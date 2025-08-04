import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
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
        "и я повторю его тебе! 🎯\n\n"
        "Используй /help для получения справки."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
🤖 <b>Эхо-бот - Справка</b>

<b>Доступные команды:</b>
/start - Начать работу с ботом
/help - Показать эту справку
/status - Показать статус бота

<b>Как использовать:</b>
Просто отправь мне любое сообщение (текст, фото, видео, голосовое сообщение), 
и я повторю его тебе! 🎯

<b>Особенности:</b>
• Поддерживает все типы сообщений
• Сохраняет форматирование текста
• Работает с эмодзи
• Копирует стикеры и GIF
    """
    await update.message.reply_html(help_text)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /status"""
    await update.message.reply_text(
        "✅ Бот работает нормально!\n"
        "🟢 Статус: Активен\n"
        "📊 Версия: 1.0.0"
    )

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех остальных сообщений - эхо"""
    # Получаем информацию о пользователе
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    # Логируем сообщение
    logger.info(f"Получено сообщение от {user.id} ({user.username}) в {chat_type}: {update.message.text}")
    
    # Отправляем эхо
    await update.message.reply_text(
        f"🔄 <b>Эхо:</b>\n{update.message.text}",
        parse_mode='HTML'
    )

async def echo_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик медиа-сообщений"""
    user = update.effective_user
    
    # Определяем тип медиа
    if update.message.photo:
        media_type = "фото"
        file_id = update.message.photo[-1].file_id
    elif update.message.video:
        media_type = "видео"
        file_id = update.message.video.file_id
    elif update.message.voice:
        media_type = "голосовое сообщение"
        file_id = update.message.voice.file_id
    elif update.message.sticker:
        media_type = "стикер"
        file_id = update.message.sticker.file_id
    elif update.message.animation:
        media_type = "GIF"
        file_id = update.message.animation.file_id
    else:
        media_type = "медиа-файл"
        file_id = None
    
    # Логируем
    logger.info(f"Получено {media_type} от {user.id} ({user.username})")
    
    # Отправляем эхо
    caption = f"🔄 <b>Эхо {media_type}:</b>"
    if update.message.caption:
        caption += f"\n{update.message.caption}"
    
    if file_id:
        if update.message.photo:
            await update.message.reply_photo(file_id, caption=caption, parse_mode='HTML')
        elif update.message.video:
            await update.message.reply_video(file_id, caption=caption, parse_mode='HTML')
        elif update.message.voice:
            await update.message.reply_voice(file_id, caption=caption, parse_mode='HTML')
        elif update.message.sticker:
            await update.message.reply_sticker(file_id)
            if caption != f"🔄 <b>Эхо {media_type}:</b>":
                await update.message.reply_text(caption, parse_mode='HTML')
        elif update.message.animation:
            await update.message.reply_animation(file_id, caption=caption, parse_mode='HTML')
    else:
        await update.message.reply_text(f"🔄 Получено {media_type}")

def main() -> None:
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        logger.error("Создайте файл .env с BOT_TOKEN=your_token_here")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    
    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.VOICE | filters.STICKER | filters.ANIMATION,
        echo_media
    ))
    
    # Запускаем бота
    logger.info("Запуск эхо-бота...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 