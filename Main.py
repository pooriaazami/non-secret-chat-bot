import logging
import logging.handlers as handlers

from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from utils.CommandHandlers import start, link, inbox, cancel, help_command
from utils.MessageHandlers import text_message_handler, inbox_keyboard

token = 'your-token'  # test

def main():
    logger = logging.getLogger('sercet_chat_bot')
    log_handler = handlers.TimedRotatingFileHandler('bot.log', when='D', interval=1, backupCount=2)
    logger.setLevel(logging.INFO)
    logger.addHandler(log_handler)

    updater: Updater = Updater(token=token, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('link', link))
    dispatcher.add_handler(CommandHandler('inbox', inbox))
    dispatcher.add_handler(CommandHandler('cancel', cancel))
    dispatcher.add_handler(CommandHandler('help', help_command))

    dispatcher.add_handler(MessageHandler(~Filters.command, text_message_handler))
    dispatcher.add_handler(CallbackQueryHandler(inbox_keyboard))

    updater.start_polling()


if __name__ == '__main__':
    main()
