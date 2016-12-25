from db import database
from models.Subscription import Subscription


def activate(bot, update):
    userID = update.message.from_user.id
    chatID = update.message.chat_id

    if database().subscription.get(userID=userID, chatID=chatID, all=False):
        update.message.reply_text('Подписка уже активна. Скажи /unsubscribe, чтобы отписаться')
        return

    subscription = Subscription(userID, chatID)
    database().subscription.save(subscription)
    update.message.reply_text('Подписка активирована. При добавлении нового объявления другим учатником, ты получишь '
                              'уведомление в этом чате и сможешь забрать крутую штукень первым!'
                              '\n\nЕсли уведомления тебе станут неинтересными - скажи /unsubscribe, чтобы отписаться.')


def deactivate(bot, update):
    userID=update.message.from_user.id
    chatID=update.message.chat_id

    subscription = database().subscription.get(userID=userID, chatID=chatID, all=False)
    if not subscription: update.message.reply_text('Это странно, но ты и так не подписан.')

    database().subscription.unsubscribe(userID=userID, chatID=chatID)
    update.message.reply_text('Подписка деактивировна. Надеюсь, ты нашел всё, чего тебе не хватало!'
                              '\n\nЕсли соскучишься за новыми штуками - скажи /subscribe, я снова буду тебе спамить :)')


class Notifier:
    """
    Sends notifications to the subscribed users
    """
    def __init__(self, bot, item):
        """

        :type item: models.Item.Item
        :type bot: telegram.bot.Bot
        """
        self.bot = bot
        self.item = item

    def run(self):
        subscribers = self.get_subscribers()
        self.spam(subscribers)

    def get_subscribers(self):
        return database().subscription.get()

    def spam(self, subscribers):
        item = self.item
        bot = self.bot

        for subscriber in subscribers:
            if item.get_photo():
                if item.decorator().is_info_short():
                    return bot.send_photo(subscriber.chatID, item.get_photo(), caption=item.decorator().get_info(separator='\n'))

                bot.send_photo(subscriber.chatID, item.get_photo())

            bot.send_message(subscriber.chatID, item.decorator().get_info(separator='\n'))
