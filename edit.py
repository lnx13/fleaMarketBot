#!/usr/bin/env python
# -*- coding: utf-8 -*-

from db import database


def list_available(bot, update):
    items = database().get_by_userID(update.message.from_user.id)

    lines = []
    i = 0
    for item in items:
        lines.append('/%s - %s' % (++i, item.decorator().get_short_info(60)))

    update.message.reply_text('\n'.join(lines))
