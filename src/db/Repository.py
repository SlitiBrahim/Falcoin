from tinydb import TinyDB

class Repository:

    def __init__(self):
        self.__db = None

    def connect_to_db(self, db_path):
        if self.__db is None:
            self.__db = TinyDB(db_path)

    def add(self, block):
        self.__db.insert(block.serialize())

    def get_all_docs(self):
        return self.__db.all()