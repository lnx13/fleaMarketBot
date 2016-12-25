#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import Table, Column, Integer, String, Boolean, MetaData, or_
from sqlalchemy import create_engine
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.sql.sqltypes import BigInteger

import config
from log import *
from models.Item import Item
from models.Subscription import Subscription


class database(object):
    """database class for store items, object should be created before use item"""
    Session = ''

    def __init__(self):
        if not database.Session:
            engine = create_engine(config.db, echo=True)
            metadata = MetaData()
            items_table = Table(
                'items', metadata,
                Column('id', Integer, primary_key=True),
                Column('itemName', String),
                Column('itemDescription', String),
                Column('itemPhoto', String),
                Column('userID', Integer),
                Column('username', String),
                Column('ts', Integer),
                Column('is_active', Boolean, default=True)
            )
            subscriptions_table = Table(
                'subscriptions', metadata,
                Column('chatID', BigInteger, primary_key=True),
            )
            metadata.create_all(engine)
            mapper(Item, items_table)
            mapper(Subscription, subscriptions_table)
            database.Session = sessionmaker(bind=engine, autocommit=True)
        self.session = database.Session()
        self.item = ItemRepository(self.session)
        self.subscription = SubscriptionRepository(self.session)

    def __del__(self):
        logger.info("del db object")
        self.session.close()


class ItemRepository:
    session = None

    def __init__(self, session):
        self.session = session

    def get(self,
            id=None,
            ts=False,
            userID=None,
            is_active=True,
            username=None,
            text_like=None,
            orderBy=None,
            limit=None,
            all=True):
        """
        :type ts: int|bool starting timestamp
        """
        query = self.session.query(Item)

        if id:          query = query.filter(Item.id == id)
        if userID:      query = query.filter(Item.userID == userID)
        if ts:          query = query.filter(Item.ts >= ts)
        if username:    query = query.filter(Item.username == username)
        if is_active:   query = query.filter(Item.is_active == is_active)
        if text_like:
            query = query.filter(
                or_(
                    Item.itemName.like('%' + text_like + '%'),
                    Item.itemDescription.like('%' + text_like + '%')
                )
            )

        if orderBy is not None:     query = query.order_by(orderBy)

        if limit:       query = query.limit(limit)

        if all:
            return query.all()
        else:
            return query.one_or_none()

    def save(self, item):
        self.session.add(item)
        self.session.flush()


class SubscriptionRepository:
    session = None

    def __init__(self, session):
        self.session = session

    def get(self, chatID=None, all=True, return_query=False):
        query = self.session.query(Subscription)

        if chatID:      query = query.filter(Subscription.chatID == chatID)

        if return_query: return query

        if all:
            return query.all()
        else:
            return query.one_or_none()

    def save(self, subscription):
        self.session.add(subscription)
        self.session.flush()

    def unsubscribe(self, chatID):
        self.get(chatID=chatID, return_query=True).delete()
        self.session.flush()
