import time


class Subscription:
    """Subscription class"""

    def __init__(self, chatID):
        """Init item object and add it to class"""
        self.chatID = chatID
        self.ts = int(time.time())
