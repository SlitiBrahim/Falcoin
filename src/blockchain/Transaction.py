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