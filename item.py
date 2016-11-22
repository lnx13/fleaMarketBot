#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Item(object):
    '''Item class'''


    def __init__(self, userID):
        '''Init item object and add it to class'''
        self.__itemName = ''
        self.__itemDescription = ''
        self.__itemPhoto = ''
        self.__userID = userID


    def add_name(self, name):
        '''add item name to object'''
        self.__itemName = name

    def add_description(self, description):
        '''add item description to object'''
        self.__itemDescription = description

    def add_photo(self, photo):
        '''add item photo to object'''
        self.__itemPhoto = photo

    def get_photo(self):
        '''get photo id'''
        return self.__itemPhoto

    def __str__(self):
        '''convert item to string'''
        return self.__itemName + '\n' + self.__itemDescription

class Items(object):
    '''Items storage class'''

    # {userID: itemObject}
    __items = {}

    @classmethod
    def create_item(cls, userID):
        Items.__items[userID] = Item(userID)

    @classmethod
    def add_name(cls, userID, name):
        cls.__items[userID].add_name(name)

    @classmethod
    def add_description(cls,userID, description):
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





