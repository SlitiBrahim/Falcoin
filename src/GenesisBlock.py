from Block import Block

class GenesisBlock(Block):

    def __init__(self, transactions = None):
        super().__init__(transactions)

        # init genesis block's prev_hash as zeros since it is the first in the chain
        self._prev_hash = "0" * 64
        self._index = 0
