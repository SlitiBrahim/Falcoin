from blockchain.Block import Block
from blockchain.GenesisBlock import GenesisBlock
from blockchain.ProofOfWork import ProofOfWork
from blockchain.Blockchain import Blockchain
from blockchain.Transaction import Transaction
from blockchain.CoinbaseTransaction import CoinbaseTransaction
from blockchain.Input import Input
from blockchain.Output import Output
from blockchain import crypto
from blockchain import utils
import time

def main():

    # can_unlock = yanis_tx.get_inputs()[0].can_unlock(msg)
    #
    # if can_unlock:
    #     print("referenced output can be unlocked")
    # else:
    #     print("cannot be unlocked")

    msg = "random data"
    brahim_private_key, brahim_public_key = crypto.generate_key_pair()
    brahim_sig = crypto.sign_message(msg, brahim_private_key)

    yanis_private_key, yanis_public_key = crypto.generate_key_pair()
    yanis_sig = crypto.sign_message(msg, yanis_private_key)

    hacker_private_key, hacker_public_key = crypto.generate_key_pair()
    hacker_sig = crypto.sign_message(msg, hacker_private_key)

    _, miner_public_key = crypto.generate_key_pair()

    txs = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(brahim_public_key))
    ]

    genesis_block = GenesisBlock(txs)

    pow = ProofOfWork.run(genesis_block)
    genesis_block.set_proof_of_work(pow)
    genesis_block.set_hash(pow.get_hash())
    genesis_block.set_timestamp(time.time())

    txs1 = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(miner_public_key)),
        Transaction(inputs=[Input(txs[0], 0, brahim_sig ,txs[0].get_output(index=0))], outputs=[Output(10, yanis_public_key)], fees=1.0),
    ]
    block = Block(txs1)

    block.set_index(1)
    block.set_prev_hash(genesis_block.get_hash())
    pow = ProofOfWork.run(block)
    block.set_proof_of_work(pow)
    block.set_hash(pow.get_hash())
    block.set_timestamp(time.time())

    print(genesis_block)

    print(block)

    print("debug")

if __name__ == '__main__':
    main()