#!/usr/bin/env python
# -*- coding: utf-8 -*-

import config
from item import Item
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey


class database(object):
    def __init__(self):
        engine = create_engine(config.db, echo=True)
        metadata = MetaData()
        items_table = Table('items', metadata,
            Column('id', Integer, primary_key=True),
            Column('itemName', String),
            Column('itemDescription', String),
            Column('itemPhoto', String),
            Column('userID',String),
            Column('ts', Integer)
        )
        metadata.create_all(engine)
        mapper(Item, items_table)
        Session = sessionmaker(bind=engine)
