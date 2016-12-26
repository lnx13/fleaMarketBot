from handlers.system import silence_keeper


@silence_keeper
def support(bot, update):
    update.message.reply_text(
        'Если я делаю что-то не так, или у тебя есть идеи, как можно сделать меня лучше - пиши создателям:\n\n'
        '@lnx13 - Михаил "Lynxie" Чичков\n'
        '@d_naumenko - Дмитрий Науменко\n'
    )
