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
    txs = [
        CoinbaseTransaction()
    ]

    genesis_block = GenesisBlock(txs)

    pow = ProofOfWork.run(genesis_block)
    genesis_block.set_proof_of_work(pow)
    genesis_block.set_hash(pow.get_hash())
    genesis_block.set_timestamp(time.time())

    print(genesis_block)

    txs1 = [
        CoinbaseTransaction(),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
        Transaction(inputs=[Input(txs[0], 0, txs[0].get_output(index=0))], outputs=[Output(10)]),
    ]
    block = Block(txs1)

    block.set_index(1)
    block.set_prev_hash(genesis_block.get_hash())
    pow = ProofOfWork.run(block)
    block.set_proof_of_work(pow)
    block.set_hash(pow.get_hash())
    block.set_timestamp(time.time())

    print(block)

    print("debug")

if __name__ == '__main__':
    main()