from blockchain import Block
from blockchain import GenesisBlock

class Hydrator:

    @staticmethod
    def hydrate_block(doc):
        is_genesis_block = doc['index'] == 0

        if is_genesis_block:
            obj = GenesisBlock.deserialize(doc)
        else:
            obj = Block.deserialize(doc)

        return obj