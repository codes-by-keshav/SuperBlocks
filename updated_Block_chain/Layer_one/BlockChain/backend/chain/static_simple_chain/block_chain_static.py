from block import Block

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

    def add_block(self, block):
        self.chain.append(block)

    def get_latest_block(self):
        if len(self.chain) == 0:
            return None
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine_block(self, block):
        if len(self.pending_transactions) == 0:
            return False

        # Assuming block is already constructed with transactions
        # In a real implementation, you would construct a block here using pending transactions
        self.add_block(block)
        self.pending_transactions = []
        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.block_header.prevBlockHash != previous_block.block_header.blockHash:
                return False

        return True
