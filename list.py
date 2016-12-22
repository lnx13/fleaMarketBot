#!/usr/bin/env python
# -*- coding: utf-8 -*-
import telegram

from db import database


def all(bot, update):
    """

    :type update: telegram.Update
    """
    items = database().get()
    for item in items:
        reply_item(update, item)


def reply_item(update, item):
    if (item.itemPhoto):
        update.message.reply_photo(item.itemPhoto)
    update.message.reply_text('%s - %s - %s' % (item.itemName, item.itemDescription, item.getUser()))
