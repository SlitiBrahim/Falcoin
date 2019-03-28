from Block import Block

class Blockchain:

    def __init__(self):
        self.__chain = []

    def get_chain(self, start = 0, end = None):
        if end is not None:
            return self.__chain[start:end]

        return self.__chain[start:]


    def add_to_chain(self, obj):
        if type(obj) is list:
            self.__chain += obj
        elif isinstance(obj, Block):
            self.__chain.append(obj)
        else:
            raise Exception("obj to add to chain must me list of blocks or instance of block")

        return self.__chain

    # TODO: TEST THAT !
    def find_block(self, str_hash):
        """Retrieve a block in the chain by its hash"""

        for block in self.__chain:
            if block.get_hash() == str_hash:
                return block

        # block not found
        return None


