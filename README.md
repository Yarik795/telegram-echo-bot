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

1. Подключите ваш GitHub репозиторий к Amvera:
   - Зайдите на [Amvera.app](https://amvera.app)
   - Войдите в аккаунт
   - Нажмите "New Project"
   - Выберите ваш репозиторий `telegram-echo-bot`

2. Настройте переменные окружения:
   - В настройках проекта добавьте переменную `BOT_TOKEN`
   - Установите значение вашего токена бота

3. Деплойте проект:
   - Amvera автоматически задеплоит проект при пуше в GitHub
   - Или нажмите "Deploy" в веб-интерфейсе

4. Настройте webhook:
```bash
python setup_webhook.py set https://your-project.amvera.app/api/bot
```

## Структура проекта

- `bot.py` - основной файл бота (локальный запуск)
- `api/bot.py` - веб-функция для Vercel
- `config.py` - конфигурация (токен бота)
- `requirements.txt` - зависимости проекта
- `setup_webhook.py` - скрипт для настройки webhook
- `amvera.json` - конфигурация для Amvera
- `README.md` - документация

## Функции

- `/start` - начать разговор
- `/cancel` - отменить разговор 