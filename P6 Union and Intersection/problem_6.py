import random
import string

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def __repr__(self):
        return str(self.value)


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None # new reference to inserction point

    def __str__(self):
        cur_head = self.head
        out_string = ""
        while cur_head:
            out_string += str(cur_head.value) + " -> "
            cur_head = cur_head.next
        return out_string

    def append(self, value):
        '''Constant time implementation for append method'''
        if self.head is None:
            self.head = Node(value)
            self.tail = self.head
            return
        node = Node(value)
        self.tail.next = node
        self.tail = node

def llist_to_set(llist):
    '''Function to traverse a LinkedList and return a equivalent Python set object.'''
    equiv_set = set()
    node = llist.head
    while node is not None:
        equiv_set.add(node.value)
        node = node.next
    return equiv_set

def iterable_to_llist(iter):
    '''Function to traverse a Python iterable and return a equivalent LinkedList object.'''
    llist = LinkedList()
    for item in iter:
        llist.append(item)
    return llist

def list_to_llist(alist):
    '''Function to traverse a Python list and return a equivalent LinkedList object.'''
    llist = LinkedList()
    for item in alist:
        llist.append(item)
    return llist

def union(llist_1, llist_2):

    # Traverse LL1 and LL2 and store their items into sets
    set_llist_1 = llist_to_set(llist_1)
    set_llist_2 = llist_to_set(llist_2)

    # Apply set UNION operataion over both sets
    result_set = set_llist_1.union(set_llist_2)

    # Traverse retulting set and store its items into a LL
    result_llist = iterable_to_llist(result_set)

    return result_llist

def intersection(llist_1, llist_2):

    # Traverse LL1 and LL2 and store their items into sets
    set_llist_1 = llist_to_set(llist_1)
    set_llist_2 = llist_to_set(llist_2)

    # Apply set INTERSECTION operataion over both sets
    result_set = set_llist_1.intersection(set_llist_2)

    # Traverse retulting set and store its items into a LL
    result_llist = iterable_to_llist(result_set)

    return result_llist


print('\n# Test case 1: Problem statement test case 1')
linked_list_1 = iterable_to_llist([3,2,4,35,6,65,6,4,3,21])
linked_list_2 = iterable_to_llist([6,32,4,9,6,1,11,21,1])
print (union(linked_list_1,linked_list_2))
# It is expected to see the correct union set comprising the elements
# 32, 65, 2, 35, 3, 4, 6, 1, 9, 11 and 21 with no particular order.
print (intersection(linked_list_1,linked_list_2))
# It is expected to the correct intersection set comprising the elements
# 4, 21 and 6 with no particular order.


print('\n# Test case 2: Problem statement test case 2')
linked_list_3 = iterable_to_llist([3,2,4,35,6,65,6,4,3,23])
linked_list_4 = iterable_to_llist([1,7,8,9,11,21,1])
print (union(linked_list_3,linked_list_4))
# It is expected to see the correct union set comprising the elements
# 65, 2, 35, 3, 4, 6, 1, 7, 8, 9, 11, 21 and 23 with no particular order.
print (intersection(linked_list_3,linked_list_4))
# It is expected nothing to be printed since there is no common elements 
# in the two given linked lists.


print('\n# Test case 3: Empty argments (both of them)')
linked_list_5 = iterable_to_llist([])
linked_list_6 = iterable_to_llist([])
print (union(linked_list_5,linked_list_6))
print (intersection(linked_list_5,linked_list_6))
# It is expected nothing to be printed and no execution error.


print('\n# Test case 4: Empty argments (one of them)')
linked_list_7 = iterable_to_llist([5, 4, 3, 2, 1])
linked_list_8 = iterable_to_llist([10, 9, 8, 7, 6])
print (union(linked_list_7,LinkedList()))
print (union(LinkedList(),linked_list_8))
# The result of union between a set with an empty one is the set itself. 
# Expected to see the printed content of that set only.
print (intersection(linked_list_7,LinkedList()))
print (intersection(LinkedList(),linked_list_8))
# Althought, in the same condition, the intersection will result in an empty set.
# Expected to see nothing printed


print('\n# Test case 5: Comparison of some pre-checked random scenarios')
element_9 = random.choices(string.ascii_letters, k=25)
element_10 = random.choices(string.ascii_letters, k=25)
linked_list_9 = iterable_to_llist(element_9)
linked_list_10 = iterable_to_llist(element_10)
if llist_to_set(union(linked_list_9,linked_list_10)) == set(element_9).union(set(element_10)) : print("pass") 
if llist_to_set(intersection(linked_list_9,linked_list_10)) == set(element_9).intersection(set(element_10)) : print("pass")
# Expected to pass the test with non-numeric elements as well.
