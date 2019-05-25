class ProofOfWork:

    # TODO: Get difficulty from conf file
    # cursor that we will use to adjust target
    difficulty = 15

    def __init__(self):
        self.__target = ProofOfWork.compute_target()
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
        """Return proof of work of a block to be mined."""
        proof_of_work = ProofOfWork()
        nonce = 0

        while True:
            str_hash = block.compute_hash(nonce)

            if not ProofOfWork.__is_valid_hash(str_hash):
                # increment nonce if generated hash is not valid
                nonce += 1
            else:
                break

        proof_of_work.set_hash(str_hash)
        proof_of_work.set_nonce(nonce)

        return proof_of_work

    @staticmethod
    def __is_valid_hash(str_hash):
        """Return a boolean checking if hash is below the computed target."""
        return int(str_hash, 16) < ProofOfWork.compute_target()

    @staticmethod
    def compute_target():
        """Return the target to reach."""

        # left shift to 1 so: 1 * 2^(256 - difficulty)
        # make a very large number that we can adjust with difficulty
        # more the difficulty is great, more the target will be huge and
        # the winning number hard to find
        target = 1 << (256 - ProofOfWork.difficulty)

        return target

    def serialize(self):
        data = {
            "hash": self.__hash,
            "target": self.__target,
            "nonce": self.__nonce
        }

        return data

    @staticmethod
    def deserialize(dict):
        pow = ProofOfWork()
        pow.set_target(dict['target'])
        pow.set_nonce(dict['nonce'])
        pow.set_hash(dict['hash'])

        return pow