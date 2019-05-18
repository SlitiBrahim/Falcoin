import blockchain.utils as utils
from blockchain import crypto
import math

class Input:

    def __init__(self, prev_tx, index, pubsig, output_ref = None):
        self.__prev_tx = prev_tx
        self.__index = index
        self.__output_ref = output_ref
        self.__pubsig = pubsig

    def get_prev_tx(self):
        return self.__prev_tx

    def get_index(self):
        return self.__index

    def get_output_ref(self):
        return self.__output_ref

    """Check that output_ref could be unlocked.
    output_ref's receiver must be the one who signed the current input"""
    def can_unlock(self, data):
        # get output_ref's receiver
        txo_receiver_pubkey = self.__output_ref.get_pubkey()

        # return True if the signature matches the outputs' public_key
        return crypto.verify_signature(self.__pubsig, data, txo_receiver_pubkey)

    def is_empty(self):
        return self.__prev_tx is None and self.__index < 0

    def get_value(self):
        if self.is_empty():
            raise Exception("Cannot get value of an empty input.")

        prev_tx_outputs = self.__prev_tx.get_outputs()
        input_value = prev_tx_outputs[self.__index]

        return input_value

    def json_obj(self):
        data = {
            "prev_tx": self.__prev_tx.get_hash() if not self.is_empty() else utils.zeros_hash(),
            "index": self.__index,
            "output_ref": self.__output_ref.json_obj() if self.__output_ref else None,
            "pubsig": self.__pubsig
        }

        return data

    @staticmethod
    def total_input_values(inputs):
        tx_input_values = [input.get_output_ref().get_value() for input in inputs]

        return math.fsum(tx_input_values)

    @staticmethod
    def has_duplicate_output_refs(inputs):
        output_ref_hashes = []

        for input in inputs:
            output_ref_hash = input.get_output_ref().hash()
            if output_ref_hash in output_ref_hashes:
                return True
            else:
                output_ref_hashes.append(output_ref_hash)

        return False