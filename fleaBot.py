#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Flea market bot
"""

import add
from telegram.ext import Updater, CommandHandler, RegexHandler, ConversationHandler, MessageHandler, Filters
from log import *
import config



def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def start(bot, update):
    '''bot /start functions'''
    update.message.reply_text('Хай! Я Барахолка-бот')

def stilli(bot, update):
    update.message.reply_text('Стилли аццтой!(с)')


def main():
    updater = Updater(config.token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Simple commands
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", start))
    dp.add_handler(RegexHandler(u'.*(С|с)тил{1,2}и.*', stilli))

    #Add item
    add_handler = ConversationHandler(
        entry_points=[CommandHandler('add', add.add)],

        states={
            add.NAME: [MessageHandler(Filters.text, add.name)],
            add.DESCRIPTION: [MessageHandler(Filters.text, add.description)],
            add.PHOTO: [MessageHandler(Filters.photo, add.photo),
                    RegexHandler(u'^пропустить$', add.skip_photo)],
            add.PUBLISH: [CommandHandler(u'добавить', add.publish),],
        },

        fallbacks=[CommandHandler(u'отмена', add.cancel)]
    )

    dp.add_handler(add_handler)
    #Del item

    #Edit item


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