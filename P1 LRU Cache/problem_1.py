# Udacity Data Structures and Algorithms
# Part 2 - Data Structures
# Project 2 - Problem #1 - LRU Cache

# Script Params
MAX_CAPACITY = 1024
DEFAULT_CAPACITY = 64

class MAP_Node:
    """
    Helper class for LRU Cache. 
    It defines the 'value' structure of each register entry
    """
    
    def __init__(self, value):
        self.value = value # Actual value stored in cache
        self.next = None # Key reference to the next newer register
        self.previous = None # Key reference to the previous older register


class LRU_Cache(object):
    """
    Least Recently Used cache.
    At the limit of a giving cache memory capacity the least
    recently used data gives space the newer ones.
    Interface:
        .get(address) - Returns the data value for a giving address 
                        or -1 if the data is not found.
        .set(address, value) - Uptades the value for a giving address 
                               or includes a new record if not present.
    Params:
        capacity - Cache lenght. Optional argument. Expected type <int> 
                   If received an invalid number or not provided it will 
                   assume the DEFAULT_CAPACITY param.   
                   The capacity also cannot exceed MAX_CAPACITY param.
    """
    
    def __init__(self, capacity=DEFAULT_CAPACITY):

        # Size consistency
        if capacity <= 0:
            capacity = DEFAULT_CAPACITY
        elif capacity > MAX_CAPACITY:
            capacity = MAX_CAPACITY

        # Initialize the LRU structure
        self.capacity = capacity
        # Amount of data registers currently in cache
        self.total_used = 0
        # Initialize the hash map structure
        self.cache_map = {}
        # Key references for head end (most recently accessed register) 
        self.most_recent_addr = None
        # and tail end (least recently accessed register)
        self.least_recent_addr = None


    def get(self, addr):
        if addr in self.cache_map: # Cache hit
            self.update_most_recent(addr)
            return self.cache_map[addr].value
        else: # Cache miss
            return -1
    

    def set(self, addr, value):
        if addr in self.cache_map: # Cache hit
            self.cache_map[addr].value = value
            self.update_most_recent(addr)
        else: # Cache miss
            if self.total_used >= self.capacity:
                self.delete_least_recent()
            self.insert_new_item(addr, value)


    # Helper method
    def update_most_recent(self, key):
        if key == self.most_recent_addr: # Already Up-to-date
            return
        elif key == self.least_recent_addr: # Data is at tail end
            # Detatching the node from tail
            self.least_recent_addr = self.cache_map[self.least_recent_addr].next 
            self.cache_map[self.least_recent_addr].previous = None
            # Attatching the node into head
            self.cache_map[key].previous = self.most_recent_addr
            self.cache_map[key].next = None
            self.cache_map[self.most_recent_addr].next = key
            self.most_recent_addr = key
        else: # Data is somewhere in the middle
            # Detatching the node from a DLL middle part
            self.cache_map[self.cache_map[key].next].previous = self.cache_map[key].previous
            self.cache_map[self.cache_map[key].previous].next = self.cache_map[key].next
            # Attatching the node into DLL head
            self.cache_map[key].previous = self.most_recent_addr
            self.cache_map[key].next = None
            self.cache_map[self.most_recent_addr].next = key
            self.most_recent_addr = key


    # Helper method
    def insert_new_item(self, key, value):
        self.cache_map[key] = MAP_Node(value)
        if self.total_used == 0:
            self.most_recent_addr = key
            self.least_recent_addr = key
        else:
            self.cache_map[key].previous = self.most_recent_addr
            self.cache_map[self.most_recent_addr].next = key
            self.most_recent_addr = key
        self.total_used += 1


    # Helper method
    def delete_least_recent(self):
        key_to_delete = self.least_recent_addr
        # Detatching the node from DLL tail
        self.least_recent_addr = self.cache_map[self.least_recent_addr].next
        self.cache_map[self.least_recent_addr].previous = None
        # Exclude the least accessed register
        del self.cache_map[key_to_delete]
        self.total_used -= 1


    def __repr__(self):
        if self.total_used == 0:
            return "-----------------\nempty\n-----------------\n"
        key = self.least_recent_addr
        reg = self.cache_map[key]
        repr_str = "-----------------\n"
        repr_str += "LRU Transverse from least to most recent\n"
        repr_str += "older\t key:{}, value:{} \t prev:{} \t next:{}\n".format(key, 
                reg.value, reg.previous, reg.next)
        for _ in range(1, self.total_used):
            key = self.cache_map[key].next
            reg = self.cache_map[key]
            repr_str += "\t key:{}, value:{} \t prev:{} \t next:{}\n".format(key, 
                    reg.value, reg.previous, reg.next)
        repr_str += "-----------------\n"
        return repr_str


print("\n\n")
print("# Test Cases")
our_cache = LRU_Cache(5)

print("\n\n")
print("# Test Case 0: Get from empty LRU cache")
print("\nGetting values from key # 1\n")
print(our_cache.get(1))
print(our_cache)
# It is expected to see nothing, since cache has no data.


print("\n\n")
print("# Test Case 1: Fill some data in LRU cache")
print("\nSetting values 100, 200 and 300\n")
our_cache.set(1, 100)
print(our_cache)
our_cache.set(2, 200)
print(our_cache)
our_cache.set(3, 300)
print(our_cache)
# It is expected to see data ordering in sequence (newer to older).


print("\n\n")
print("# Test Case 2: Some cache hits")
print("\nGetting values from 2, 1 and 4 keys\n")
print(our_cache.get(2))
print(our_cache)
print(our_cache.get(1))
print(our_cache)
print(our_cache.get(3))
print(our_cache)
# It is expected to see sequence updates. 
# Less accessed data going to tail end (In direction of least recent).


print("\n\n")
print("# Test Case 3: Putting some more data in cache")
print("\nSetting values 800 and 700\n")
our_cache.set(8, 800)
print(our_cache)
our_cache.set(7, 700)
print(our_cache)
# The cache is expected to be filled to full capacity.


print("\n\n")
print("# Test Case 4: Overwriting data in cache")
print("\nSetting value 900\n")
our_cache.set(9, 900)
print(our_cache)
# It is expected that the least accessed register will be deleted and
# the new value 900 will be accommodated at the beginning of the sequence.


print("\n\n")
print("# Test Case 5: Getting older data in cache")
print("\nGetting register from key #2\n")
print(our_cache.get(2))
print(our_cache)
# It is expected to see a cache miss since the value 200 (address #2) is 
# no longer available in cache. That's because it was deleted to make room 
# for value 900 in tast case 4.


print("\n\n")
print("# Test Case 6: Getting older data in cache")
print("\nGetting register from key #1\n")
print(our_cache.get(1))
print(our_cache)
# It is expected to see a cache hit and the value 100 jumping into head end 
# (most recent) in sequence.


print("\n\n")
print("# Test Case 7: Cache with invalid sizes")
our_new_cache = LRU_Cache(-1)
print("\nCache size: {}\n".format(our_new_cache.capacity))
# Expected to see the default value for invalid numbers

our_new_cache = LRU_Cache()
print("\nCache size: {}\n".format(our_new_cache.capacity))
# Expected to see the default value if not given 


print("\n\n")
print("# Test Case 8: Too high value argument")
our_new_cache = LRU_Cache(1048576)
print("\nCache size: {}\n".format(our_new_cache.capacity))
# Expected to see the MAX_CAPACITY parameter value for numbers that are too high

