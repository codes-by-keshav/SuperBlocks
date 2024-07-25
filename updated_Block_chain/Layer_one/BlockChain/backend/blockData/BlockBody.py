class BlockBody:
    def __init__(self, height, blocksize, blockheader, txcount, txs, data_size_limit, form,
                 user_transaction_number, priority, multichainable, block_number, mining_rate,
                 interaction_region, encryption_dynamic_hash, block_type, lifetime, data, scheduled_time):
        self._height = height
        self._blocksize = blocksize
        self._blockheader = blockheader
        self._txcount = txcount
        self._txs = txs
        self._data_size_limit = data_size_limit
        self._form = form
        self._user_transaction_number = user_transaction_number
        self._priority = priority
        self._multichainable = multichainable
        self._block_number = block_number
        self._mining_rate = mining_rate
        self._interaction_region = interaction_region
        self._encryption_dynamic_hash = encryption_dynamic_hash
        self._block_type = block_type
        self._lifetime = lifetime
        self._data = data
        self._scheduled_time = scheduled_time
