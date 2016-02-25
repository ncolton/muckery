class AVLNode(object):
    @property
    def height(self):
        height = [1]
        if self.left:
            height.append(self.left.height + 1)
        if self.right:
            height.append(self.right.height + 1)
        return max(height)

    @property
    def balance(self):
        left_height = 0
        right_height = 0
        if self.left:
            left_height = self.left.height
        if self.right:
            right_height = self.right.height
        return left_height - right_height

    def __init__(self, data, parent):
        self.data = data
        self.parent = parent
        self.left = None
        self.right = None


class AVLTree(object):
    def add(self, data):
        if not self.root:
            self.root = AVLNode(data, None)
            return
        node = self.root
        while True:
            if data == node.data:
                return
            if data < node.data:
                if not node.left:
                    node.left = AVLNode(data, node)
                    break
                node = node.left
            else # data > node.data:
                if not node.right:
                    node.right = AVLNode(data, node)
                    break
                node = node.right

        if abs(node.balance) > 1:
            self.balance(node)

    def left_rotation(self, root):
        pivot = root.right
        root.right = pivot.left
        root.right.parent = root
        pivot.left = root
        pivot.parent = root.parent
        root.parent = pivot
        if pivot.parent:
            if pivot.parent.right is root:
                pivot.parent.right = pivot
            if pivot.parent.left is root:
                pivot.parent.left = pivot
