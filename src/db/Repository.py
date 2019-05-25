from tinydb import TinyDB
from blockchain import Block
from .Hydrator import Hydrator

class Repository:

    def __init__(self):
        self.__db = None

    def connect_to_db(self, db_path):
        if self.__db is None:
            self.__db = TinyDB(db_path)

    def add(self, obj):
        """Add a block or a list of blocks"""
        if type(obj) is not list and isinstance(obj, Block) == False:
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

    def db_sync(self, blockchain):
        """Sync db with in-memory blockchain.
        Add in-memory blockchain blocks in db if they were not added
        """

        db_blocks = [Hydrator.hydrate_block(s_block) for s_block in self.get_all_docs()]

        # if blockchain has more blocks than db, that means db is not updated
        if len(blockchain.get_chain()) > len(db_blocks):
            for index, bc_block in enumerate(blockchain.get_chain()):
                try:
                    # will raise Error if db_blocks don't have that index
                    _ = db_blocks[index]
                except IndexError:
                    # if error caught that means db is missing that block
                    self.add(bc_block)
