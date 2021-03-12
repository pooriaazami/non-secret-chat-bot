from re import split

from telegram import Bot

from Models.Enums import NotifyModes
from Models.User import UserModel

import random


class FfgEncryption:
    # letters => "a1AbBcC2dDeEfFgGh3HiIj4JkKlLmMnNo5OpPqQ6rRsS7tTuUv8VwWxXy9YzZ0"
    letters = ['c', 'q', 'N', 'B', '5', 'P', 'g', 'u', 'J', 'F', '3', 'T', 'r', 'V', 'Z', 'G', '6', 'S', 'O', 'b', 'w',
               'M',
               'z', 'j', 'R', 'Q', '9', 'v', 'X', 'e', 'K', 'i', 'y', 'f', 'E', 'W', 'A', 'H', 'p', 'a', '4', '2', 'x',
               '7',
               'k', 'l', 'o', 'n', 'U', 's', '1', 'm', 'L', '0', 't', 'C', 'I', 'D', 'Y', 'h', '8', 'd']

    def __get_inedx(self, char, string=letters):
        """get the index of character in string in first line."""

        for i in range(len(string)):
            if char == string[i]:
                return i

    def encode(self, parameter: int) -> str:
        """encode the characters"""
        generated = str()
        parameter = str(parameter)
        for i in range(10):
            rand_char = random.sample(self.letters, 1)
            generated += rand_char[0]
        for i in range(len(parameter)):
            generated += str(self.letters[(self.__get_inedx(parameter[i]) + i) % len(self.letters)])
        for i in range(10):
            rand_char = random.sample(self.letters, 1)
            generated += rand_char[0]
        return generated

    def decode(self, parameter: str) -> int:
        """encode the characters"""
        generated = str()
        parameter_rand_less = str()
        for i in range(10, (len(parameter) - 10)):
            parameter_rand_less += parameter[i]
        for i in range(len(parameter_rand_less)):
            generated += str(self.letters[(self.__get_inedx(parameter_rand_less[i]) - i) % len(self.letters)])
        return int(generated)


def generate_link(telegram_id):
    cryptographer = FfgEncryption()
    return f'https://t.me/sercet_chat_test_bot?start={cryptographer.encode(telegram_id)}'


def notify_user(bot: Bot, user: UserModel, mode, *args):
    if mode == NotifyModes.RECEIVE_MESSAGE:
        bot.send_message(chat_id=user.telegram_id, text='یک پیام جدید دارید 📫📫📫\n'
                                                        'برای مشاده دستور /inbox را وارد کنید')
    elif mode == NotifyModes.MESSAGE_READ:
        res = bot.send_message(chat_id=user.telegram_id, text='خوانده شد', reply_to_message_id=args[1])
        return res


