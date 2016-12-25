import time

from db import database
from models.Subscription import Subscription


def activate(bot, update):
    chatID = update.message.chat_id

    if database().subscription.get(chatID=chatID, all=False):
        update.message.reply_text('Подписка уже активна. Скажи /unsubscribe, чтобы отписаться')
        return

    subscription = Subscription(chatID)
    database().subscription.save(subscription)
    update.message.reply_text('Подписка активирована. При добавлении нового объявления другим учатником, ты получишь '
                              'уведомление в этом чате и сможешь забрать крутую штукень первым!'
                              '\n\nЕсли уведомления тебе станут неинтересными - скажи /unsubscribe, чтобы отписаться.')


def deactivate(bot, update):
    chatID = update.message.chat_id

    subscription = database().subscription.get(chatID=chatID, all=False)
    if not subscription: update.message.reply_text('Это странно, но ты и так не подписан.')

    database().subscription.unsubscribe(chatID)
    update.message.reply_text('Подписка деактивировна. Надеюсь, ты нашел всё, чего тебе не хватало!'
                              '\n\nЕсли соскучишься за новыми штуками - скажи /subscribe, я снова буду тебе спамить :)')


class Notifier:
    """
    Sends notifications to the subscribed users
    """

    def __init__(self, bot, item, rate_per_second=20):
        """

        :type item: models.Item.Item
        :type bot: telegram.bot.Bot
        """
        self.bot = bot
        self.item = item
        self.rate_per_second = rate_per_second

    def run(self):
        subscribers = self.get_subscribers()
        self.spam(subscribers)

    def get_subscribers(self):
        return database().subscription.get()

    def spam(self, subscribers):
        count = 0
        item = self.item
        bot = self.bot

        for subscriber in subscribers:
            count += 1
            if count % self.rate_per_second == 0: time.sleep(1)
            if item.get_photo():
                if item.decorator().is_info_short():
                    bot.send_photo(subscriber.chatID, item.get_photo(), caption=item.decorator().get_info(separator='\n'))
                    continue
                bot.send_photo(subscriber.chatID, item.get_photo())

            bot.send_message(subscriber.chatID, item.decorator().get_info(separator='\n'))
