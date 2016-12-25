from db import database


def delete_item(bot, update, groups):
    # todo: спросить, уверен ли
    id = groups[0]
    item = database().item.get(id=id, userID=update.message.from_user.id, all=False)
    if item is None:
        update.message.reply_text('Товар с идентификатором "%s" не найден' % id)
        return

    item.is_active = False
    update.message.reply_text('Товар "%s" был удалён' % item.decorator().get_title())
    database().item.save(item)


def list_items(bot, update):
    items = database().item.get(userID=update.message.from_user.id)
    if len(items) == 0:
        update.message.reply_text('У тебя нет активных товаров. Хочешь создать? Пиши /add')
        return

    send_items(update, items)


def send_items(update, items):
    result = []
    for item in items:
        result.append('%s: %s' % ('/delete%s' % item.id, item.decorator().get_title()))

    update.message.reply_text('\n'.join(result))
