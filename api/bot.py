from http.server import BaseHTTPRequestHandler
import json
import os
import sys

# Добавляем путь к родительской директории для импорта модулей
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# Состояния для разговора
WAITING_NAME = 1

# Конфигурация
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7052592700:AAEzgL-EsnETAuXhJZPBA6vSLHXgxkKIeOU')

# Создаем приложение
application = Application.builder().token(BOT_TOKEN).build()

# Обработчики
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

# Настраиваем обработчики
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        WAITING_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
)

application.add_handler(conv_handler)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Получаем данные от Telegram
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        # Парсим JSON
        update_data = json.loads(post_data.decode('utf-8'))
        update = Update.de_json(update_data, application.bot)
        
        # Обрабатываем обновление
        application.process_update(update)
        
        # Отправляем ответ
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({'status': 'ok'}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Bot is running!'.encode()) 