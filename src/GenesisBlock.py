from Block import Block

class GenesisBlock(Block):

    def __init__(self, transactions = None):
        # Block.__init__(self, transactions)
        super().__init__(transactions)

        # init genesis block's prev_hash as zeros since it is the first in the chain
        self._prev_hash = "0" * 64
