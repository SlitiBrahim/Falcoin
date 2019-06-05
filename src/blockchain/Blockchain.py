from .Block import Block
from .GenesisBlock import GenesisBlock

class Blockchain:

    __instantiated = False

    def __init__(self):
        if Blockchain.__instantiated:
            raise Exception("Singleton Blockchain class already instantiated.")
        else:
            Blockchain.__instantiated = True

        self.__chain = []

    def get_chain(self, start = 0, end = None):
        if end is not None:
            return self.__chain[start:end]

        return self.__chain[start:]

    def set_chain(self, blocks):
        """Allow to set chain with blocks got from local db"""

        if len(self.get_chain()) > 0:
            raise Exception("Blockchain already contains blocks, setting chain "
                            "is only allowed for empty blockchain")

        # check if all elements are Block objects
        valid = all(list(map(lambda b: isinstance(b, Block), blocks)))

        if valid:
            self.__chain = blocks

    def get_last_block(self):
        if self.get_chain_length() == 0:
            return None

        return self.__chain[-1]

    def get_chain_length(self):
        return len(self.__chain)

    def add_block_to_chain(self, block):
        index = self.get_chain_length()

        if index == 0 and not isinstance(block, GenesisBlock):
            raise Exception("First block added in the chain must be of type GenesisBlock")

        block.set_index(index)

        # check if block already exist in the chain
        if self.find_block(block.get_hash()) is not None:
            raise Exception("Block already exist in chain")

        self.__chain.append(block)

        return self.__chain

    def add_blocks_to_chain(self, obj_list):
        is_block_instances = list(map(lambda obj: isinstance(obj, Block), obj_list))

        # check if obj_list contains non-Block instances
        if not all(is_block_instances):
            raise Exception("List must contain only Block instances")

        for block in obj_list:
            try:
                self.add_block_to_chain(block)
            except Exception:
                continue

    def find_block(self, str_hash):
        """Retrieve a block in the chain by its hash"""

        for block in self.__chain:
            if block.get_hash() == str_hash:
                return block

        # block not found
        return None

    def find_output_block(self, output):
        """Retrieve a block in the chain by an output"""

        output_hash = output.hash()
        for block in self.__chain:
            for tx in block.get_transactions():
                for tx_output in tx.get_outputs():
                    if tx_output.hash() == output_hash:
                        return block

        # block not found
        return None

    def count_balance(self, pubkey):
        balance = 0.0

        # transaction where the given pubkey is involved
        txs = self.get_transactions(pubkey)

        for tx in txs:
            for tx_input in tx.get_inputs():
                if not tx_input.is_empty():
                    txo = tx_input.get_output_ref()
                    if pubkey == txo.get_pubkey():
                        balance -= txo.get_value()
            for tx_output in tx.get_outputs():
                if pubkey == tx_output.get_pubkey():
                    balance += tx_output.get_value()

        return balance

    def get_transactions(self, pubkey=None):
        """If pubkey is set, will return all txs where pubkey is involved
        Otherwise will return all transactions
        """

        txs = []

        for block in self.__chain:
            for tx in block.get_transactions():
                # if pubkey is passed and tx does'nt involve given pubkey
                if pubkey is not None and not tx.is_involved(pubkey):
                    break

                txs.append(tx)

        return txs