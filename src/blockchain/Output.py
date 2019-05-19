import time
import json
import math
from hashlib import sha256

class Output:

    def __init__(self, value, pubkey):
        self.__value = value
        self.__pubkey = pubkey
        self.__timestamp = time.time()

    def get_value(self):
        return self.__value

    def get_pubkey(self):
        return self.__pubkey

    def json_obj(self):
        data = {
            "value": self.__value,
            "pubkey": self.__pubkey,
            "time": self.__timestamp
        }

        return data

    def hash(self):
        """Returns hash of output"""
        data = json.dumps(self.json_obj())
        hash = sha256(data.encode()).hexdigest()

        return hash

    def find_reference(self, output_block, blockchain):
        """Returns tx_input and its block if output is referenced, otherwise will return None"""

        # start looking for reference from next block after output's block
        # avoid iterating on blockchain from first block
        start_index = output_block.get_index() + 1

        # iterating on all blocks after output's block
        for block in blockchain.get_chain(start=start_index):
            for tx in block.get_transactions():
                for tx_input in tx.get_inputs():
                    if not tx_input.is_empty():
                        # if input's output_ref is equal to current output instance
                        if self.hash() == tx_input.get_output_ref().hash():
                            # return input that refers current output and its block
                            return tx_input, block

        # output not referred in any input
        return None

    @staticmethod
    def total_output_values(outputs):
        tx_output_values = [output.get_value() for output in outputs]

        return math.fsum(tx_output_values)