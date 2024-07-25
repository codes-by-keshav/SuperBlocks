class BlockHeader:
    def __init__(self, version, prevBlockHash, merkleRoot, timestamp, bits, from_account, to_account,
                 nounce, timestamp_info, hash_of_previous, encrypted_ip, user_points, supply):
        self.version = version
        self.prevBlockHash = prevBlockHash
        self.merkleRoot = merkleRoot
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nounce
        self.blockHash = ""  # This will be calculated later
        self._from_account = from_account
        self._to_account = to_account
        self._timestamp = timestamp_info
        self._hash_of_previous = hash_of_previous
        self._encrypted_ip = encrypted_ip
        self._user_points = user_points
        self._supply = supply
