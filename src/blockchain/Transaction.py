import math
import json
import time
from hashlib import sha256

class Transaction:

    def __init__(self, inputs, outputs):
        self._inputs = inputs
        self._outputs = outputs
        self._fees = 0.0
        self._hash = self.compute_hash()

    def get_hash(self):
        return self._hash

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def get_output(self, index):
        return self._outputs[index]

    def generate_fees(self):
        self._fees = self._calculate_fees()

        return self.get_fees_amount()

    def _calculate_fees(self):
        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_output_ref().get_value(), self._inputs))
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self._outputs))

        return math.fsum(tx_input_values) - math.fsum(tx_output_values)

    def get_fees_amount(self):
        return self._fees

    def _get_data_obj(self):
        data = {
            "inputs": [i.json_obj() for i in self._inputs],
            "outputs": [o.json_obj() for o in self._outputs]
        }

        return data

    """Returns object as dictionary"""
    def json_obj(self):
        data = {
            "hash": self._hash,
            **self._get_data_obj(), # use unpack operator to include tx_data
            "fees": self.generate_fees()
        }

        return data

    def compute_hash(self):
        # get tx data object (dictionary) of current instance and convert it to str
        tx_data = json.dumps(self._get_data_obj())
        # concatenate json + time.time() so the hash is never the same
        # prevent same coinbase txs to have same hashes
        data = (tx_data + str(time.time())).encode().decode("utf-8")

        return sha256(data.encode()).hexdigest()

    @staticmethod
    def merkle_root(transactions):
        is_tx_instances = list(map(lambda obj: isinstance(obj, Transaction), transactions))

        if all(is_tx_instances):
            # get hash of transactions in a list
            tx_hashes = [tx.get_hash() for tx in transactions]
        else:
            is_str_objects = list(map(lambda obj: isinstance(obj, str), transactions))

            if all(is_str_objects):
                tx_hashes = transactions
            else:
                raise TypeError("\"transactions\" argument must be list of Transaction "
                                "objects or list of strings")

        if len(tx_hashes) == 1:
            # return the final hash
            return tx_hashes.pop()
        # check if txs number is even (required for merkle root algorithm)
        elif len(tx_hashes) > 1 and (len(tx_hashes) % 2) != 0:
            # duplicate last hash so txs number is even
            tx_hashes.append(tx_hashes[-1])

        tx_hash_pairs = []
        # iterate over tx_hashes by step 2
        for i in range(0, len(tx_hashes), 2):
            # hash of tx_hash_left + tx_hash_right
            hash_pair = sha256("".join(tx_hashes[i:i+2]).encode()).hexdigest()
            tx_hash_pairs.append(hash_pair)

        # recursively return reduced tx_hash_pairs until we get a single hash
        return Transaction.merkle_root(tx_hash_pairs)