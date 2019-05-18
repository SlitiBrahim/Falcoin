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

    # msg = "random data"
    # brahim_private_key, brahim_public_key = crypto.generate_key_pair()
    # brahim_sig = crypto.sign_message(msg, brahim_private_key)
    #
    # yanis_private_key, yanis_public_key = crypto.generate_key_pair()
    # yanis_sig = crypto.sign_message(msg, yanis_private_key)
    #
    # hacker_private_key, hacker_public_key = crypto.generate_key_pair()
    # hacker_sig = crypto.sign_message(msg, hacker_private_key)
    #
    # _, miner_public_key = crypto.generate_key_pair()
    #
    # txs = [
    #     CoinbaseTransaction(CoinbaseTransaction.generate_default_output(brahim_public_key))
    # ]
    #
    # genesis_block = GenesisBlock(txs)
    #
    # pow = ProofOfWork.run(genesis_block)
    # genesis_block.set_proof_of_work(pow)
    # genesis_block.set_hash(pow.get_hash())
    # genesis_block.set_timestamp(time.time())
    #
    # txs1 = [
    #     CoinbaseTransaction(CoinbaseTransaction.generate_default_output(miner_public_key)),
    #     Transaction(inputs=[Input(txs[0], 0, brahim_sig ,txs[0].get_output(index=0))], outputs=[Output(10, yanis_public_key)], fees=1.0),
    # ]
    # block = Block(txs1)
    #
    # block.set_index(1)
    # block.set_prev_hash(genesis_block.get_hash())
    # pow = ProofOfWork.run(block)
    # block.set_proof_of_work(pow)
    # block.set_hash(pow.get_hash())
    # block.set_timestamp(time.time())
    #
    # print(genesis_block)
    #
    # print(block)

    blockchain = Blockchain()

    my_private_key, my_public_key = crypto.generate_key_pair()
    yanis_private_key, yanis_public_key = crypto.generate_key_pair()

    txs = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(yanis_public_key))
    ]

    genesis_block = GenesisBlock(Transaction.extract_valid_transactions(txs, blockchain))
    pow = ProofOfWork.run(genesis_block)
    genesis_block.set_proof_of_work(pow)
    genesis_block.set_hash(pow.get_hash())
    genesis_block.set_timestamp(time.time())

    blockchain.add_block_to_chain(genesis_block)

    input = Input(txs[0], 0, txs[0].get_output(index=0))
    input.set_pubsig(Input.generate_pubsig(input, yanis_private_key))

    txs1 = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(my_public_key)),
        Transaction(inputs=[input], outputs=[Output(10, my_public_key)], fees=0.0),
    ]

    block1 = Block(Transaction.extract_valid_transactions(txs1, blockchain))
    block1.set_index(1)
    block1.set_prev_hash(genesis_block.get_hash())
    pow = ProofOfWork.run(block1)
    block1.set_proof_of_work(pow)
    block1.set_hash(pow.get_hash())
    block1.set_timestamp(time.time())

    blockchain.add_block_to_chain(block1)

    input = Input(txs1[1], 0, txs1[1].get_output(index=0))
    input.set_pubsig(Input.generate_pubsig(input, my_private_key))

    txs2 = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(my_public_key)),
        Transaction(inputs=[input], outputs=[Output(10, yanis_public_key)], fees=0.0),
    ]

    block2 = Block(Transaction.extract_valid_transactions(txs2, blockchain))
    block2.set_index(1)
    block2.set_prev_hash(block1.get_hash())
    pow = ProofOfWork.run(block2)
    block2.set_proof_of_work(pow)
    block2.set_hash(pow.get_hash())
    block2.set_timestamp(time.time())

    blockchain.add_block_to_chain(block2)

    txs3 = [
        CoinbaseTransaction(CoinbaseTransaction.generate_default_output(yanis_public_key)),
        Transaction(inputs=[input], outputs=[Output(10, yanis_public_key)], fees=0.0),
    ]

    block3 = Block(Transaction.extract_valid_transactions(txs3, blockchain))
    block3.set_index(3)
    block3.set_prev_hash(block1.get_hash())
    pow = ProofOfWork.run(block3)
    block3.set_proof_of_work(pow)
    block3.set_hash(pow.get_hash())
    block3.set_timestamp(time.time())

    print(genesis_block)
    print(block1)
    print(block2)
    print(block3)

    print("debug")

if __name__ == '__main__':
    main()