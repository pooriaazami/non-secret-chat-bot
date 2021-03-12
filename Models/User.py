class UserModel:

    def __init__(self, telegram_id, firstname, lastname, username, access=1):
        self.__telegram_id = telegram_id
        self.__firstname = firstname
        self.__lastname = lastname
        self.__username = username
        self.__access = access

    @property
    def firstname(self):
        return self.__firstname

    @property
    def lastname(self):
        return self.__lastname

    @property
    def username(self):
        return self.__username

    @property
    def telegram_id(self):
        return self.__telegram_id

    @property
    def access(self):
        return self.__access

    @firstname.setter
    def firstname(self, vale):
        self.__firstname = vale

    @lastname.setter
    def lastname(self, vale):
        self.__lastname = vale

    @username.setter
    def username(self, vale):
        self.__username = vale

    @access.setter
    def access(self, vale):
        self.__access = vale

    def __eq__(self, o: object) -> bool:
        if o.__init_subclass__(UserModel):
            return self.__telegram_id == o.telegram_id and \
                   self.__username == o.username and \
                   self.__access == o.access and \
                   self.__lastname == o.lastname

        return False
