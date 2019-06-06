import time
import json
import math
from hashlib import sha256

class Output:

    def __init__(self, value, pubkey, timestamp = None):
        self.__value = float(value)
        self.__pubkey = pubkey
        self.__timestamp = time.time() if timestamp is None else timestamp

    def get_value(self):
        return self.__value

    def get_pubkey(self):
        return self.__pubkey

    def serialize(self, include_spent = False, blockchain = None):
        data = {
            "value": self.__value,
            "pubkey": self.__pubkey,
            "time": self.__timestamp
        }

        if include_spent:
            data["spent"] = self.is_spent(blockchain)

        return data

    @staticmethod
    def deserialize(dict):
        value = float(dict['value'])
        pubkey = dict['pubkey']
        time = float(dict['time'])

        return Output(value, pubkey, time)

    def hash(self):
        """Returns hash of output"""
        data = json.dumps(self.serialize())
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

    def is_spent(self, blockchain):
        output_block, _ = blockchain.find_output_block(self)

        if self.find_reference(output_block, blockchain) is not None:
            return True

        return False

    @staticmethod
    def total_output_values(outputs):
        tx_output_values = [output.get_value() for output in outputs]

        return math.fsum(tx_output_values)