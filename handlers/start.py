from handlers.system import silence_keeper


@silence_keeper
def start(bot, update):
    update.message.reply_text('Хай! Я Барахолка-бот!\nНапиши /help, чтобы узнать о моих возможностях.')
