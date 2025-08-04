import os
import logging
import sys
import asyncio
import threading
import signal
from pathlib import Path
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования для Amvera
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/data/bot.log') if Path('/data').exists() else logging.NullHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создаем папку для данных если её нет
data_dir = Path('/data')
if data_dir.exists():
    data_dir.mkdir(exist_ok=True)
    logger.info(f"Используется постоянное хранилище: {data_dir}")
else:
    logger.info("Постоянное хранилище недоступно, используем временные файлы")

# Глобальная переменная для хранения приложения
application_instance = None

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    logger.info(f"Получен сигнал {signum}, завершаем работу...")
    if application_instance:
        try:
            # Останавливаем бота асинхронно
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(application_instance.stop())
            loop.close()
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {e}")
    sys.exit(0)

def save_statistics(user_id: int, username: str, message_type: str) -> None:
    """Сохраняет статистику использования бота"""
    try:
        stats_file = data_dir / 'statistics.txt' if data_dir.exists() else Path('statistics.txt')
        with open(stats_file, 'a', encoding='utf-8') as f:
            f.write(f"{user_id},{username},{message_type}\n")
    except Exception as e:
        logger.warning(f"Не удалось сохранить статистику: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start"""
    user = update.effective_user
    save_statistics(user.id, user.username or "unknown", "start")
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
/stats - Показать статистику использования
/health - Проверить здоровье бота

<b>Как использовать:</b>
Просто отправь мне любое сообщение (текст, фото, видео, голосовое сообщение), 
и я повторю его тебе! 🎯

<b>Особенности:</b>
• Поддерживает все типы сообщений
• Сохраняет форматирование текста
• Работает с эмодзи
• Копирует стикеры и GIF
• Сохраняет статистику использования
• Оптимизирован для облачного хостинга
• Мониторинг здоровья системы
    """
    await update.message.reply_html(help_text)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /status"""
    await update.message.reply_text(
        "✅ Бот работает нормально!\n"
        "🟢 Статус: Активен\n"
        "📊 Версия: 1.0.0\n"
        "🌐 Хостинг: Amvera"
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /stats - показывает статистику использования"""
    try:
        stats_file = data_dir / 'statistics.txt' if data_dir.exists() else Path('statistics.txt')
        if stats_file.exists():
            with open(stats_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            if lines:
                total_messages = len(lines)
                unique_users = len(set(line.split(',')[0] for line in lines))
                
                # Подсчитываем типы сообщений
                message_types = {}
                for line in lines:
                    msg_type = line.strip().split(',')[2]
                    message_types[msg_type] = message_types.get(msg_type, 0) + 1
                
                stats_text = f"📊 <b>Статистика бота:</b>\n\n"
                stats_text += f"📈 Всего сообщений: {total_messages}\n"
                stats_text += f"👥 Уникальных пользователей: {unique_users}\n\n"
                stats_text += f"📝 <b>По типам:</b>\n"
                
                for msg_type, count in sorted(message_types.items()):
                    stats_text += f"• {msg_type}: {count}\n"
                
                await update.message.reply_html(stats_text)
            else:
                await update.message.reply_text("📊 Статистика пока пуста")
        else:
            await update.message.reply_text("📊 Файл статистики не найден")
    except Exception as e:
        logger.error(f"Ошибка при чтении статистики: {e}")
        await update.message.reply_text("❌ Ошибка при чтении статистики")

async def health(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /health - проверка здоровья бота"""
    import psutil
    import platform
    
    try:
        # Получаем информацию о системе
        memory = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        health_text = f"🏥 <b>Здоровье бота:</b>\n\n"
        health_text += f"🖥️ <b>Система:</b>\n"
        health_text += f"• Платформа: {platform.system()} {platform.release()}\n"
        health_text += f"• Python: {platform.python_version()}\n"
        health_text += f"• CPU: {cpu_percent:.1f}%\n"
        health_text += f"• RAM: {memory.percent:.1f}% ({memory.used // (1024**3):.1f}GB / {memory.total // (1024**3):.1f}GB)\n\n"
        
        health_text += f"💾 <b>Хранилище:</b>\n"
        if data_dir.exists():
            try:
                stats_file = data_dir / 'statistics.txt'
                if stats_file.exists():
                    size = stats_file.stat().st_size
                    health_text += f"• Статистика: {size} байт\n"
                else:
                    health_text += f"• Статистика: файл не найден\n"
            except Exception as e:
                health_text += f"• Статистика: ошибка чтения\n"
        else:
            health_text += f"• Постоянное хранилище: недоступно\n"
        
        health_text += f"\n✅ <b>Статус:</b> Работает нормально"
        
        await update.message.reply_html(health_text)
    except Exception as e:
        logger.error(f"Ошибка при проверке здоровья: {e}")
        await update.message.reply_text("❌ Ошибка при проверке здоровья бота")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик всех остальных сообщений - эхо"""
    # Получаем информацию о пользователе
    user = update.effective_user
    chat_type = update.effective_chat.type
    
    # Сохраняем статистику
    save_statistics(user.id, user.username or "unknown", "text")
    
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
    elif update.message.animation:
        media_type = "GIF"
        file_id = update.message.animation.file_id
    else:
        media_type = "медиа-файл"
        file_id = None
    
    # Сохраняем статистику
    save_statistics(user.id, user.username or "unknown", media_type)
    
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
        elif update.message.animation:
            await update.message.reply_animation(file_id, caption=caption, parse_mode='HTML')
    else:
        await update.message.reply_text(f"🔄 Получено {media_type}")

async def echo_sticker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик стикеров"""
    user = update.effective_user
    
    # Сохраняем статистику
    save_statistics(user.id, user.username or "unknown", "стикер")
    
    # Логируем
    logger.info(f"Получен стикер от {user.id} ({user.username})")
    
    # Отправляем эхо стикера
    await update.message.reply_sticker(update.message.sticker.file_id)

def run_bot_in_thread(application: Application) -> None:
    """Запускает бота в отдельном потоке с правильным event loop"""
    def run_bot():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(application.run_polling(allowed_updates=Update.ALL_TYPES))
        except Exception as e:
            logger.error(f"Ошибка в боте: {e}")
        finally:
            loop.close()
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    logger.info("Бот запущен в отдельном потоке")

def main() -> None:
    """Запуск бота"""
    # Получаем токен из переменных окружения
    token = os.getenv('BOT_TOKEN')
    
    if not token:
        logger.error("BOT_TOKEN не найден в переменных окружения!")
        logger.error("Создайте файл .env с BOT_TOKEN=your_token_here")
        return
    
    # Проверяем валидность токена
    if not token.startswith('5') or len(token) < 40:
        logger.error("Неверный формат токена! Токен должен начинаться с '5' и быть длинным")
        return
    
    # Создаем приложение
    application = Application.builder().token(token).build()
    
    # Сохраняем глобальную ссылку на приложение
    global application_instance
    application_instance = application
    
    # Настраиваем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("health", health))
    
    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.VOICE | filters.ANIMATION,
        echo_media
    ))
    
    # Отдельный обработчик для стикеров
    application.add_handler(MessageHandler(filters.Sticker.ALL, echo_sticker))
    
    # Запускаем бота
    logger.info("Запуск эхо-бота...")
    
    # Проверяем, запущены ли мы в Amvera (есть ли переменная PORT)
    if os.getenv('PORT'):
        # Запускаем в отдельном потоке для Amvera
        run_bot_in_thread(application)
        
        # Держим основной поток живым
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Получен сигнал остановки")
    else:
        # Обычный запуск для локальной разработки
        application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main() 