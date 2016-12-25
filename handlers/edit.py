#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import database


def list_items(bot, update):
    update.message.reply_text('Редактирование пока не реализовано. Пока можно удалить товар и создать его заново.')