from hashlib import sha256
import json
from .Transaction import Transaction
from .CoinbaseTransaction import CoinbaseTransaction
from .ProofOfWork import ProofOfWork

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

    def get_transaction_by_hash(self, str_hash):
        for tx in self._transactions:
            if tx.get_hash() == str_hash:
                return tx

        return None

    def set_transactions(self, transactions):
        self._transactions = transactions
        self._merkle_root = Transaction.merkle_root(self._transactions)

    def get_timestamp(self):
        return self._timestamp

    def set_timestamp(self, timestamp):
        self._timestamp = timestamp

    def generate_merkle_root(self):
        self._merkle_root = Transaction.merkle_root(self._transactions)

        return self._merkle_root

    def get_merkle_root(self):
        return self._merkle_root

    def set_merkle_root(self, merkle_root):
        self._merkle_root = merkle_root

    def compute_hash(self, nonce = None):
        if self._prev_hash is None:
            raise Exception("block \"_prev_hash\" property cannot be None, it must be set.")

        transactions_hash = self._merkle_root
        # get nonce from parameter if issued otherwise get it from proof_of_work
        # allow to compute hash both by passing nonce parameter or by using the one from the block
        nonce_val = nonce if nonce is not None else self._proof_of_work.get_nonce()

        key = self._prev_hash + transactions_hash + str(nonce_val)

        return sha256(key.encode()).hexdigest()

    def serialize(self):
        data = {
            "hash": self._hash,
            "index": self._index,
            "prev_hash": self._prev_hash,
            "pow": self._proof_of_work.serialize(),
            "transactions": [tx.serialize() for tx in self._transactions],
            "timestamp": self._timestamp,
            "merkle_root": self._merkle_root
        }

        return data

    @staticmethod
    def deserialize(dict):
        # deserialize transactions
        txs = []
        # loop through transactions and get index, transaction (dict)
        for index, s_tx in enumerate(dict['transactions']):
            # if first tx in txs so it's a CoinbaseTransaction
            if index == 0:
                tx = CoinbaseTransaction.deserialize(s_tx)
            else:
                tx = Transaction.deserialize(s_tx)

            txs.append(tx)

        block = Block(txs)
        block.set_hash(dict['hash'])
        block.set_index(dict['index'])
        block.set_prev_hash(dict['prev_hash'])
        block.set_proof_of_work(ProofOfWork.deserialize(dict['pow']))
        block.set_timestamp(dict['timestamp'])
        block.set_merkle_root(dict['merkle_root'])

        return block

    def __str__(self):
        """Prints object as a formatted json"""
        return json.dumps(self.serialize(), indent=4)