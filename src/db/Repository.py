from tinydb import TinyDB, Query

class Repository:

    def __init__(self):
        self.__db = None

    def connect_to_db(self, path):
        self.__db = TinyDB(path)

    def get_all_docs(self):
        return self.__db.all()

    def insert(self, obj):
        """Add Block or list of Blocks in db"""
        if type(obj) is not list:
            obj = [obj]

        # serialized block
        s_blocks = [block.json_obj() for block in obj]
        self.__db.insert_multiple(s_blocks)

    def search(self, query):
        return self.__db.search(query)