from enum import Enum


class UserStatus(Enum):
    STABLE = 0
    SENDING_MESSAGE = 1


class MessageStatus(Enum):
    SENT = 0
    RECEIVE = 1
    READ = 2


class NotifyModes(Enum):
    RECEIVE_MESSAGE = 0
    MESSAGE_READ = 1
