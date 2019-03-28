from Block import Block
from GenesisBlock import GenesisBlock
from ProofOfWork import ProofOfWork
from Blockchain import Blockchain
import time

def main():
    blockchain = Blockchain()

    block = GenesisBlock()

    proof_of_work = ProofOfWork.run(block)
    block.set_proof_of_work(proof_of_work)
    block.set_hash(proof_of_work.get_hash())
    block.set_timestamp(time.time())

    blockchain.add_block_to_chain(block)

    print("hash of the mined block:", block.get_hash())
    print("last block hash:", block.get_prev_hash())
    print("nonce:", block.get_proof_of_work().get_nonce())
    print(block.get_timestamp())

    block1 = Block()

    block1.set_prev_hash(blockchain.get_last_block().get_hash())
    proof_of_work = ProofOfWork.run(block1)
    block1.set_proof_of_work(proof_of_work)
    block1.set_hash(proof_of_work.get_hash())
    block1.set_timestamp(time.time())

    blockchain.add_block_to_chain(block1)

    print("hash of the mined block:", block1.get_hash())
    print("last block hash:", block1.get_prev_hash())
    print("nonce:", block1.get_proof_of_work().get_nonce())
    print(block1.get_timestamp())

if __name__ == '__main__':
    main()