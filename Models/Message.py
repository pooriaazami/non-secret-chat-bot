from Models import Enums


class MessageModel:
    def __init__(self,
                 database_id,
                 receiver_id,
                 sender_id,
                 send_message_id,
                 receive_message_id,
                 replay_to_message_id,
                 send_date,
                 read_date=None,
                 status=Enums.MessageStatus.SENT,
                 text=None,
                 paths=None):
        self.__database_id = database_id
        self.__receiver_id = receiver_id
        self.__sender_id = sender_id
        self.__send_message_id = send_message_id
        self.__receive_message_id = receive_message_id
        self.__replay_to_message_id = replay_to_message_id
        self.__send_date = send_date
        self.__read_date = read_date
        self.__status = status
        self.__text = text
        self.__paths = paths

    @property
    def database_id(self):
        return self.__database_id

    @property
    def receiver_id(self):
        return self.__receiver_id

    @property
    def sender_id(self):
        return self.__sender_id

    @property
    def send_message_id(self):
        return self.__send_message_id

    @property
    def receive_message_id(self):
        return self.__receive_message_id

    @property
    def replay_to_message_id(self):
        return self.__replay_to_message_id

    @property
    def send_date(self):
        return self.__send_date

    @property
    def read_date(self):
        return self.__read_date

    @property
    def status(self):
        return self.__status.value

    @property
    def text(self):
        return self.__text

    @property
    def paths(self):
        return self.__paths
