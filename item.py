#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from telegram.user import User


class ItemDecorator(object):
    def __init__(self, item):
        self.item = item

    def shortInfo(self, maxlength=200):
        """strips item to max length"""
        username = ' - %s' % self.getUser()
        targetLength = maxlength - len(username)
        shortInfo = ('%s - %s' % (self.item.itemName, self.item.itemDescription))
        if len(shortInfo) > targetLength:
            return shortInfo[:targetLength - 3] + '...' + username

        return shortInfo + username

    def getUser(self):
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
