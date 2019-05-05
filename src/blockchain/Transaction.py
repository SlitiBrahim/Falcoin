import math
from blockchain.Input import Input
from blockchain.Output import Output

class Transaction:

    def __init__(self, inputs, outputs):
        self.__inputs = inputs
        self.__outputs = outputs
        self.__fees = self.__calculate_fees()

    def get_inputs(self):
        return self.__inputs

    def get_outputs(self):
        return self.__outputs

    def __calculate_fees(self):
        if self.__is_coinbase_tx():
            # to fees for coinbase tx
            return 0.0

        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_value(), self.__inputs))
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self.__outputs))

        return Transaction.__get_total(tx_input_values) - Transaction.__get_total(tx_output_values)

    def get_fees_amount(self):
        return self.__fees

    @staticmethod
    def __get_total(collection):
        # not using += to sum up double numbers for avoiding errors to accumulate quickly
        return math.fsum(collection)

    @staticmethod
    def generate_coinbase_tx():
        # input of a coinbase tx do not point to an existing tx output
        tx_input = Input(None, -1)
        # reward for the miner who mined the block
        tx_output = Output(100)
        # tx with one input and one output only
        tx = Transaction([tx_input], [tx_output])

        return tx

    """"Return true if the instance of Transaction is a coinbase transaction"""
    def __is_coinbase_tx(self):
        return len(self.__inputs) == 1 and self.__inputs[0].is_empty()