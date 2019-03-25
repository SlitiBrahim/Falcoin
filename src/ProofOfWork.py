class ProofOfWork:

    difficulty = 4

    def __init__(self):
        self.__target = None
        self.__nonce = None

    def get_target(self):
        return self.__target

    def set_target(self, target):
        self.__target = target

    def get_nonce(self):
        return self.__nonce

    def set_nonce(self, nonce):
        self.__nonce = nonce

    @staticmethod
    def run(block):
        proof_of_work = ProofOfWork()

        while True:
            hash = block.compute_hash()
            print("nonce:", block.get_nonce())

            if hash[:ProofOfWork.difficulty] == ("0" * ProofOfWork.difficulty):
                break
            else:
                block.increment_nonce()

        print("hash:", hash)

        return proof_of_work, hash
