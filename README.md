# Telegram Echo Bot

Простой Telegram бот, написанный на Python с использованием библиотеки python-telegram-bot.

## Описание

Этот бот реализует простой диалог с пользователем:
- При команде `/start` бот спрашивает имя пользователя
- После ввода имени бот приветствует пользователя
- Команда `/cancel` позволяет отменить разговор

## Установка и запуск

1. Установите зависимости:
```bash
pip install python-telegram-bot
```

2. Получите токен бота у @BotFather в Telegram

3. Замените токен в файле `bot.py`:
```python
application = Application.builder().token('YOUR_BOT_TOKEN').build()
```

4. Запустите бота:
```bash
python bot.py
```

## Структура проекта

- `bot.py` - основной файл бота
- `requirements.txt` - зависимости проекта
- `README.md` - документация

## Функции

- `/start` - начать разговор
- `/cancel` - отменить разговор 