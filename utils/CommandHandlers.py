from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from Models.User import UserModel
from utils.DatabaseInterface import read_user_by_id, insert_user, read_messages, mark_messages_as_read
from utils.glob import tasks
from utils.task_manager import generate_link, send_advance_message, FfgEncryption


def start(update: Update, context: CallbackContext):
    user = read_user_by_id(update.effective_user.id)

    if not user:
        user = UserModel(telegram_id=update.effective_user.id,
                         firstname=update.effective_user.first_name,
                         lastname=update.effective_user.last_name,
                         username=update.effective_user.username)
        insert_user(user)

    if context.args:
        cryptographer = FfgEncryption()
        contact = read_user_by_id(cryptographer.decode(context.args[0]))
        if user.telegram_id in tasks.keys():
            update.message.reply_text(
                f"شما در حال ارسال پیام به {tasks[user.telegram_id]['contact'].firstname} هستید. اگر میخواهید به شخص "
                f"دیگری پیام دهید باید ابتدا فرایند قبلی را با دستور /cancel متوقف کنید")
        elif contact is None:
            update.message.reply_text('لینک وارد شده اشتباه است😢')
        elif contact.telegram_id == update.effective_user.id:
            update.message.reply_text('😐')
            update.message.reply_text('شما نمیتوانید به خودتان پیام دهید')
        else:
            tasks[user.telegram_id] = {'contact': contact}
            update.message.reply_text(
                f'شما در حال ارسال پیام به {contact.firstname} هستید ')
            update.message.reply_text('اگر پشیمون شدی /cancel رو بزن')

    else:
        update.message.reply_text('به ربات پیام ناشناس خوش آمدید😃')
        update.message.reply_text('با استفاده از این بات میتونی به هر کسی که عضو ربات شده باشه به صورت ناشناس پیام '
                                  'بدی و راحت باهاش حرف بزنی بدون اینکه متوجه بشه کی بهش پیام داده اگه میخوای لینک '
                                  'ناشناس یک آدم خاص رو پیدا کنی آیدیشو برای بات بفرست، اگه عضو باشه لینکش برات میاد '
                                  'برای اینکه پیام هایی که برات اومده رو ببینی باید دستور /inbox رو استفاده کنی')


def link(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text=generate_link(update.effective_user.id))


def create_inbox_keyboard():
    keyboard = [
        [
            InlineKeyboardButton('پاسخ', callback_data='Answer'),
        ]
    ]

    return InlineKeyboardMarkup(keyboard)


def inbox(update: Update, context: CallbackContext):
    messages = read_messages(update.effective_user.id)
    user = read_user_by_id(update.effective_user.id)

    if len(messages) == 0:
        update.message.reply_text("هیچ پیامی در صندوق پستی شما وجود ندارد.😢")
    else:
        for row in messages:
            res = send_advance_message(
                row.text,
                row.paths,
                create_inbox_keyboard(),
                row.replay_to_message_id,
                user,
                context.bot
            )

        mark_messages_as_read(messages, context.bot, user, res)


def cancel(update: Update, context: CallbackContext):
    user = read_user_by_id(update.effective_user.id)

    if user.telegram_id in tasks.keys():
        del tasks[user.telegram_id]

        update.message.reply_text('ارسال پیام لغو شد')


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text('با استفاده از این بات میتونی به هر کسی که عضو ربات شده باشه به صورت ناشناس پیام '
                              'بدی و راحت باهاش حرف بزنی بدون اینکه متوجه بشه کی بهش پیام داده اگه میخوای لینک '
                              'ناشناس یک آدم خاص رو پیدا کنی آیدیشو برای بات بفرست، اگه عضو باشه لینکش برات میاد '
                              'برای اینکه پیام هایی که برات اومده رو ببینی باید دستور /inbox رو استفاده کنی')
