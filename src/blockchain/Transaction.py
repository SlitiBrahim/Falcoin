import math
from blockchain.Input import Input
from blockchain.Output import Output

class Transaction:

    def __init__(self, inputs, outputs):
        self.__inputs = inputs
        self.__outputs = outputs
        self.__fees = 0.0

    def get_inputs(self):
        return self.__inputs

    def get_outputs(self):
        return self.__outputs

    def get_output(self, index):
        return self.__outputs[index]

    def generate_fees(self):
        self.__fees = self._calculate_fees()

        return self.get_fees_amount()

    def _calculate_fees(self):
        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_value(), self.__inputs))
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self.__outputs))

        return math.fsum(tx_input_values) - math.fsum(tx_output_values)

    def get_fees_amount(self):
        return self.__fees