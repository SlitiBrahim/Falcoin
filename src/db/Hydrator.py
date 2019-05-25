from blockchain import GenesisBlock
from blockchain import Block

class Hydrator:

    @staticmethod
    def hydrate_block(doc):
        is_genesis_block = doc['index'] == 0

        if is_genesis_block:
            # TODO: Implement deserialize method on GenesisBlock
            obj = GenesisBlock.deserialize(doc)
        else:
            obj = Block.deserialize(doc)

        return obj