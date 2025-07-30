# Telegram Echo Bot

Простой Telegram бот, написанный на Python с использованием библиотеки python-telegram-bot.

## Описание

Этот бот реализует простой диалог с пользователем:
- При команде `/start` бот спрашивает имя пользователя
- После ввода имени бот приветствует пользователя
- Команда `/cancel` позволяет отменить разговор

## Установка и запуск

### Локальный запуск

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Получите токен бота у @BotFather в Telegram

3. Замените токен в файле `config.py`:
```python
BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'
```

4. Запустите бота:
```bash
python bot.py
```

### Деплой на Amvera

1. Создайте проект на Amvera:
   - Зайдите на [Amvera.ru](https://amvera.ru)
   - Войдите в аккаунт
   - Создайте новый проект `ehobot`

2. Подключите репозиторий:
```bash
git remote add amvera https://git.amvera.ru/y31415/ehobot
```

3. Отправьте код на Amvera:
```bash
git push amvera master
```

4. Настройте переменные окружения в веб-интерфейсе Amvera:
   - `BOT_TOKEN` = `7052592700:AAEzgL-EsnETAuXhJZPBA6vSLHXgxkKIeOU`

5. Запустите деплой в веб-интерфейсе Amvera

## Структура проекта

- `bot.py` - основной файл бота (локальный запуск)
- `app.py` - основной файл для Amvera
- `api/bot.py` - веб-функция для Vercel
- `config.py` - конфигурация (токен бота)
- `requirements.txt` - зависимости проекта
- `setup_webhook.py` - скрипт для настройки webhook
- `amvera.yml` - конфигурация для Amvera
- `README.md` - документация

## Функции

- `/start` - начать разговор
- `/cancel` - отменить разговор 