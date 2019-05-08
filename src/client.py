from blockchain.Block import Block
from blockchain.GenesisBlock import GenesisBlock
from blockchain.ProofOfWork import ProofOfWork
from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from blockchain.CoinbaseTransaction import CoinbaseTransaction
from blockchain.Input import Input
from blockchain.Output import Output
import time

def main():
    blockchain = Blockchain()

    transactions = [
        CoinbaseTransaction()
    ]

    block = GenesisBlock(transactions)

    proof_of_work = ProofOfWork.run(block)
    block.set_proof_of_work(proof_of_work)
    block.set_hash(proof_of_work.get_hash())
    block.set_timestamp(time.time())

    blockchain.add_block_to_chain(block)

    print("hash of the mined block:", block.get_hash())
    print("last block hash:", block.get_prev_hash())
    print("nonce:", block.get_proof_of_work().get_nonce())
    print("timestamp:", block.get_timestamp())

    txs = [
        CoinbaseTransaction(),
        Transaction(inputs=[Input(transactions[0], 0, transactions[0].get_output(index=0))],
                    outputs=[Output(15)])
    ]

    block1 = Block(txs)
    block1.set_prev_hash(blockchain.get_last_block().get_hash())

    pow = ProofOfWork.run(block1)
    block1.set_proof_of_work(pow)
    block1.set_hash(pow.get_hash())
    block1.set_timestamp(time.time())

    blockchain.add_block_to_chain(block1)

    print("debug")

if __name__ == '__main__':
    main()