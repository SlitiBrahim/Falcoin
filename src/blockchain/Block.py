from hashlib import sha256
import json

class Block:

    def __init__(self, transactions = None):
        self.__hash = None
        self._index = None
        self._prev_hash = None
        self.__proof_of_work = None
        self.__transactions = transactions if transactions is not None else []
        self.__timestamp = None

    def get_hash(self):
        return self.__hash

    def set_hash(self, str_hash):
        self.__hash = str_hash

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_prev_hash(self):
        return self._prev_hash

    def set_prev_hash(self, prev_hash):
        self._prev_hash = prev_hash

    def get_proof_of_work(self):
        return self.__proof_of_work

    def set_proof_of_work(self, proof_of_work):
        self.__proof_of_work = proof_of_work

    def get_transactions(self):
        return self.__transactions

    def set_transactions(self, transactions):
        self.__transactions = transactions

    # TODO: Add add_transaction method who  check if transaction is already existing

    def get_timestamp(self):
        return self.__timestamp

    def set_timestamp(self, timestamp):
        self.__timestamp = timestamp

    def compute_hash(self, nonce = None):
        if self._prev_hash is None:
            raise Exception("block \"_prev_hash\" property cannot be None, it must be set.")

        # TODO: replace it when Transaction Class is implemented
        transactions = json.dumps(self.__transactions).encode().decode("utf-8")

        # get nonce from parameter if issued otherwise get it from proof_of_work
        # allow to compute hash both by passing nonce parameter or by using the one from the block
        nonce_val = nonce if nonce is not None else self.__proof_of_work.get_nonce()
        key = self._prev_hash + transactions + str(nonce_val)

        return sha256(key.encode()).hexdigest()