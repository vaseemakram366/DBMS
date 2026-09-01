# B+ Tree Implementation

class BPlusTree:
    def __init__(self, order=3):
        self.order = order
        self.root = []

    def search(self, key):
        node = self.root

        while isinstance(node, Node):
            i = 0

            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            node = node.children[i]

        return key in node

    def insert(self, key):
        if not isinstance(self.root, Node):
            self.root.append(key)
            self.root.sort()

            if len(self.root) >= self.order:
                old = self.root

                left = Node()
                right = Node()

                mid = len(old) // 2

                left.keys = old[:mid]
                right.keys = old[mid:]

                root = Node()
                root.keys = [right.keys[0]]
                root.children = [left, right]

                self.root = root

            return

        self._insert(self.root, key)

    def _insert(self, node, key):
        i = 0

        while i < len(node.keys) and key >= node.keys[i]:
            i += 1

        child = node.children[i]

        if isinstance(child, Node):
            self._insert(child, key)

            if len(child.keys) >= self.order:
                self.split(node, i)

        else:
            child.append(key)
            child.sort()

    def split(self, parent, index):
        child = parent.children[index]

        mid = len(child.keys) // 2

        new_node = Node()
        new_node.keys = child.keys[mid:]

        child.keys = child.keys[:mid]

        parent.keys.insert(index, new_node.keys[0])
        parent.children.insert(index + 1, new_node)

    def display(self, node=None, level=0):
        if node is None:
            node = self.root

        if isinstance(node, Node):
            print("  " * level, node.keys)

            for child in node.children:
                self.display(child, level + 1)

        else:
            print("  " * level, node)


class Node:
    def __init__(self):
        self.keys = []
        self.children = []


tree = BPlusTree(3)

for value in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(value)

tree.display()