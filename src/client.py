from Block import Block
from ProofOfWork import ProofOfWork

def main():
    block = Block()

    proof_of_work = ProofOfWork.run(block)
    block.set_proof_of_work(proof_of_work)
    block.set_hash(proof_of_work.get_hash())

    print("hash of the mined block: ", block.get_hash())

if __name__ == '__main__':
    main()