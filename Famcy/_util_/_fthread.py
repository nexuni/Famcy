import threading
import enum
from flask import session, g, request

class FPriority(enum.IntEnum):
    """
    This is the enum for defining
    Famcy module priorities. 
    """
    Standard = 1
    Error = 2
    Critical = 3

class FamcyPageQueue:
    def __init__(self):
        super(FamcyPageQueue, self).__init__()
        self.BackgroundQueueDict = {}

    # def init_queue(self, _id):
    #     session["BackgroundQueueDict"] = FamcyPriorityQueue()

    def add(self, value, priority):
        if isinstance(value.target, list):
            _page = value.target[0].find_page_parent(value.target[0])
        else:
            _page = value.target.find_page_parent(value.target)
        route_name = _page.route.replace("/", "_")[1:]
        # print('route_name: ', route_name)

        session[route_name+"BackgroundQueueDict"].add(value, priority)
        # print("add", session[route_name+"BackgroundQueueDict"])

class FamcyPriorityQueue:
    """
    This PQ is adopted from:
    https://github.com/fafl/priority-queue.git
    """
    def __init__(self):

        # List of items, flattened binary heap. The first element is not used.
        # Each node is a tuple of (value, priority, insert_counter)
        self.nodes = [None]  # first element is not used

        # Current state of the insert counter
        self.insert_counter = 0          # tie breaker, keeps the insertion order

    # Comparison function between two nodes
    # Higher priority wins
    # On equal priority: Lower insert counter wins
    def _is_higher_than(self, a, b):
        return b[1] < a[1] or (a[1] == b[1] and a[2] < b[2])

    # Move a node up until the parent is bigger
    def _heapify(self, new_node_index):
        while 1 < new_node_index:
            new_node = self.nodes[new_node_index]
            parent_index = new_node_index // 2
            parent_node = self.nodes[parent_index]

            # Parent too big?
            if self._is_higher_than(parent_node, new_node):
                break

            # Swap with parent
            tmp_node = parent_node
            self.nodes[parent_index] = new_node
            self.nodes[new_node_index] = tmp_node

            # Continue further up
            new_node_index = parent_index

    # Add a new node with a given priority
    def add(self, value, priority):
        new_node_index = len(self.nodes)
        self.insert_counter += 1
        self.nodes.append((value, priority, self.insert_counter))

        # Move the new node up in the hierarchy
        self._heapify(new_node_index)

    # Return the top element
    def peek(self):
        if len(self.nodes) == 1:
            return None
        else:
            return self.nodes[1][0]

    # Return the bottom element
    def bottom(self):
        if len(self.nodes) == 1:
            return None
        else:
            return self.nodes[-1][0]

    # Remove the top element and return it
    def pop(self):
        if len(self.nodes) == 1:
            raise LookupError("Heap is empty")

        result = self.nodes[1][0]
        
        # Move empty space down
        empty_space_index = 1
        while empty_space_index * 2 < len(self.nodes):

            left_child_index = empty_space_index * 2
            right_child_index = empty_space_index * 2 + 1

            # Left child wins
            if (
                len(self.nodes) <= right_child_index
                or self._is_higher_than(self.nodes[left_child_index], self.nodes[right_child_index])
            ):
                self.nodes[empty_space_index] = self.nodes[left_child_index]
                empty_space_index = left_child_index

            # Right child wins
            else:
                self.nodes[empty_space_index] = self.nodes[right_child_index]
                empty_space_index = right_child_index
        
        # Swap empty space with the last element and heapify
        last_node_index = len(self.nodes) - 1
        self.nodes[empty_space_index] = self.nodes[last_node_index]
        self._heapify(empty_space_index)
        
        # Throw out the last element
        self.nodes.pop()

        return result

class FamcyThread(threading.Thread):
	"""
	Represent the famcy thread implementation. 
	Currently it's just inherit from the
	basic threading Thread class. 
	"""
	def __init__(self, *args, **kwargs):
		super(FamcyThread, self).__init__(*args, **kwargs)

