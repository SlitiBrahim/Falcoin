from blockchain.Block import Block
import blockchain.utils as utils

class GenesisBlock(Block):

    def __init__(self, transactions = None):
        super().__init__(transactions)

        # init genesis block's prev_hash as zeros since it is the first in the chain
        self._prev_hash = utils.zeros_hash()
        self._index = 0

    @staticmethod
    def deserialize(dict):
        """Use Block.deserialize method but cast result to a GenesisBlock obj"""
        block = super(GenesisBlock, GenesisBlock).deserialize(dict)

        genesis_block = GenesisBlock(block.get_transactions())
        genesis_block.set_hash(block.get_hash())
        genesis_block.set_index(block.get_index())
        genesis_block.set_prev_hash(block.get_prev_hash())
        genesis_block.set_proof_of_work(block.get_proof_of_work())
        genesis_block.set_timestamp(block.get_timestamp())
        genesis_block.set_merkle_root(block.get_merkle_root())

        return genesis_block