class Output:

    def __init__(self, value, pubkey):
        self.__value = value
        self.__pubkey = pubkey

    def get_value(self):
        return self.__value

    def get_pubkey(self):
        return self.__pubkey

    def json_obj(self):
        data = {
            "value": self.__value,
            "pubkey": self.__pubkey
        }

        return data