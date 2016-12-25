#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flea market bot
"""
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, Filters

import config
from handlers import add, edit, list, subscription, help, delete, view, start, jokes, support
from log import *


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Базовые команды
    dp.add_handler(CommandHandler("start", start.start))
    dp.add_handler(CommandHandler("help", help.help))

    # Просмотр
    dp.add_handler(CommandHandler("list", list.all))
    #dp.add_handler(CommandHandler("view", view.all_items)) # so many messages
    dp.add_handler(RegexHandler('^\/view(\d+).*', view.item, pass_groups=True))

    # Подписка
    dp.add_handler(CommandHandler("subscribe", subscription.activate))
    dp.add_handler(CommandHandler("unsubscribe", subscription.deactivate))

    # Добавление
    dp.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', add.add, pass_user_data=True)],

        states={
            add.NAME: [MessageHandler(Filters.text, add.name)],
            add.DESCRIPTION: [MessageHandler(Filters.text, add.description)],
            add.PHOTO: [MessageHandler(Filters.photo, add.photo), CommandHandler('skip', add.skip_photo)],
            add.PUBLISH: [CommandHandler('publish', add.publish, pass_user_data=True), ],
        },

        fallbacks=[CommandHandler(u'cancel', add.cancel, pass_user_data=True)]
    ))

    # Редактирование
    dp.add_handler(CommandHandler("edit", edit.list_items))

    edit_handler = ConversationHandler(
        entry_points=[RegexHandler('^/edit(\d+).*', edit.edit, pass_groups=True, pass_user_data=True)],

        states={
            edit.NAME: [MessageHandler(Filters.text, edit.name, pass_user_data=True),
                        CommandHandler('skip', edit.skip_name, pass_user_data=True)],

            edit.DESCRIPTION: [MessageHandler(Filters.text, edit.description, pass_user_data=True),
                        CommandHandler('skip', edit.skip_description, pass_user_data=True)],

            edit.PHOTO: [MessageHandler(Filters.photo, edit.photo, pass_user_data=True),
                        CommandHandler('skip', edit.skip_photo, pass_user_data=True)],

            edit.PUBLISH: [CommandHandler('save', edit.publish, pass_user_data=True), ],
        },

        fallbacks=[CommandHandler('cancel', edit.cancel, pass_user_data=True)]
    )
    dp.add_handler(edit_handler)

    # Удаление
    dp.add_handler(CommandHandler("delete", delete.list_items))
    dp.add_handler(RegexHandler(u'^\/delete(\d+).*', delete.delete_item, pass_groups=True))

    # Другое
    dp.add_handler(RegexHandler(u'.*(С|с)тил{1,2}и.*', jokes.stilli))
    dp.add_handler(CommandHandler("support", support.support))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()