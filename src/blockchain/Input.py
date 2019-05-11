import blockchain.utils as utils

class Input:

    def __init__(self, prev_tx, index, output_ref = None):
        self.__prev_tx = prev_tx
        self.__index = index
        self.__output_ref = output_ref
        # TODO: Add PubSig feature

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