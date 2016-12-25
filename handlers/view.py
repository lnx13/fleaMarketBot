from db import database


def item(bot, update, groups):
    id = groups[0]
    item = database().item.get(id=id, all=False)
    if item is None:
        update.message.reply_text('Товар с идентификатором "%s" не найден' % id)
        return

    respond_item(update, item)


def all_items(bot, update):
    items = database().item.get()
    if len(items) == 0:
        update.message.reply_text('Нет ни одного товара')
        return

    for item in items:
        respond_item(update, item)


def respond_item(update, item):
    if item.get_photo():
        if item.decorator().is_info_short():
            return update.message.reply_photo(item.get_photo(), caption=item.decorator().get_info(separator='\n'))
        update.message.reply_photo(item.get_photo())

    update.message.reply_text(item.decorator().get_info(separator='\n'))
