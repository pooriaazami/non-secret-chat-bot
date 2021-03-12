import logging
from datetime import datetime
from idlelib.iomenu import encoding
from threading import Timer

import schedule
from telegram.ext import Updater, Dispatcher, CommandHandler, MessageHandler, Filters, CallbackQueryHandler

from utils.CommandHandlers import start, link, inbox, cancel
from utils.MessageHandlers import text_message_handler, inbox_keyboard

# token = '1600237318:AAGNe51T9bY-08uwPSA9v80ewkPsREkR3hM'  # test


token = '1623432939:AAGo8LPXw5gwARFW8FriC8kNdbSf1IlORwk'  # prime


def main():
    path = r".\logs\%s.log" % (str(datetime.now()).replace(":", "-"))
    file = open(path, 'w')
    file.write('File created')
    file.close()
    logging.basicConfig(filename=path, level=logging.DEBUG)

    logging.info('Bot started')
    updater: Updater = Updater(token=token, use_context=True)
    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('link', link))
    dispatcher.add_handler(CommandHandler('inbox', inbox))
    dispatcher.add_handler(CommandHandler('cancel', cancel))

    dispatcher.add_handler(MessageHandler(
        ~Filters.command, text_message_handler))
    dispatcher.add_handler(CallbackQueryHandler(inbox_keyboard))

    updater.start_polling()


if __name__ == '__main__':
    main()
