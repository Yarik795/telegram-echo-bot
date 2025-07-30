#!/usr/bin/env python3
"""
Веб-сервер для Telegram бота на Amvera
"""
import os
import logging
from flask import Flask, request, jsonify
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

# Создаем Flask приложение
app = Flask(__name__)

# Создаем Telegram приложение
telegram_app = Application.builder().token(BOT_TOKEN).build()

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

telegram_app.add_handler(conv_handler)

@app.route('/')
def home():
    """Главная страница"""
    return '''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Telegram Echo Bot - Amvera</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            h1 {
                color: #333;
                text-align: center;
            }
            .status {
                background: #e8f5e8;
                border: 1px solid #4caf50;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
            .bot-info {
                background: #f0f8ff;
                border: 1px solid #2196f3;
                padding: 15px;
                border-radius: 5px;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Telegram Echo Bot</h1>
            
            <div class="status">
                <h3>✅ Статус: Работает</h3>
                <p>Бот успешно развернут на Amvera и готов к работе!</p>
            </div>
            
            <div class="bot-info">
                <h3>📱 Информация о боте</h3>
                <ul>
                    <li><strong>Платформа:</strong> Amvera</li>
                    <li><strong>Язык:</strong> Python</li>
                    <li><strong>Библиотека:</strong> python-telegram-bot</li>
                    <li><strong>Функции:</strong> Простой диалог с пользователем</li>
                </ul>
            </div>
            
            <div class="bot-info">
                <h3>🎯 Команды бота</h3>
                <ul>
                    <li><code>/start</code> - Начать разговор</li>
                    <li><code>/cancel</code> - Отменить разговор</li>
                </ul>
            </div>
            
            <div class="status">
                <h3>🔧 Техническая информация</h3>
                <p><strong>Веб-сервер:</strong> Flask</p>
                <p><strong>Python версия:</strong> 3.9</p>
                <p><strong>Переменные окружения:</strong> BOT_TOKEN</p>
            </div>
        </div>
    </body>
    </html>
    '''

@app.route('/health')
def health():
    """Эндпоинт для проверки здоровья сервиса"""
    return jsonify({"status": "healthy", "bot": "running"})

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook для Telegram"""
    try:
        update_data = request.get_json()
        update = Update.de_json(update_data, telegram_app.bot)
        telegram_app.process_update(update)
        return jsonify({"status": "ok"})
    except Exception as e:
        logging.error(f"Webhook error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Запускаем бота в фоновом режиме
    import threading
    def run_bot():
        telegram_app.run_polling()
    
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Запускаем веб-сервер
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False) 