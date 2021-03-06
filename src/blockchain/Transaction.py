import math
import json
import time
from hashlib import sha256
from .Input import Input
from .Output import Output

class Transaction:

    def __init__(self, inputs, outputs, fees = None):
        self._inputs = inputs
        self._outputs = outputs
        # if fees arg is not passed calculate it dynamically
        self._fees = float(fees) if fees is not None else self.calculate_fees()
        self._hash = self.compute_hash()

    def get_hash(self):
        return self._hash

    def set_hash(self, str_hash):
        self._hash = str_hash

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def get_output(self, index):
        return self._outputs[index]

    def get_total_inputs(self):
        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_value(), self._inputs))

        return math.fsum(tx_input_values)

    def get_total_outputs(self):
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self._outputs))

        return math.fsum(tx_output_values)

    def calculate_fees(self):
        return self.get_total_inputs() - self.get_total_outputs()

    def get_fees_amount(self):
        return self._fees

    def set_fees(self, fees):
        self._fees = fees

    def _get_data_obj(self, with_txo_spent_prop = False, blockchain = None):
        data = {
            "inputs": [i.serialize() for i in self._inputs],
            "outputs": [o.serialize(with_txo_spent_prop, blockchain) for o in self._outputs]
        }

        return data

    def serialize(self, with_txo_spent_prop = False, blockchain = None):
        """Returns object as dictionary"""
        data = {
            "hash": self._hash,
            **self._get_data_obj(with_txo_spent_prop, blockchain), # use unpack operator to include tx_data
            "fees": self.get_fees_amount()
        }

        return data

    @staticmethod
    def deserialize(dict):
        tx_i = [Input.deserialize(s_txi) for s_txi in dict['inputs']]
        tx_o = [Output.deserialize(s_txo) for s_txo in dict['outputs']]
        fees = dict['fees']
        tx = Transaction(tx_i, tx_o, fees)
        tx.set_hash(dict['hash'])

        return tx

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
    def __is_valid_fees(tx):
        # invalid fees if set as negative number
        if tx.get_fees_amount() < 0:
            return False

        tx_input_values = Input.total_input_values(tx.get_inputs())
        tx_output_values = Output.total_output_values(tx.get_outputs())

        # return false if fees is set as a number greater than what's remaining after inputs - outputs
        return (tx_input_values - tx_output_values) - tx.get_fees_amount() >= 0

    def is_valid(self, referenced_output_hashes, blockchain):
        def invalid_tx():
            return False, []

        txo_hashes = []
        for tx_input in self.get_inputs():
            txo_hashes.append(tx_input.get_output_ref().hash())

        # ===== 1st verification: outputs already referenced by a previous tx in that candidate block
        # True if any of the current tx output ref is already referenced by a previous tx
        any_output_already_referenced = any([txo_hash in referenced_output_hashes for txo_hash in txo_hashes])

        if any_output_already_referenced:
            # invalid tx since its output refs are also referenced in another tx for current candidate block
            # prevent double spending
            return invalid_tx()

        # ===== 2nd verification: same output used as inputs more than once
        if Input.has_duplicate_output_refs(self._inputs):
            return invalid_tx()

        # ===== 3rd verification: check that inputs are >= than outputs and if fees is set, check that is valid
        if self.get_total_inputs() - self.get_total_outputs() - self.get_fees_amount() < 0.0:
            return invalid_tx()

        # ===== 4th verification: check that referred output belongs to input owners
        # (not using an output which does not belong to the input owner)
        # if not all inputs valid
        if not all([input.is_valid(blockchain) for input in self.get_inputs()]):
            return invalid_tx()

        return True, txo_hashes

    @staticmethod
    def extract_valid_transactions(transactions, blockchain):
        # store valid txs as dict: hash, Transaction
        valid_txs = {}
        # output hashes referenced in that transactions list
        referenced_output_hashes = []

        for tx in transactions:
            # check if tx was already processed and validated (tx duplication)
            if tx.get_hash() in list(valid_txs.keys()):
                continue

            is_valid_tx, txo_hashes = tx.is_valid(referenced_output_hashes, blockchain)
            if is_valid_tx:
                # add this tx as a valid transaction
                valid_txs[tx.get_hash()] = tx
                # add valid tx's output refs in the referenced outputs' list
                referenced_output_hashes.extend(txo_hashes)

        return list(valid_txs.values())

    @staticmethod
    def get_tx_by_hash(str_hash, blockchain):
        # TODO: Check for merkle_tree
        for block in blockchain.get_chain():
            for tx in block.get_transactions():
                if str_hash == tx.get_hash():
                    return tx

        return None

    def is_involved(self, pubkey):
        """Return a boolean on either the given pubkey
        is involved in this transaction or not.
        Pubkey is involved if it's used in input output refs or in outputs."""

        for tx_input in self._inputs:
            if not tx_input.is_empty():
                txo = tx_input.get_output_ref()
                if pubkey == txo.get_pubkey():
                    return True
        for tx_output in self._outputs:
            if pubkey == tx_output.get_pubkey():
                return True

        return False

    def get_index(self, output):
        output_hash = output.hash()

        for index, txo in enumerate(self.get_outputs()):
            if txo.hash() == output_hash:
                return index

        return -1