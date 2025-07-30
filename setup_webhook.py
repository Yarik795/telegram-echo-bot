#!/usr/bin/env python3
"""
Скрипт для настройки webhook Telegram бота
"""
import os
import requests
import sys

# Получаем токен из переменной окружения или используем дефолтный
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7052592700:AAEzgL-EsnETAuXhJZPBA6vSLHXgxkKIeOU')

def get_bot_info():
    """Получаем информацию о боте"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getMe"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"❌ Ошибка получения информации о боте: {response.text}")
        return None

def delete_webhook():
    """Удаляем webhook"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    response = requests.post(url)
    if response.status_code == 200:
        print("✅ Webhook удален")
        return True
    else:
        print(f"❌ Ошибка удаления webhook: {response.text}")
        return False

def set_webhook(webhook_url):
    """Устанавливаем webhook"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {
        'url': webhook_url,
        'allowed_updates': ['message', 'callback_query']
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print(f"✅ Webhook установлен: {webhook_url}")
            return True
        else:
            print(f"❌ Ошибка установки webhook: {result.get('description')}")
            return False
    else:
        print(f"❌ Ошибка запроса: {response.text}")
        return False

def get_webhook_info():
    """Получаем информацию о текущем webhook"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['result']
    else:
        print(f"❌ Ошибка получения информации о webhook: {response.text}")
        return None

def main():
    print("🤖 Настройка webhook для Telegram бота")
    print("=" * 50)
    
    # Получаем информацию о боте
    bot_info = get_bot_info()
    if bot_info:
        print(f"📱 Бот: @{bot_info['username']} ({bot_info['first_name']})")
    
    # Показываем текущий webhook
    webhook_info = get_webhook_info()
    if webhook_info and webhook_info.get('url'):
        print(f"🔗 Текущий webhook: {webhook_info['url']}")
    else:
        print("🔗 Webhook не установлен")
    
    print("\nВыберите действие:")
    print("1. Установить webhook")
    print("2. Удалить webhook")
    print("3. Показать информацию о webhook")
    print("4. Выход")
    
    choice = input("\nВведите номер (1-4): ").strip()
    
    if choice == "1":
        # Запрашиваем URL для webhook
        print("\n📝 Введите URL для webhook:")
        print("Пример: https://ваш-домен.amvera.ru/webhook")
        webhook_url = input("URL: ").strip()
        
        if webhook_url:
            # Сначала удаляем старый webhook
            delete_webhook()
            # Устанавливаем новый
            set_webhook(webhook_url)
        else:
            print("❌ URL не может быть пустым")
    
    elif choice == "2":
        delete_webhook()
    
    elif choice == "3":
        webhook_info = get_webhook_info()
        if webhook_info:
            print(f"\n📋 Информация о webhook:")
            print(f"URL: {webhook_info.get('url', 'Не установлен')}")
            print(f"Последняя ошибка: {webhook_info.get('last_error_message', 'Нет')}")
            print(f"Последнее обновление: {webhook_info.get('last_error_date', 'Нет')}")
            print(f"Количество обновлений: {webhook_info.get('pending_update_count', 0)}")
    
    elif choice == "4":
        print("👋 До свидания!")
        sys.exit(0)
    
    else:
        print("❌ Неверный выбор")

if __name__ == "__main__":
    main() 