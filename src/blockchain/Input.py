import blockchain.utils as utils
from blockchain import crypto
from blockchain import Output
import math
import json

class Input:

    def __init__(self, prev_tx, index, output_ref = None):
        self.__prev_tx = prev_tx if not None else utils.zeros_hash()
        self.__index = index
        self.__output_ref = output_ref
        self.__pubsig = None

    def get_prev_tx(self):
        return self.__prev_tx

    def get_index(self):
        return self.__index

    def set_pubsig(self, pubsig):
        self.__pubsig = pubsig

    def get_output_ref(self):
        return self.__output_ref

    def is_output_spent(self, blockchain):
        output = self.__output_ref
        output_block = blockchain.find_output_block(output)

        if output.find_reference(output_block, blockchain) is not None:
            return True

        return False

    def can_unlock(self, data, blockchain):
        """Check that output_ref could be unlocked.
        output_ref's receiver must be the one who signed the current input
        """

        if self.is_output_spent(blockchain):
            return False

        # get output_ref's receiver
        txo_receiver_pubkey = self.__output_ref.get_pubkey()

        # return True if the signature matches the outputs' public_key
        return crypto.verify_signature(self.__pubsig, data, txo_receiver_pubkey)

    def is_empty(self):
        return self.__prev_tx is None and self.__index < 0

    def get_value(self):
        if self.is_empty():
            raise Exception("Cannot get value of an empty input.")

        return self.__output_ref.get_value()

    def json_obj(self, with_pubsig=True):
        data = {
            "prev_tx": self.__prev_tx,
            "index": self.__index,
            "output_ref": self.__output_ref.json_obj() if self.__output_ref else None,
        }

        if with_pubsig:
            data["pubsig"] = self.__pubsig

        return data

    @staticmethod
    def deserialize(dict):
        prev_tx = dict['prev_tx']
        index = dict['index']

        if dict['output_ref'] is not None:
            output_ref = Output.deserialize(dict['output_ref'])
        else:
            output_ref = None

        input = Input(prev_tx, index, output_ref)
        input.set_pubsig(dict['pubsig'])

        return input

    def is_valid(self, blockchain):
        # pubsig was not set
        if self.__pubsig is None:
            return False

        data = self.dump_json_obj(with_pubsig=False)
        # check that referred output belongs to the input owner
        if not self.can_unlock(data, blockchain):
            return False

        return True

    def dump_json_obj(self, with_pubsig=True):
        data = json.dumps(self.json_obj(with_pubsig))

        return data

    @staticmethod
    def generate_pubsig(input, private_key):
        data = input.dump_json_obj(with_pubsig=False)
        sig = crypto.sign_message(data, private_key)

        return sig

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