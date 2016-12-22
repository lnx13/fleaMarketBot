#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from log import *
from item import Item
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, or_


class database(object):
    """database class for store items, objest should be created before use item"""
    Session=''

    def __init__(self):
        if not database.Session:
            engine = create_engine(config.db, echo=True)
            metadata = MetaData()
            items_table = Table('items', metadata,
                Column('id', Integer, primary_key=True),
                Column('itemName', String),
                Column('itemDescription', String),
                Column('itemPhoto', String),
                Column('userID',Integer),
                Column('username',String),
                Column('ts', Integer)
            )
            metadata.create_all(engine)
            mapper(Item, items_table)
            database.Session = sessionmaker(bind=engine)
        self.session = database.Session()

    def save_to_db(self, item):
        """save item to database"""
        self.session.add(item)
        self.session.commit()

    def get_by_userID(self, userID):
        """get all items by userID"""
        return self.session.query(Item).filter(Item.userID == userID).all()

    def get(self, ts=False):
        """
        :type ts: int|bool starting timestamp
        """
        query = self.session.query(Item)
        if (ts): query.filter(Item.ts >= ts)

        return query.all()


    def find(self, str):
        """find item by sting it name or description"""
        return self.session.query(Item).filter(or_(Item.itemName.like('%'+str+'%'), Item.itemDescription.like('%'+str+'%'))).all()

    def __del__(self):
        logger.info("del db object")
        self.session.close()