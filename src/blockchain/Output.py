class Output:

    def __init__(self, value):
        self.__value = value
        # TODO: Add PubKey feature

    def get_value(self):
        return self.__value

    def json_obj(self):
        data = {
            "value": self.__value
        }

        return data