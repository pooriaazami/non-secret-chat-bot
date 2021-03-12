import datetime
import sqlite3

from Models.Enums import MessageStatus, NotifyModes
from Models.Message import MessageModel
from Models.User import UserModel
from utils.task_manager import notify_user


def insert_user(user):
    with sqlite3.connect('./databases/users.sqlite3') as conn:
        cursor = conn.cursor()

        query = f"INSERT INTO USERS (telegram_id, firstname, lastname, username, access) " \
                f"VALUES({user.telegram_id}, '{user.firstname}', '{user.lastname}', '{user.username}', {user.access})"

        cursor.execute(query)
        conn.commit()


def read_user_by_id(telegram_id):
    with sqlite3.connect('./databases/users.sqlite3') as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM USERS WHERE telegram_id = {telegram_id}"

        result = cursor.execute(query).fetchall()

    if len(result) == 0:
        return None

    return UserModel(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])


def read_user_by_username(username):
    if username[0] == '@':
        username = username[1:]

    with sqlite3.connect('./databases/users.sqlite3') as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM USERS WHERE username = '{username}'"

        result = cursor.execute(query).fetchall()

    if len(result) == 0:
        return None

    return UserModel(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])


def insert_message(message: MessageModel):
    with sqlite3.connect('./databases/messages.sqlite3') as conn:
        cursor = conn.cursor()

        if message.text is not None:
            text = message.text.replace("'", "\'")
        else:
            text = message.text

        if message.paths is not None:
            caption = message.paths.replace("'", "\'")
        else:
            caption = message.paths

        query = f"INSERT INTO MESSAGES (receiver_id, sender_id," \
                f" send_message_id, receive_message_id, " \
                f"send_date, read_date," \
                f"status, text, paths, replay_to_message_id) VALUES({message.receiver_id}, {message.sender_id}," \
                f"{message.send_message_id}, " \
                f"{message.receive_message_id}," \
                f"'{message.send_date}', " \
                f"'{message.read_date}'," \
                f"{message.status}, " \
                f"'{text}', " \
                f"'{caption}', " \
                f"{message.replay_to_message_id})"

        cursor.execute(query)
        conn.commit()


def read_messages(telegram_id):
    with sqlite3.connect('./databases/messages.sqlite3') as conn:
        cursor = conn.cursor()
        query = f"SELECT * FROM MESSAGES WHERE receiver_id = {telegram_id} and status = 0"

        res = cursor.execute(query).fetchall()

    ans = []
    for message in res:
        ans.append(MessageModel(
            database_id=message[0],
            receiver_id=message[1],
            sender_id=message[2],
            send_message_id=message[3],
            receive_message_id=message[4],
            replay_to_message_id=message[5],
            send_date=message[6],
            read_date=message[7],
            status=MessageStatus(message[8]),
            text=message[9].replace("\'", "'"),
            paths=message[10].replace("\'", "'")
        ))

    return ans


def mark_messages_as_read(messages, bot, user, res):
    with sqlite3.connect('./databases/messages.sqlite3') as conn:
        cursor = conn.cursor()

        for message in messages:
            sender = read_user_by_id(message.sender_id)

            notify_user(bot, sender, NotifyModes.MESSAGE_READ, user.firstname, message.send_message_id)
            query = f"UPDATE MESSAGES SET " \
                    f"status={MessageStatus.READ.value}, " \
                    f"read_date='{str(datetime.datetime.now())}', " \
                    f"receive_message_id = {res.message_id} " \
                    f"WHERE id={message.database_id}"

            cursor.execute(query)

        conn.commit()


def edit_access(user: UserModel, access):
    with sqlite3.connect('./databases/users.sqlite3') as conn:
        cursor = conn.cursor()

        query = f"UPDATE USERS SET access={access} WHERE telegram_id = {user.telegram_id}"

        cursor.execute(query)
        conn.commit()


def rewrite_user(user):
    with sqlite3.connect('./databases/users.sqlite3') as conn:
        cursor = conn.cursor()

        query = f"UPDATE USERS SET firstname = '{user.firstname}', lastname = '{user.lastname}'," \
                f" username = '{user.username}' WHERE telegram_id={user.telegram_id}"

        cursor.execute(query)
        conn.commit()


def read_message_by_id(chat_id, message_id):
    with sqlite3.connect('./databases/messages.sqlite3') as conn:
        cursor = conn.cursor()

        query = f"SELECT * FROM MESSAGES WHERE receiver_id={chat_id} and receive_message_id={message_id}"

        res = cursor.execute(query).fetchall()

        conn.commit()

    if len(res) == 0:
        return None

    return MessageModel(
        database_id=res[0][0],
        receiver_id=res[0][1],
        sender_id=res[0][2],
        send_message_id=res[0][3],
        receive_message_id=res[0][4],
        replay_to_message_id=res[0][5],
        send_date=res[0][6],
        read_date=res[0][7],
        status=MessageStatus(res[0][8]),
        text=res[0][9].replace("\'", "'"),
        paths=res[0][10].replace("\'", "'")
    )
