from Block import Block
from GenesisBlock import GenesisBlock
from ProofOfWork import ProofOfWork
from Blockchain import Blockchain
import time

def main():
    blockchain = Blockchain()

    print(blockchain.get_chain())

    print(blockchain.get_chain())

    exit()

    block = GenesisBlock()

    proof_of_work = ProofOfWork.run(block)
    block.set_proof_of_work(proof_of_work)
    block.set_hash(proof_of_work.get_hash())
    block.set_timestamp(time.time())

    print("hash of the mined block:", block.get_hash())
    print("nonce:", block.get_proof_of_work().get_nonce())
    print(block.get_timestamp())

if __name__ == '__main__':
    main()