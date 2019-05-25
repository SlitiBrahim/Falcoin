from tinydb import TinyDB
from blockchain import Block

class Repository:

    def __init__(self):
        self.__db = None

    def connect_to_db(self, db_path):
        if self.__db is None:
            self.__db = TinyDB(db_path)

    def add(self, obj):
        """Add a block or a list of blocks"""
        if obj is not list and isinstance(obj, Block) == False:
            raise TypeError("arg should be a block obj or a list of block objects")

        if isinstance(obj, Block):
            objs = [obj]
        else:
            objs = obj

        # serialized block objects
        s_objs = [o.serialize() for o in objs]

        self.__db.insert_multiple(s_objs)

    def get_all_docs(self):
        return self.__db.all()