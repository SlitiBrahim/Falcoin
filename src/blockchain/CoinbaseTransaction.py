from blockchain.Transaction import Transaction
from blockchain.Input import Input
from blockchain.Output import Output

class CoinbaseTransaction(Transaction):

    def __init__(self, output):
        inputs = [CoinbaseTransaction.__generate_empty_input()]
        outputs = [output]

        super().__init__(inputs, outputs, None)

    # used to return fees amount on CoinbaseTransaction creation
    def calculate_fees(self):
        # 0.0 since a coinbase tx doesn't have fees
        return 0.0

    @staticmethod
    def __generate_empty_input():
        return Input(None, -1, None)

    @staticmethod
    def generate_default_output(pubkey):
        return Output(100, pubkey)

    def is_valid(self, _):
        # don't use passed argument, just to be in adequacy with Transaction.is_valid method
        # return empty list for txo hashes (used in Transaction class)
        return self._fees >= 0, []