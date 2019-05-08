from blockchain.Transaction import Transaction
from blockchain.Input import Input
from blockchain.Output import Output

class CoinbaseTransaction(Transaction):

    def __init__(self, output = None):
        inputs = [CoinbaseTransaction.__generate_empty_input()]
        outputs = [output] if output else [CoinbaseTransaction.__generate_default_output()]

        super().__init__(inputs, outputs)

    def _calculate_fees(self):
        return self._fees

    @staticmethod
    def __generate_empty_input():
        return Input(None, -1)

    @staticmethod
    def __generate_default_output():
        return Output(100)