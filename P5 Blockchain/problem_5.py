# Udacity Data Structures and Algorithms
# Part 2 - Data Structures
# Project 2 - Problem #5 - Blockchain

from dataclasses import dataclass
import datetime as dt
import time
import hashlib
import random

class Block:

    def __init__(self, previous_hash, data):
        self.previous_hash = previous_hash
        # Data stored in string format
        self.data = str(data)
        # Timestamp considers GMT time zone (UTC±00:00)
        self.timestamp = dt.datetime.now(dt.timezone.utc)
        self.hash = self.calc_hash()

    def calc_hash(self):
        sha = hashlib.sha256()
        sha.update(self.previous_hash.encode('utf-8'))
        sha.update(str(self.timestamp).encode('utf-8'))
        sha.update(self.data.encode('utf-8'))
        return sha.hexdigest()

    def __repr__(self):
        repr_str  = 'block hash: {}'.format(self.hash)
        repr_str += '\nprevious hash: {}'.format(self.previous_hash)
        repr_str += '\ntimestamp: {}'.format(self.timestamp)
        repr_str += '\nblock data: {}'.format(self.data)
        return repr_str 


class Blockchain:

    # Helper class 'Node' for a linked-list blockchain
    @dataclass
    class Node:
        index : int
        block : Block
        previous : Block

    def __init__(self) -> None:
        self.index = 0
        # First block is created with no user data
        # previous hash for genesis block with zeroes
        genesis_block = Block('0'*64, "Genesis Block - First One")
        self.head = self.Node(self.index, genesis_block, None)

    def add_block(self, data):
        # New block always added at the head (top) end of the list
        self.index += 1
        new_block = Block(self.head.block.hash, data)
        new_node = self.Node(self.index, new_block, self.head)
        self.head = new_node

    def __repr__(self):
        node = self.head
        repr_str = ''
        while node is not None:
            repr_str += '\n-------'
            repr_str += '\nblock index: {}\n'.format(node.index)
            repr_str += str(node.block)
            node = node.previous
        repr_str += '\n'
        return repr_str 


if __name__ == "__main__":

    print('\n# Test case 1: An empty chain with only the genesys block')
    my_blockchain = Blockchain()
    print(my_blockchain)
    # It is expected to see only the first block created in the Blockchain class constructor


    print('\n# Test case 2: Some blocks added')
    my_blockchain = Blockchain()
    time.sleep(0.5)
    my_blockchain.add_block('some transactions')
    time.sleep(0.5)
    my_blockchain.add_block('more transactions')
    time.sleep(0.5)
    my_blockchain.add_block('some more transactions')
    print(my_blockchain)
    # It is expected to see three more blocks with a half second leg in timestamp


    print('\n# Test case 3: Couple of more blocks added but with the same data')
    my_blockchain.add_block('same transactions')
    my_blockchain.add_block('same transactions')
    print(my_blockchain)
    # It is expected to see two more blocks at the top with different hashes


    print('\n# Test case 4: A Thousand more blocks added with some random data')
    print('Last five are going to be printed.\n')
    for i in range(1000):
        data = str(random.random())
        my_blockchain.add_block(data)
    
    curr_node = my_blockchain.head
    for _ in range(5):
        print('-------')
        print('block index: {}'.format(curr_node.index))
        print(curr_node.block)
        curr_node = curr_node.previous
    # It is expected to see the last five blocks from index #1001 to #1005
