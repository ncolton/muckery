# Things I didn't do properly:
# * Failed to inherit from object
# * Don't need parenthesis around the 'True' for the while statement's conditional
# * Forgetting to put the damned colons after the method definition!
# * Forgetting to put the damned colons after conditionals!

import pytest


class NotFound(Exception):
    pass


class Node(object):
    def __init__(self, data=None):
        self.left = None
        self.right = None
        self.data = data


class BinaryTree(object):
    def __init__(self):
        self.root = None

    def search(self, n):
        '''
        return node containing n from tree, raise ex
        '''
        if self.root is None:
            raise NotFound('%s not present in tree' % n)
        node = self.root
        while True:
            if node.data == n:
                return node
            if node.data > n:
                if node.left is None:
                    raise NotFound('%s not present in tree' % n)
                node = node.left
            else:  # node.data < n
                if node.right is None:
                    raise NotFound('%s not present in tree' % n)
                node = node.right

    def insert(self, n):
        '''
        insert a value into the tree

        :return: True if value was added, False if it already exists in the tree
        '''
        if self.root is None:
            self.root = Node(n)
            return True

        node = self.root
        while True:
            if node.data == n:
                return False
            if node.data > n:
                if node.left is None:
                    node.left = Node(n)
                    return True
                node = node.left
            else:  # node.data < n
                if node.right is None:
                    node.right = Node(n)
                    return True
                node = node.right

    def pre_order(self, node=None):
        if not node:
            node = self.root
        values = [node.data]
        if node.left:
            values.extend(self.pre_order(node.left))
        if node.right:
            values.extend(self.pre_order(node.right))
        return values

    def in_order(self, node=None):
        if not node:
            node = self.root
        values = []
        if node.left:
            values.extend(self.in_order(node.left))
        values.append(node.data)
        if node.right:
            values.extend(self.in_order(node.right))
        return values

    def post_order(self, node=None):
        if not node:
            node = self.root
        values = []
        if node.left:
            values.extend(self.post_order(node.left))
        if node.right:
            values.extend(self.post_order(node.right))
        values.append(node.data)
        return values


def test_init_has_no_root():
    t = BinaryTree()
    assert t.root is None


def test_insert_first_value_has_value_in_root_node():
    t = BinaryTree()
    t.insert(112)
    assert t.root.data is 112


def test_insert_value_less_than_root_is_roots_left_child():
    t = BinaryTree()
    t.insert(5)
    t.insert(3)
    assert t.root.left.data == 3


def test_insert_value_greater_than_root_is_roots_right_child():
    t = BinaryTree()
    t.insert(5)
    t.insert(7)
    assert t.root.right.data == 7


def test_insert_root_left_left():
    t = BinaryTree()
    t.insert(5)
    t.insert(3)
    t.insert(1)
    assert t.root.left.data == 3
    assert t.root.left.left.data == 1

def test_insert_root_left_right():
    t = BinaryTree()
    t.insert(5)
    t.insert(3)
    t.insert(4)
    assert t.root.left.data == 3
    assert t.root.left.right.data == 4


def test_insert_root_right_left():
    t = BinaryTree()
    t.insert(5)
    t.insert(9)
    t.insert(7)
    assert t.root.right.data == 9
    assert t.root.right.left.data == 7

def test_insert_root_right_right():
    t = BinaryTree()
    t.insert(5)
    t.insert(9)
    t.insert(11)
    assert t.root.right.data == 9
    assert t.root.right.right.data == 11


def test_search_raises_exception_for_empty_tree():
    t = BinaryTree()
    with pytest.raises(NotFound):
        t.search(2)


def test_search():
    t = BinaryTree()
    for number in [7, 3, 1, 5, 11, 9, 13]:
        t.insert(number)
    assert t.search(7) is t.root
    assert t.search(3) is t.root.left
    assert t.search(1) is t.root.left.left
    assert t.search(5) is t.root.left.right
    assert t.search(11) is t.root.right
    assert t.search(9) is t.root.right.left
    assert t.search(13) is t.root.right.right


def test_pre_order_traversal():
    t = BinaryTree()
    for number in [7, 3, 1, 5, 11, 9, 13]:
        t.insert(number)
    assert t.pre_order() == [7, 3, 1, 5, 11, 9, 13]


def test_in_order_traversal():
    t = BinaryTree()
    for number in [7, 3, 1, 5, 11, 9, 13]:
        t.insert(number)
    assert t.in_order() == [1, 3, 5, 7, 9, 11, 13]


def test_post_order_traversal():
    t = BinaryTree()
    for number in [7, 3, 1, 5, 11, 9, 13]:
        t.insert(number)
    assert t.post_order() == [1, 5, 3, 9, 13, 11, 7]


def test_breadth_first_traversal():
    t = BinaryTree()
    for number in [7, 3, 1, 5, 11, 9, 13]:
        t.insert(number)
    assert t.breadth_first() == [7, 3, 11, 1, 5, 9, 13]
