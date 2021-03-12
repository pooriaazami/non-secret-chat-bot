import datetime

from telegram import Bot, Message

from Models.User import UserModel
from utils.DatabaseInterface import read_user_by_id, read_user_by_username, edit_access, rewrite_user, \
    read_message_by_id
from utils.task_manager import generate_link


def hello(bot, user, message, args):
    bot.send_message(chat_id=user.telegram_id, text='سلام 😎😎😎')


def date(bot, user, message, args):
    bot.send_message(chat_id=user.telegram_id, text=str(datetime.datetime.now()))


def info(bot, active_user, message, args):
    if len(args) < 2:
        bot.send_message(chat_id=active_user.telegram_id,
                         text='لطفا دستور وارد شده را برسی کنید، همچین دستوری وجود ندارد')
        return

    if args[1].isnumeric():
        user = read_user_by_id(int(args[1]))
    else:
        user = read_user_by_username(args[1])

    if user is None:
        bot.send_message(chat_id=active_user.telegram_id, text='متاسفانه اطلاعات این کاربر در دیتابیس موجود نیست')
    else:
        text = f'firstname = {user.firstname}\n' \
               f'lastname= {user.lastname}\n' \
               f'telegram_id = {user.telegram_id}\n' \
               f'id = @{user.username}\n' \
               f'access = {user.access}\n' \
               f'link = {generate_link(user.telegram_id)}'

        bot.send_message(chat_id=active_user.telegram_id, text=text)


def edit_access_command(bot, active_user, message, args):
    if len(args) < 2:
        bot.send_message(chat_id=active_user.telegram_id, text='لطفا دستور وارد شده را برسی کنید')
        return
    if len(args) == 2:
        args.append(2)

    if args[1].isnumeric():
        user = read_user_by_id(int(args[1]))
    else:
        user = read_user_by_username(args[1])

    if user is None:
        bot.send_message(chat_id=active_user.telegram_id, text='متاسفانه اطلاعات این کاربر در دیتابیس موجود نیست')
    else:
        if active_user.access > user.access and 0 < int(args[2]) < active_user.access:
            if user.username == 'None':
                bot.send_message(chat_id=active_user.telegram_id, text='ادمین ها باید آیدی داشته باشند')
            else:

                edit_access(user, int(args[2]))

                bot.send_message(chat_id=active_user.telegram_id, text='انجام شد')
                bot.send_message(chat_id=user.telegram_id,
                                 text=f'دسترسی شما توسط @{active_user.username} به سطح  {args[2]} تغییر پیدا کرد.')
        else:
            bot.send_message(chat_id=active_user.telegram_id,
                             text='تاسفانه امکان تغییر دسترسی کاربر مورد نظر به این سطح وجود ندارد')


def update(bot, active_user, message, args):
    if len(args) < 2:
        bot.send_message(chat_id=active_user.telegram_id, text='لطفا دستور وارد شده را برسی کنید')
        return
    if len(args) == 2:
        args.append(2)

    if args[1].isnumeric():
        user = read_user_by_id(int(args[1]))
    else:
        user = read_user_by_username(args[1])

    if user is None:
        bot.send_message(chat_id=active_user.telegram_id, text='متاسفانه اطلاعات این کاربر در دیتابیس موجود نیست')
    else:
        res = bot.get_chat(chat_id=user.telegram_id)

        user.firstname = res.first_name
        user.lastname = res.last_name
        user.username = res.username

        rewrite_user(user)

        bot.send_message(chat_id=active_user.telegram_id, text='انجام شد')


