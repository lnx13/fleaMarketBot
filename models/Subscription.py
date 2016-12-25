import time


class Subscription:
    """Subscription class"""

    def __init__(self, userID, chatID):
        """Init item object and add it to class"""
        self.userID = userID
        self.chatID = chatID
        self.ts = int(time.time())
