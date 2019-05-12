import blockchain.utils as utils
from blockchain import crypto

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

    """Set referred output as spent"""
    def make_output_ref_spent(self):
        self.__output_ref.set_spent()

        return self.__output_ref

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
            "output_ref": self.__output_ref.json_obj() if self.__output_ref else None
        }

        return data