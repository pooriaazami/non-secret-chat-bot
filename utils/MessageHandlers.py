import datetime

from telegram import Update, Message
from telegram.ext import CallbackContext

from Models.Enums import NotifyModes
from Models.Message import MessageModel
from utils.CommandParser import command_parser
from utils.DatabaseInterface import read_user_by_id, insert_message, read_message_by_id, read_user_by_username
from utils.glob import tasks
from utils.task_manager import notify_user, generate_link


def message_processor(message, bot, user):
    if message.text is not None and message.text[0] == '@':
        res = read_user_by_username(message.text)

        if res is not None:
            bot.send_message(chat_id=user.telegram_id, text=generate_link(res.telegram_id))
        else:
            bot.send_message(chat_id=user.telegram_id, text='متاسفانه اطلاعات این کابر در دیتابیس ربات وجود ندارد😢😢')

        return

    if user.access > 1:
        args = message.text.split(' ')
        args[0] = args[0].lower()

        command_parser(bot, user, message, args)
    else:
        bot.send_message(chat_id=user.telegram_id, text='متوجه نشدم ☹️')


def process_message(message: Message, receiver_id, sender_id, replay_to_message_id):
    paths = ''
    if message.animation is not None:
        paths += f'animation:file_id={message.animation.file_id};'

    if message.audio is not None:
        paths += f'audio:file_id={message.audio.file_id};'

    if message.contact is not None:
        paths += f'contact:' \
                 f'firstname={message.contact.first_name}&' \
                 f'lastname={message.contact.last_name}&' \
                 f'phone={message.contact.phone_number}&' \
                 f'telegram_id={message.contact.user_id};'

    if message.dice is not None:
        paths += f'dice:val={message.dice.value}&emoji={message.dice.emoji};'

    if message.document is not None and message.animation is None:
        paths += f'document:file_id={message.document.file_id};'

    if message.photo is not None:
        for photo in message.photo:
            paths += f'photo:file_id={photo.file_id};'

    if message.sticker is not None:
        paths += f'sticker:file_id={message.sticker.file_id};'

    if message.video is not None:
        paths += f'video:file_id={message.video.file_id}'

    if message.voice is not None:
        paths += f'voice:file_id={message.voice.file_id};'

    if message.caption is not None:
        paths += f'caption:text={message.caption};'

    insert_message(MessageModel(
        database_id=-1,
        receiver_id=receiver_id,
        sender_id=sender_id,
        send_message_id=message.message_id,
        receive_message_id=-1,
        replay_to_message_id=replay_to_message_id,
        send_date=str(datetime.datetime.now()),
        text=message.text,
        paths=paths if len(paths) != 0 else 'None'
    ))


def text_message_handler(update: Update, context: CallbackContext):
    user = read_user_by_id(update.effective_user.id)

    if user.telegram_id in tasks.keys():
        data = tasks[user.telegram_id]

        process_message(update.message,
                        data['contact'].telegram_id,
                        user.telegram_id,
                        data.get('replay_id', 0))

        notify_user(context.bot, data['contact'], NotifyModes.RECEIVE_MESSAGE)
        del tasks[user.telegram_id]

        update.message.reply_text('پیام شما ارسال شد')

    else:
        message_processor(update.message, context.bot, user)


def inbox_keyboard(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    value = query.data

    if value == 'Answer':
        message = read_message_by_id(update.effective_user.id, query.message.message_id)

        user = read_user_by_id(message.sender_id)

        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text='پیام خود را وارد کنید:',
                                 reply_to_message_id=query.message.message_id)

        tasks[update.effective_user.id] = {'contact': user, 'replay_id': message.send_message_id}
