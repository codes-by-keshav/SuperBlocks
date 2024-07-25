from block_header import BlockHeader
from block_body import BlockBody

class Block:
    def __init__(self, block_header, block_body):
        self.block_header = block_header
        self.block_body = block_body

    def calculate_block_hash(self):
        # Code to calculate block hash goes here
        pass
