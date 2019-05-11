class Output:

    def __init__(self, value):
        self.__value = value
        self.__spent = False
        # TODO: Add PubKey feature

    def set_spent(self, spent = True):
        self.__spent = spent

    def get_value(self):
        return self.__value

    def json_obj(self):
        data = {
            "value": self.__value,
            "is_spent": self.__spent
        }

        return data