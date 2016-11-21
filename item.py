#!/usr/bin/env python
# -*- coding: utf-8 -*-

class Item(object):
    '''Items class'''

    #{userID: itemObject}
    items={}

    def __init__(self, userID):
        '''Init item object and add it to class'''
        self.__itemName = ''
        self.__itemDescription = ''
        self.__itemPhoto = ''
        self.__userID = userID
        Item.items[userID] = self

    def add_name(self, name):
        '''add item name to object'''
        self.__itemName = name

    def add_description(self, description):
        '''add item description to object'''
        self.__itemDescription = description

    def add_photo(self, photo):
        '''add item photo to object'''
        self.__itemPhoto = photo

    def del_item(self):
        '''del item object from class and return it'''
        del Item.items[self.__userID]
        return self

    def __str__(self):
        '''convert item to string'''
        return self.__itemName + '\n' + self.__itemDescription