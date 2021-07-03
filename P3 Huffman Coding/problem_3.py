# Udacity Data Structures and Algorithms
# Part 2 - Data Structures
# Project 2 - Problem #3 - Huffman Coding

import sys
from dataclasses import dataclass

# Binary Minimum Heap structure helper class farther used 
# for creating a minimum frequency priority queue.
class Min_Heap:
    
    # Helper data class for heap node
    @dataclass
    class Node:
        data : object
        frequency : int

    def __init__(self):
        # List based heap
        self.heap = []
        self.head = None
        self.tail = None
 
    def size(self):
        return len(self.heap)

    def is_empty(self):
        return True if self.size() == 0 else False

    def push(self, data, frequency):
        if self.is_empty(): 
            self.head, self.tail = 0, 0
        else:
            self.tail += 1 
        # A new element is initially inserted at the tail end...
        self.heap.append(self.Node(data, frequency))
        # ...so it needs to be repositioned to meet heap constraints.
        self.sift_up(self.tail)

    def pop(self):
        if self.is_empty() : return None
        if self.size() == 1 : 
            self.head = None
            self.tail = None
            return self.heap.pop() 
        self.tail -= 1 
        node = self.heap[0]
        # As an element is always popped from the head end, the last 
        # heap element at tail is swapped to the head...
        self.heap[0] = self.heap.pop()
        # ...so it needs to be repositioned to meet heap constraints.
        self.sift_down(self.head)
        return node

    def sift_up(self, i):
        parent = self.parent(i)
        if parent is not None:
            if self.heap[i].frequency < self.heap[parent].frequency:
                self.swap_nodes(i, parent)
                self.sift_up(parent)

    def sift_down(self, i):
        left, right = self.left(i), self.right(i)
        if left and not right:
            if self.heap[i].frequency > self.heap[left].frequency:
                self.swap_nodes(i, left)
                self.sift_down(left)
        elif left and right:
            if self.heap[left].frequency <= self.heap[right].frequency:
                if self.heap[i].frequency > self.heap[left].frequency:
                    self.swap_nodes(i, left)
                    self.sift_down(left)
            elif self.heap[right].frequency < self.heap[left].frequency:
                if self.heap[i].frequency > self.heap[right].frequency:
                    self.swap_nodes(i, right)
                    self.sift_down(right)

    def parent(self, i):
        if i == 0 : return None
        pos = (i - 1) // 2
        return pos
    
    def left(self, i):
        pos = i * 2 + 1
        return pos if pos < self.size() else None
    
    def right(self, i):
        pos = i * 2 + 2
        return pos if pos < self.size() else None

    def swap_nodes(self, a, b):
        auxiliary_node = self.heap[a]
        self.heap[a] = self.heap[b]
        self.heap[b] = auxiliary_node


# Helper class for creating and managing a Huffman tree
@dataclass
class Huffman_Tree:
    @dataclass
    class Inner_Node:
        left : object
        right : object
    @dataclass
    class Leaf_Node:
        char : object
        frequency : object
    root : object


