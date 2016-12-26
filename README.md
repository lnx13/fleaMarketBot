# fleaMarketBot
Telegram flea market bot for Ukraine FPV group

Bot framework https://github.com/python-telegram-bot/python-telegram-bot

# How to start

## Окружение

Создать `db.py`:


```python
# Telegram API token. Напишите @BotFather, чтобы получить
token = ''

# DSN строка для подключения к БД
db = 'sqlite:/path/to/database/file'

# Список идентификаторов чатов, в которых бот всегда будет предлагать общаться в ЛС
silent_chats = []
```

## Register bot commands in BotFather

```
/setcommands

help - показать это сообщение
list - показать список из названий товаров, которые сейчас продаются
subscribe - подписаться на новые товары
unsubscribe - отписаться от рассылки новых товаров
add - добавить свой товар
edit - отредактировать свой товар
delete - удалить свой товар
support - спросить поддержку
```


# Roadmap

 - Регулярная проверка актуальности
 - Улучшить дизайн сообщений, возможно применить Markdown
 - Банлист
