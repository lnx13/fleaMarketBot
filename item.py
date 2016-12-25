#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from telegram.user import User

class ItemDecorator(object):
    def __init__(self, item):
        self.item = item

    def get_short_info(self, maxlength=200, separator=None):
        """strips item to max length"""
        if self.is_info_short(maxlength = maxlength):
            return self.get_info(separator=separator)

        username = '... - %s' % self.get_user()
        return self.get_info(append_username=False, separator=separator)[:maxlength-len(username)] + username

    def get_info(self, append_username=True, separator=' - '):
        result = '%s%s%s' % (self.item.itemName, separator, self.item.itemDescription)
        if append_username: result += '%s%s' % (separator, self.get_user())

        return result

    def is_info_short(self, maxlength=200):
        return len(self.get_info()) <= maxlength

    def get_title(self):
        return self.item.itemName

    def get_user(self):
        return '@' + self.item.username


class Item(object):
    """Item class"""

    def __init__(self, userID, username):
        """Init item object and add it to class"""
        self.itemName = ''
        self.itemDescription = ''
        self.itemPhoto = ''
        self.userID = userID
        self.username = username
        self.ts = int(time.time())
        self.is_active = True

    def add_name(self, name):
        """add item name to object"""
        self.itemName = name

    def add_description(self, description):
        """add item description to object"""
        self.itemDescription = description

    def add_photo(self, photo):
        '''add item photo to object'''
        self.itemPhoto = photo

    def get_photo(self):
        '''get photo id'''
        return self.itemPhoto

    def get_ts(self):
        return self.ts

    def update_ts(self):
        self.ts = int(time.time())

    def __str__(self):
        """convert item to string"""
        return self.itemName + '\n' + self.itemDescription

    def decorator(self):
        return ItemDecorator(self)


class Items(object):
    '''Items temporary storage class'''

    # {userID: itemObject}
    __items = {}

    @classmethod
    def create_item(cls, userID, username):
        Items.__items[userID] = Item(userID, username)

    @classmethod
    def add_name(cls, userID, name):
        cls.__items[userID].add_name(name)

    @classmethod
    def add_description(cls, userID, description):
        cls.__items[userID].add_description(description)

    @classmethod
    def add_photo(cls, userID, photo):
        cls.__items[userID].add_photo(photo)

    @classmethod
    def get_photo(cls, userID):
        cls.__items[userID].get_photo()

    @classmethod
    def get_item(cls, userID):
        return cls.__items[userID]

    @classmethod
    def del_item(cls, userID):
        '''del item object from class and return it'''
        obj = cls.__items[userID]
        del cls.__items[userID]
        return obj
