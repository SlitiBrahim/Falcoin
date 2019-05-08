import math
import json
import time
from hashlib import sha256
from blockchain.Input import Input
from blockchain.Output import Output

class Transaction:

    def __init__(self, inputs, outputs):
        self.__inputs = inputs
        self.__outputs = outputs
        self._fees = 0.0
        self.__hash = self.compute_hash()

    def get_hash(self):
        return self.__hash

    def get_inputs(self):
        return self.__inputs

    def get_outputs(self):
        return self.__outputs

    def get_output(self, index):
        return self.__outputs[index]

    def generate_fees(self):
        self._fees = self._calculate_fees()

        return self.get_fees_amount()

    def _calculate_fees(self):
        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_output_ref().get_value(), self.__inputs))
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self.__outputs))

        return math.fsum(tx_input_values) - math.fsum(tx_output_values)

    def get_fees_amount(self):
        return self._fees

    """Returns object as dictionary"""
    def json_obj(self):
        data = {
            "inputs": [i.json_obj() for i in self.__inputs],
            "outputs": [o.json_obj() for o in self.__outputs],
            "fees": self.generate_fees()
        }

        return data

    def compute_hash(self):
        # get json object (dictionary) of current instance and convert it to str
        json_data = json.dumps(self.json_obj())
        # concatenate json + time.time() so the hash is never the same
        # prevent same coinbase txs to have same hashes
        data = (json_data + str(time.time())).encode().decode("utf-8")

        return sha256(data.encode()).hexdigest()