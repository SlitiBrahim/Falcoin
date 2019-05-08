from hashlib import sha256
import json
from blockchain.Transaction import Transaction

class Block:

    def __init__(self, transactions = None):
        self._hash = None
        self._index = None
        self._prev_hash = None
        self._proof_of_work = None
        self._transactions = transactions if transactions is not None else []
        self._timestamp = None
        self._merkle_root = self.generate_merkle_root()

    def get_hash(self):
        return self._hash

    def set_hash(self, str_hash):
        self._hash = str_hash

    def get_index(self):
        return self._index

    def set_index(self, index):
        self._index = index

    def get_prev_hash(self):
        return self._prev_hash

    def set_prev_hash(self, prev_hash):
        self._prev_hash = prev_hash

    def get_proof_of_work(self):
        return self._proof_of_work

    def set_proof_of_work(self, proof_of_work):
        self._proof_of_work = proof_of_work

    def get_transactions(self):
        return self._transactions

    def set_transactions(self, transactions):
        self._transactions = transactions
        self._merkle_root = Transaction.merkle_root(self._transactions)

    # TODO: Add add_transaction method who  check if transaction is already existing

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def generate_merkle_root(self):
        self._merkle_root = Transaction.merkle_root(self._transactions)

        return self._merkle_root

    def compute_hash(self, nonce = None):
        if self._prev_hash is None:
            raise Exception("block \"_prev_hash\" property cannot be None, it must be set.")

        # TODO: replace it with merkle root value
        transactions = json.dumps([]).encode().decode("utf-8")
        # get nonce from parameter if issued otherwise get it from proof_of_work
        # allow to compute hash both by passing nonce parameter or by using the one from the block
        nonce_val = nonce if nonce is not None else self._proof_of_work.get_nonce()

        key = self._prev_hash + transactions + str(nonce_val)

        return sha256(key.encode()).hexdigest()

    def json_obj(self):
        data = {
            "hash": self._hash,
            "index": self._index,
            "prev_hash": self._prev_hash,
            "pow": self._proof_of_work.json_obj(),
            "transactions": [tx.json_obj() for tx in self._transactions],
            "timestamp": self._timestamp,
            "merkle_root": self._merkle_root
        }

        return data

    """Prints object as a formatted json"""
    def __str__(self):
        return json.dumps(self.json_obj(), indent=4)