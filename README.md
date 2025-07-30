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

### Деплой на Vercel (Amvera)

1. Установите Vercel CLI:
```bash
npm install -g vercel
```

2. Войдите в аккаунт Vercel:
```bash
vercel login
```

3. Деплойте проект:
```bash
vercel --prod
```

4. Установите переменную окружения `BOT_TOKEN` в настройках Vercel

5. Настройте webhook:
```bash
python setup_webhook.py set https://your-vercel-domain.vercel.app/api/bot
```

## Структура проекта

- `bot.py` - основной файл бота (локальный запуск)
- `api/bot.py` - веб-функция для Vercel
- `config.py` - конфигурация (токен бота)
- `requirements.txt` - зависимости проекта
- `setup_webhook.py` - скрипт для настройки webhook
- `vercel.json` - конфигурация для Vercel
- `README.md` - документация

## Функции

- `/start` - начать разговор
- `/cancel` - отменить разговор 