def send_advance_message(text, query, keyboard, replay_to_message_id, user, bot: Bot):
    if query != 'None':

        regex = ':|=|;|&'
        split_query: list = split(regex, query)
        split_query.pop()

        ptr = 0
        end = len(split_query)
        while ptr < end:
            caption = split_query.index('caption') if 'caption' in split_query else -1

            if split_query[ptr] == 'animation':
                if replay_to_message_id == 0:
                    res = bot.send_animation(chat_id=user.telegram_id,
                                             animation=split_query[ptr + 2],
                                             reply_markup=keyboard)
                else:
                    res = bot.send_animation(chat_id=user.telegram_id,
                                             animation=split_query[ptr + 2],
                                             reply_to_message_id=replay_to_message_id,
                                             reply_markup=keyboard)
                ptr += 2
            elif split_query[ptr] == 'audio':
                if replay_to_message_id == 0:
                    res = bot.send_audio(chat_id=user.telegram_id,
                                         audio=split_query[ptr + 2],
                                         reply_markup=keyboard)
                else:
                    res = bot.send_audio(chat_id=user.telegram_id,
                                         audio=split_query[ptr + 2],
                                         reply_to_message_id=replay_to_message_id,
                                         reply_markup=keyboard)
                ptr += 2
            elif split_query[ptr] == 'contact':
                if replay_to_message_id == 0:
                    res = bot.send_contact(chat_id=user.telegram_id,
                                           first_name=split_query[ptr + 2],
                                           last_name=split_query[ptr + 4],
                                           phone_number=split_query[ptr + 6],
                                           reply_markup=keyboard)
                else:
                    res = bot.send_contact(chat_id=user.telegram_id,
                                           first_name=split_query[ptr + 2],
                                           last_name=split_query[ptr + 4],
                                           phone_number=split_query[ptr + 6],
                                           reply_to_message_id=replay_to_message_id,
                                           reply_markup=keyboard)
                    ptr += 6
            elif split_query[ptr] == 'document':
                if caption != -1:
                    if replay_to_message_id == 0:
                        res = bot.send_document(chat_id=user.telegram_id,
                                                document=split_query[ptr + 2],
                                                caption=split_query[caption + 2],
                                                reply_markup=keyboard)
                    else:
                        res = bot.send_document(chat_id=user.telegram_id,
                                                document=split_query[ptr + 2],
                                                caption=split_query[caption + 2],
                                                reply_to_message_id=replay_to_message_id,
                                                reply_markup=keyboard)
                else:
                    if replay_to_message_id == 0:
                        res = bot.send_document(chat_id=user.telegram_id,
                                                document=split_query[ptr + 2],
                                                reply_markup=keyboard)
                    else:
                        res = bot.send_document(chat_id=user.telegram_id,
                                                document=split_query[ptr + 2],
                                                reply_to_message_id=replay_to_message_id,
                                                reply_markup=keyboard)

                    ptr += 2
            elif split_query[ptr] == 'photo':
                if caption != -1:
                    if replay_to_message_id == 0:
                        res = bot.send_photo(chat_id=user.telegram_id,
                                             photo=split_query[ptr + 2],
                                             caption=split_query[caption + 2],
                                             reply_markup=keyboard)
                    else:
                        res = bot.send_photo(chat_id=user.telegram_id,
                                             photo=split_query[ptr + 2],
                                             caption=split_query[caption + 2],
                                             reply_to_message_id=replay_to_message_id,
                                             reply_markup=keyboard)
                else:
                    if replay_to_message_id == 0:
                        res = bot.send_photo(chat_id=user.telegram_id,
                                             photo=split_query[ptr + 2],
                                             reply_markup=keyboard)
                    else:
                        res = bot.send_photo(chat_id=user.telegram_id,
                                             photo=split_query[ptr + 2],
                                             reply_to_message_id=replay_to_message_id,
                                             reply_markup=keyboard)
                ptr += 2
            elif split_query[ptr] == 'sticker':
                if replay_to_message_id == 0:
                    res = bot.send_sticker(chat_id=user.telegram_id,
                                           sticker=split_query[ptr + 2],
                                           reply_markup=keyboard)
                else:
                    res = bot.send_sticker(chat_id=user.telegram_id,
                                           sticker=split_query[ptr + 2],
                                           reply_to_message_id=replay_to_message_id,
                                           reply_markup=keyboard)
                    ptr += 2
            elif split_query[ptr] == 'video':
                if replay_to_message_id == 0:
                    res = bot.send_video(chat_id=user.telegram_id,
                                         video=split_query[ptr + 2],
                                         reply_markup=keyboard)
                else:
                    res = bot.send_video(chat_id=user.telegram_id,
                                         video=split_query[ptr + 2],
                                         reply_to_message_id=replay_to_message_id,
                                         reply_markup=keyboard)
                    ptr += 2
            elif split_query[ptr] == 'voice':
                if replay_to_message_id == 0:
                    res = bot.send_voice(chat_id=user.telegram_id,
                                         voice=split_query[ptr + 2],
                                         reply_markup=keyboard)
                else:
                    res = bot.send_voice(chat_id=user.telegram_id,
                                         voice=split_query[ptr + 2],
                                         reply_to_message_id=replay_to_message_id,
                                         reply_markup=keyboard)
                    ptr += 2

            ptr += 1
    else:
        if replay_to_message_id == 0:
            res = bot.send_message(chat_id=user.telegram_id,
                                   text=text,
                                   reply_markup=keyboard)
        else:
            res = bot.send_message(chat_id=user.telegram_id,
                                   text=text,
                                   reply_to_message_id=replay_to_message_id,
                                   reply_markup=keyboard)

    return res
