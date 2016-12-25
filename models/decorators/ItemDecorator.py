class ItemDecorator(object):
    def __init__(self, item):
        self.item = item

    def get_short_info(self, maxlength=200, separator=None):
        """strips item to max length"""
        if self.is_info_short(maxlength = maxlength):
            return self.get_info(separator=separator)

        username = '... - %s' % self.get_user()
        return self.get_info(append_username=False, separator=separator)[:maxlength-len(username)] + username

    def get_info(self, append_username=True, separator=' - '):
        result = '%s%s%s' % (self.item.itemName, separator, self.item.itemDescription)
        if append_username: result += '%s%s' % (separator, self.get_user())

        return result

    def is_info_short(self, maxlength=200):
        return len(self.get_info()) <= maxlength

    def get_title(self):
        return self.item.itemName

    def get_user(self):
        return '@' + self.item.username