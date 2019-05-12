class Output:

    def __init__(self, value, pubkey):
        self.__value = value
        self.__spent = False
        self.__pubkey = pubkey

    def set_spent(self, spent = True):
        self.__spent = spent

    def get_value(self):
        return self.__value

    def get_pubkey(self):
        return self.__pubkey

    def json_obj(self):
        data = {
            "value": self.__value,
            "is_spent": self.__spent
        }

        return data