from blockchain import Block
from blockchain import GenesisBlock
from blockchain import ProofOfWork
from blockchain import Blockchain
from blockchain import Transaction
from blockchain import CoinbaseTransaction
from blockchain import Input
from blockchain import Output
from blockchain import crypto
from blockchain import utils
from db import Hydrator
from db import Repository
import time
import os

def main():
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

    input = Input(txs[0].get_hash(), 0, txs[0].get_output(index=0))
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

    input = Input(txs1[1].get_hash(), 0, txs1[1].get_output(index=0))
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

    blockchain.add_block_to_chain(block3)

    # ========= DB =========

    abs_db_path = os.path.abspath('../db/blockchain.db')
    repository = Repository()
    repository.connect_to_db(abs_db_path)

    # repository.add(block2)

    block_docs = repository.get_all_docs()
    block_objs = list(map(lambda doc: Hydrator.hydrate_block(doc), block_docs))

    print("debug")

if __name__ == '__main__':
    main()