def analyze(bot, user, message, args):
    if message.reply_to_message is None:
        bot.send_message(chat_id=user.telegram_id, text='باید پیام مورد نظر را با این دستور ریپلای کنید')
        return

    message = read_message_by_id(user.telegram_id, message.reply_to_message.message_id)
    if message is None:
        bot.send_message(chat_id=user.telegram_id,
                         text='پیام وارد شده را نمیتوان برسی کرد')
        return

    sender = read_user_by_id(message.sender_id)

    text = f'User information:\n' \
           f'telegram_id = {sender.telegram_id}\n' \
           f'firstname = {sender.firstname}\n' \
           f'lastname = {sender.lastname}\n' \
           f'username = @{sender.username}\n' \
           f'link = {generate_link(sender.telegram_id)}\n\n' \
           f'Message information:\n' \
           f'send date = {message.send_date}\n'

    bot.send_message(chat_id=user.telegram_id, text=text)


def who(bot, user, message, args):
    if message.reply_to_message is None:
        bot.send_message(chat_id=user.telegram_id, text='باید پیام مورد نظر را با این دستور ریپلای کنید')
        return

    message = read_message_by_id(user.telegram_id, message.reply_to_message.message_id)
    if message is None:
        bot.send_message(chat_id=user.telegram_id,
                         text='پیام وارد شده را نمیتوان برسی کرد')
        return

    bot.send_message(chat_id=user.telegram_id, text=str(message.sender_id))


def commands_list(bot, user, message, args):
    text = ""
    for command in commands.keys():
        text += command
        text += '\n'

    bot.send_message(chat_id=user.telegram_id,
                     text=text)


def help_command(bot, user, message, args):
    if len(args) < 2:
        commands_list(bot, user, message, args)
        return

    args[1] = args[1].lower()
    if args[1] in commands.keys():
        bot.send_message(chat_id=user.telegram_id,
                         text=commands[args[1]]['help'])
    else:
        bot.send_message(chat_id=user.telegram_id,
                         text='دستور مورد نظر یافت نشد')


commands = {
    'hello': {'function': hello, 'help': 'اگر ادمین باشید با وارد کردن این دستور، ربات به شما سلام میکند'},
    'info': {'function': info, 'help': 'info <telegram_id | username>\n'
                                       'این دستور مشخصات کاربری که آیدی عددی یا آیدی تلگرامی او را وارد کردید، برای '
                                       'شا نمایش میدهد'},
    'edit': {'function': edit_access_command, 'help': 'edit <telegram_id | username> \n'
                                                      'edit <telegram_id | username> access\n'
                                                      'با استفاده از این دستور میتوانید کاربر جدیدی را ادمین بات کنید\n'
                                                      'هر ادمین سطح دسترسی بالاتر از 1 دارد، توجه داشته باشید که شما '
                                                      'میتونید یک کاربر را در سطحی کمتر از خودتان ادمین کنید'},
    'update': {'function': update, 'help': 'update <telegram_id | username>\n'
                                           'این دستور اطلاعات کاربری که آیدی او را وارد کردید در دیتابیس به روز رسانی '
                                           'میکند'},
    'analyze': {'function': analyze,
                'help': 'اگر میخواهید بدانید که چه کسی به شما پیام داده است، پیام دریافتی را با این دستور ریپلای کنید\n'
                        'این دستور مشخصات کامل کاربر را برای شما نمایش میدهد'},
    'who': {'function': who,
            'help': 'اگر میخواهید بدانید آیدی عددی کسی که به شما پیام داده چیست، پیام دریافتی را با این دستور ریپلای '
                    'کنید'},
    'date': {'function': date, 'help': 'این دستور تاریخ سیستم را به نمایش میدهد'},
    'help': {'function': help_command, 'help': 'help\n'
                                               'help <command name>\n'
                                               'این دستور راهنمای دستور مورد نظر را به شما نشنان میدند'},
    'list': {'function': commands_list, 'help': 'این دستور لیست دستورات موجود را نمایش میدهد'}

}


def command_parser(bot: Bot, user: UserModel, message: Message, args):
    if args[0] in commands.keys():
        commands[args[0]]['function'](bot, user, message, args)
    else:
        bot.send_message(chat_id=user.telegram_id,
                         text='دستور مورد نظر یافت نشد')
