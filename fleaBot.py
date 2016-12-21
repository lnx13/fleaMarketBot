#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flea market bot
"""

from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, Filters, InlineQueryHandler
from log import *
import add
import list
import config
import help
import edit

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    """bot /start functions"""
    update.message.reply_text('Хай! Я Барахолка-бот!\nНапиши /help, чтобы узнать о моих возможностях.')

# def help(bot, update):
#     update.message.reply_text(
#         '/add - добавить товар\n'
#         '/list - показать все товары, которые сейчас продаются\n'
#         '/subscribe - подписаться на новые товары'
#     )

def subscribe(bot, update):
    update.message.reply_text('Меня этому еще не научили ' u'\U0001F614' ' Попробуй позже')

def stilli(bot, update):
    update.message.reply_text('Стилли аццтой!(с)')

def main():
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Simple commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("list", list.all))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(RegexHandler(u'.*(С|с)тил{1,2}и.*', stilli))

    #Add item
    add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add.add, pass_user_data=True)],

        states={
            add.NAME: [MessageHandler(Filters.text, add.name)],
            add.DESCRIPTION: [MessageHandler(Filters.text, add.description)],
            add.PHOTO: [MessageHandler(Filters.photo, add.photo),
                    RegexHandler(u'^пропустить$', add.skip_photo)],
            add.PUBLISH: [CommandHandler(u'добавить', add.publish, pass_user_data=True),],
        },

        fallbacks=[CommandHandler(u'отмена', add.cancel, pass_user_data=True)]
    )

    dp.add_handler(add_handler)

    #Del item

    #Edit item
    dp.add_handler(CommandHandler("edit", edit.list_available))

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