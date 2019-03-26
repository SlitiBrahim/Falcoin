class ProofOfWork:

    difficulty = 3

    def __init__(self):
        # TODO: Implement target
        self.__target = None
        self.__nonce = None
        self.__hash = None

    def get_target(self):
        return self.__target

    def set_target(self, target):
        self.__target = target

    def get_nonce(self):
        return self.__nonce

    def set_nonce(self, nonce):
        self.__nonce = nonce

    def get_hash(self):
        return self.__hash

    def set_hash(self, str_hash):
        self.__hash = str_hash

    @staticmethod
    def run(block):
        proof_of_work = ProofOfWork()
        nonce = 0

        while True:
            print("nonce:", nonce)
            str_hash = block.compute_hash(nonce)

            if not ProofOfWork.__is_valid_hash(str_hash):
                nonce += 1
            else:
                break

        proof_of_work.set_hash(str_hash)
        proof_of_work.set_nonce(nonce)

        return proof_of_work

    @staticmethod
    def __is_valid_hash(str_hash):
        # TODO: Change it with: "< difficulty"
        return str_hash[:ProofOfWork.difficulty] == ("0" * ProofOfWork.difficulty)
