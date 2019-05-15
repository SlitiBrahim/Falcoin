import math
import json
import time
from hashlib import sha256
from blockchain.Input import Input
from blockchain.Output import Output

class Transaction:

    def __init__(self, inputs, outputs, fees = None):
        self._inputs = inputs
        self._outputs = outputs
        # if fees arg is not passed calculate it dynamically
        self._fees = float(fees) if fees is not None else self._calculate_fees()
        self._hash = self.compute_hash()

    def get_hash(self):
        return self._hash

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def get_output(self, index):
        return self._outputs[index]

    def calculate_fees(self):
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
            "fees": self.get_fees_amount()
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
        # > 1 so no infinite loop. check if txs number is even (required for merkle root algorithm)
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

    @staticmethod
    def __has_duplicate_output_refs(inputs):
        output_ref_hashes = []

        for input in inputs:
            output_ref_hash = input.get_output_ref().hash()
            if output_ref_hash in output_ref_hashes:
                return True
            else:
                output_ref_hashes.append(output_ref_hash)

        return False

    @staticmethod
    def __is_valid_fees(tx):
        # invalid fees if set as negative number
        if tx.get_fees_amount() < 0:
            return False

        tx_input_values = Input.total_input_values(tx.get_inputs())
        tx_output_values = Output.total_output_values(tx.get_outputs())

        # return false if fees is set as a number greater than what's remaining after inputs - outputs
        return (tx_input_values - tx_output_values) - tx.get_fees_amount() >= 0

    @staticmethod
    def extract_valid_transactions(transactions):
        # store valid txs as dict: hash, Transaction
        valid_txs = {}
        # output hashes referenced in that transactions list
        referenced_output_hashes = []

        for tx in transactions:
            # check if tx was already processed and validated (tx duplication)
            if tx.get_hash() in list(valid_txs.keys()):
                continue

            # TODO: Remove this, just a pragmatic solution for Parent/Child class import problem
            from blockchain.CoinbaseTransaction import CoinbaseTransaction

            if isinstance(tx, CoinbaseTransaction):
                if tx.get_fees_amount() >= 0.0:
                    continue

                # make coinbase tx as valid. No need to check output refs since there is no one
                valid_txs[tx.get_hash()] = tx
                continue

            # same output ref used in more than one input
            if Transaction.__has_duplicate_output_refs(inputs=tx.get_inputs()):
                continue

            # list containing current transaction output ref hashes
            txo_hashes = []
            for tx_input in tx.get_inputs():
                txo_hashes.append(tx_input.get_output_ref().hash())

            def are_outputs_referenced_in(output_hashes, references):
                for output_hash in output_hashes:
                    if output_hash in references:
                        return True

                return False

            # check if current tx output refs are already referenced by a previous tx
            if are_outputs_referenced_in(txo_hashes, referenced_output_hashes):
                # ignore tx since its output refs are also referenced in another tx for current candidate block
                # prevent double spending
                continue

            # TODO: Check fees

            # TODO: Check if output is already referenced in blockchain

            # finally add this tx as a valid transaction
            valid_txs[tx.get_hash()] = tx
            # add valid tx's output refs in the referenced outputs' list
            referenced_output_hashes.extend(txo_hashes)

        return list(valid_txs.values())