import requests
import os

# Получаем токен из переменной окружения или используем дефолтный
BOT_TOKEN = os.environ.get('BOT_TOKEN', '7052592700:AAEzgL-EsnETAuXhJZPBA6vSLHXgxkKIeOU')

def set_webhook(url):
    """Устанавливает webhook для бота"""
    webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    data = {
        'url': url,
        'allowed_updates': ['message']
    }
    
    response = requests.post(webhook_url, json=data)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print(f"✅ Webhook успешно установлен: {url}")
            return True
        else:
            print(f"❌ Ошибка установки webhook: {result.get('description')}")
            return False
    else:
        print(f"❌ Ошибка HTTP: {response.status_code}")
        return False

def delete_webhook():
    """Удаляет webhook"""
    webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
    response = requests.post(webhook_url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            print("✅ Webhook успешно удален")
            return True
        else:
            print(f"❌ Ошибка удаления webhook: {result.get('description')}")
            return False
    else:
        print(f"❌ Ошибка HTTP: {response.status_code}")
        return False

def get_webhook_info():
    """Получает информацию о текущем webhook"""
    webhook_url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
    response = requests.get(webhook_url)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('ok'):
            webhook_info = result.get('result', {})
            if webhook_info.get('url'):
                print(f"📡 Текущий webhook: {webhook_info['url']}")
            else:
                print("📡 Webhook не установлен")
            return webhook_info
        else:
            print(f"❌ Ошибка получения информации: {result.get('description')}")
            return None
    else:
        print(f"❌ Ошибка HTTP: {response.status_code}")
        return None

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "set" and len(sys.argv) > 2:
            url = sys.argv[2]
            set_webhook(url)
        elif command == "delete":
            delete_webhook()
        elif command == "info":
            get_webhook_info()
        else:
            print("Использование:")
            print("  python setup_webhook.py set <URL>  - установить webhook")
            print("  python setup_webhook.py delete     - удалить webhook")
            print("  python setup_webhook.py info       - показать информацию о webhook")
    else:
        print("Использование:")
        print("  python setup_webhook.py set <URL>  - установить webhook")
        print("  python setup_webhook.py delete     - удалить webhook")
        print("  python setup_webhook.py info       - показать информацию о webhook") 