import time
import hashlib
import json
from block import Block


class Blockchain:
    def __init__(self, mempool):
        self.chain = []
        self.mempool = mempool

    def is_valid_chain(self):
        valid = True
        for index in range(len(self.chain)-1):
            if self.chain[index+1].previous_hash != Block.hash(self.chain[index]):
                valid = False
        for index in range(len(self.chain)):
            if (not self.satisfy_target(Block.hash(self.chain[index]))):
                valid = False
        return valid

    def new_block(self, miner):
        if (len(self.mempool) == 0):
            return None
            print("No transaction to mine")
        else:
            if (len(self.chain) == 0):
                previous_hash = '0000'
            else:
                previous_hash = Block.hash(self.chain[-1])
            block = Block(int(time.time()), len(self.chain),
                          self.mempool[-1], 0,
                          previous_hash,
                          3, miner, miner, True)
        self.mine(block)
        self.chain.append(block)
        self.mempool.pop(-1)
        return block

    def mine(self, block):
        while (block.is_mining == True):
            current_hash = Block.hash(block)
            if (self.satisfy_target(current_hash)):
                block.is_mining = False
            else:
                block.nonce += 1

    @property
    def last_block(self):
        return self.chain[-1]

    def satisfy_target(self, current_hash):
        return (current_hash[0:4] == '0000')
