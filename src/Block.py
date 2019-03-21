from hashlib import sha256
import json

class Block:

    def __init__(self):
        self.__hash = None
        self.__index = None # TODO: Replace it with Blockchain.get_chain_length()
        self.__prev_hash = None
        self.__proof_of_work = None
        self.__nonce = None
        self.__transactions = []
        self.__timestamp = None

    def get_hash(self):
        return self.__hash

    def set_hash(self, str_hash):
        self.__hash = str_hash

    def get_index(self):
        return self.__index

    def set_index(self, index):
        self.__index = index

    def get_prev_hash(self):
        return self.__prev_hash

    def set_prev_hash(self, prev_hash):
        self.__prev_hash = prev_hash

    def get_nonce(self):
        return self.__nonce

    def set_nonce(self, nonce):
        self.__nonce = nonce

    def get_transactions(self):
        return self.__transactions

    def set_transactions(self, transactions):
        self.__transactions = transactions

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    @staticmethod
    def hash(block):
        if block.get_nonce() is None or block.get_prev_hash() is None:
            raise Exception(f"Value of 'nonce' or 'prev_hash' property of the block is None")

        # TODO: replace it when Transaction Class is implemented
        transactions = json.dumps(block.get_transactions()).encode().decode("utf-8")
        key = block.get_prev_hash() + transactions + str(block.get_nonce())

        return sha256(key.encode()).hexdigest()