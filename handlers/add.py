#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import desc
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler

from db import database
from log import *
from models.Item import Items, Item
from handlers.subscription import Notifier

# add item conversation
NAME, DESCRIPTION, PHOTO, PUBLISH = range(4)


def pre_publish(bot, update):
    """check item before publish"""
    user = update.message.from_user
    reply_keyboard = [['/publish', '/cancel', ]]
    update.message.reply_text('Все верно?\n' + str(Items.get_item(user.id)),
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))


def add(bot, update, user_data):
    """

    :type update: telegram.Update
    """
    user_data['base'] = database()
    user = update.message.from_user
    update.message.reply_text(
        'Чтобы добавить товар на продажу, напишите его название. Если передумали, в любой момент можно написать /cancel',
        reply_markup=ReplyKeyboardRemove())
    Items.create_item(user.id, user.username)

    return NAME


def name(bot, update):
    """add item name"""
    user = update.message.from_user
    itemName = update.message.text
    logger.info("Item name: %s" % (itemName))
    Items.add_name(user.id, itemName)

    update.message.reply_text('Отлично! Теперь напишите описание товара. Не забудьте указать количество и цену!',
                              reply_markup=ReplyKeyboardRemove())

    return DESCRIPTION


def description(bot, update):
    """add item description"""
    reply_keyboard = [['/skip', ]]

    user = update.message.from_user
    itemDescription = update.message.text
    logger.info("Item description: %s" % (itemDescription))
    Items.add_description(user.id, itemDescription)

    update.message.reply_text('Последний шаг. Отправте фото товара, или нажмите "skip", чтобы пропустить фото.',
                              reply_markup=ReplyKeyboardMarkup(
                                  reply_keyboard,
                                  one_time_keyboard=True,
                                  resize_keyboard=True
                              ))

    return PHOTO


def photo(bot, update):
    """add item photo"""
    user = update.message.from_user
    photo_id = update.message.photo[-1].file_id
    logger.info("Item photo id from %s: %s" % (user.first_name, photo_id))
    Items.add_photo(user.id, photo_id)

    pre_publish(bot, update)

    return PUBLISH


def skip_photo(bot, update):
    """if item without photo"""
    user = update.message.from_user
    logger.info("User %s doesnt add item photo :(" % (user.first_name,))

    pre_publish(bot, update)

    return PUBLISH


def cancel(bot, update, user_data):
    """interupt adding"""
    user = update.message.from_user
    del user_data['base']
    logger.info("User %s cancel :(" % (user.first_name,))
    Items.del_item(user.id)
    update.message.reply_text('Окей, отменил.', reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def publish(bot, update, user_data):
    """publish item"""
    user = update.message.from_user
    item = Items.del_item(user.id)
    user_data['base'].item.save(item)
    del user_data['base']
    update.message.reply_text('Товар добавлен!', reply_markup=ReplyKeyboardRemove())

    newItem = database().item.get(userID=update.message.from_user.id, orderBy=desc(Item.id), limit=1, all=False)
    Notifier(bot, newItem).run()

    return ConversationHandler.END
