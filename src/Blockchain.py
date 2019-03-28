from Block import Block

class Blockchain:

    def __init__(self):
        self.__chain = []

    def get_chain(self, start = 0, end = None):
        if end is not None:
            return self.__chain[start:end]

        return self.__chain[start:]

    def get_last_block(self):
        return self.__chain[-1]

    def get_chain_length(self):
        return len(self.__chain)

    def add_block_to_chain(self, block):
        index = self.get_chain_length()
        block.set_index(index)

        # check if block already exist in the chain
        if self.find_block(block.get_hash()) is not None:
            raise Exception("Block already exist in chain")

        self.__chain.append(block)

        return self.__chain

    def find_block(self, str_hash):
        """Retrieve a block in the chain by its hash"""

        for block in self.__chain:
            if block.get_hash() == str_hash:
                return block

        # block not found
        return None


