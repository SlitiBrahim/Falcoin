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
        if not self.__is_coinbase_tx():
            tx_input_values = list(map(lambda i: i.get_value(), self.__inputs))
        else:
            tx_input_values = []

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
        tx_input = Input(None, -1)
        tx_output = Output(100)
        tx = Transaction([tx_input], [tx_output])

        return tx

    def __is_coinbase_tx(self):
        return len(self.__inputs) == 1 and self.__inputs[0].is_empty()