def huffman_encoding(data):
    '''
    Huffman encoder that encodes a data string into a bit
    sequence a generates a corresponding Huffman tree.
    params:     
        data : original data string
    result:
        encoded_data : bit-like encoded data string
        tree : Huffman_Tree class object
    '''

    # Exceptional Case - No data to compress
    if data == "" : return "", Huffman_Tree(None)      

    # Create and fill a Char:Frequency Map
    char_frequency = dict()
    for char in data:
        char_frequency[char] = char_frequency.get(char, 0) + 1

    # Create and fill a min-heap based Priority List
    priority_queue = Min_Heap()
    for char, freq in char_frequency.items():
        priority_queue.push(char, freq)

    # Construct a Huffman Tree
    tree = Huffman_Tree(None)

    if priority_queue.size() == 1:
        # Exceptional Case - Data containing only one symbol
        node = priority_queue.pop()
        huffman_node = Huffman_Tree.Leaf_Node(node.data, node.frequency)
        tree.root = Huffman_Tree.Inner_Node(huffman_node, None)
    
    else:

        # Traverse the Priority List to construct a Huffman Tree
        while True:

            # Pops the first item from priority queue.
            node1 = priority_queue.pop()

            # At some point the queue will be filled with eather original Min_Heap
            # and Huffman_Tree node references. In here the differences as addressed.
            if type(node1.data) is not Huffman_Tree.Inner_Node:
                huffman_node1 = Huffman_Tree.Leaf_Node(node1.data, node1.frequency)
            else:
                huffman_node1 = Huffman_Tree.Inner_Node(node1.data.left, node1.data.right)

            if priority_queue.is_empty(): 
                # If the lest item was popped from the queue,
                # it is assigned to the Huffman tree as root.
                tree.root = huffman_node1
                break
            
            # Pops second item.
            node2 = priority_queue.pop()

            if type(node2.data) is not Huffman_Tree.Inner_Node:
                huffman_node2 = Huffman_Tree.Leaf_Node(node2.data, node2.frequency)
            else:
                huffman_node2 = Huffman_Tree.Inner_Node(node2.data.left, node2.data.right)
            
            # Creates a combined node and pushes it back to the queue
            combined_node = Huffman_Tree.Inner_Node(huffman_node1, huffman_node2)
            combined_freq = node1.frequency + node2.frequency 
            priority_queue.push(combined_node, combined_freq)

    # Visit Huffman Tree nodes recursively and build up a Huffman Code Table 
    huffman_code_table = dict()
    def visit_node(node, acc_code=''):
        if type(node) is Huffman_Tree.Leaf_Node:
            huffman_code_table[node.char] = acc_code
        if type(node) is Huffman_Tree.Inner_Node:
            visit_node(node.left, acc_code + '0')
            visit_node(node.right, acc_code + '1')
    visit_node(tree.root)

    # Encode Data
    encoded_data = ""
    for char in data:
        encoded_data += huffman_code_table[char]

    return encoded_data, tree


def huffman_decoding(encoded_data, tree):
    '''
    Huffman decoder that extracts from encoded data the
    original string sequence based on a given Huffman Tree.
    params:     
        encoded_data : bit-like encoded data string
        tree : Huffman_Tree class object
    result:
        decoded_data : original data string
    '''

    # Parse encoded data and decode it based on the Huffman Tree walk
    decoded_data = ''
    node = tree.root
    for bit in encoded_data:
        # Walks left or right based on current bit code
        if bit == '0':
            node = node.left
        else:
            node = node.right
        # If a leaf is reached it is possible to match the code so far
        # parsed with its corresponding character
        if type(node) is Huffman_Tree.Leaf_Node:
            # Updates decoded data
            decoded_data += node.char
            # Gets back to Huffman tree root
            node = tree.root

    return decoded_data


if __name__ == "__main__":

    def evaluate(description, original_data, limit=None):
        '''Helper funcion to evaluate Huffman's code problem'''
        print ("\n", description)
        print ("The size of the data: {} bytes".format(sys.getsizeof(original_data)))
        if limit:
            print ("The content of the data:\n\'{} ... \'".format(original_data[:limit]))
        else:
            print ("The content of the data:\n\'{}\'".format(original_data))

        encoded_data, tree = huffman_encoding(original_data)
        if len(encoded_data) != 0:
            print ("The size of the encoded data: {} bytes".format(sys.getsizeof(int(encoded_data, base=2))))
        else:
            print ("The size of the encoded data: 0 bytes")
        if limit:
            print ("The content of the encoded data:\n\'{} ... \'".format(encoded_data[:limit]))
        else:
            print ("The content of the encoded data:\n\'{}\'".format(encoded_data))

        decoded_data = huffman_decoding(encoded_data, tree)
        if limit:
            print ("The content of the decoded data:\n\'{} ... \'".format(decoded_data[:limit]))
        else:
            print ("The content of the decoded data:\n\'{}\'".format(decoded_data))
        result = True if original_data == decoded_data else False
        print ("Are original and decoded data equal?: {}\n\n".format(result))

    # Test Case 1: Original problem phrase
    a_great_sentence = "The bird is the word"
    evaluate("# Test Case 1: Original problem phrase", a_great_sentence)

    # Test Case 2: Tiny phrase
    a_character = "a"
    evaluate("# Test Case 2: Tiny phrases", a_character)

    # Test Case 3: Empty phrase
    nothing = ""
    evaluate("# Test Case 3: Empty phrase", nothing)

    # Test Case 4: Phrases with only one symbol
    a_sentence = "bbbbbbbbbb"
    evaluate("# Test Case 4: Phrases with only one symbol", a_sentence)

    # Test Case 5: A real file. In fact 'this file'
    # f = open("2_Project/P3 Huffman Coding/problem_3.py", "r")
    f = open("problem_3.py", "r")
    file_content = f.read()
    evaluate("# Test Case 5: A real file. In fact 'this script file'", file_content, 400)
