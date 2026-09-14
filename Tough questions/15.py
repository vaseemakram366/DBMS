# B+ Tree with Insert + Delete
class Node:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None


class BPlusTree:
    def __init__(self, order=4):
        self.order = order
        self.root = Node(leaf=True)

    def search(self, key):
        node = self.root

        while not node.leaf:
            i = 0

            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            node = node.children[i]

        return key in node.keys

    def insert(self, key):
        root = self.root

        if len(root.keys) == self.order - 1:
            new_root = Node()
            new_root.children.append(root)
            self.root = new_root

            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)

        else:
            self._insert_non_full(root, key)

    def _insert_non_full(self, node, key):
        if node.leaf:
            i = len(node.keys) - 1
            node.keys.append(None)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            node.keys[i + 1] = key
            return

        i = len(node.keys) - 1

        while i >= 0 and key < node.keys[i]:
            i -= 1

        i += 1

        if len(node.children[i].keys) == self.order - 1:
            self._split_child(node, i)

            if key >= node.keys[i]:
                i += 1

        self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, index):
        child = parent.children[index]

        new_node = Node(child.leaf)

        mid = len(child.keys) // 2

        if child.leaf:
            new_node.keys = child.keys[mid:]
            child.keys = child.keys[:mid]

            new_node.next = child.next
            child.next = new_node

            parent.keys.insert(
                index,
                new_node.keys[0]
            )

        else:
            promoted = child.keys[mid]

            new_node.keys = child.keys[mid + 1:]
            child.keys = child.keys[:mid]

            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]

            parent.keys.insert(index, promoted)

        parent.children.insert(
            index + 1,
            new_node
        )

    def delete(self, key):
        node = self.root

        while not node.leaf:
            i = 0

            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            node = node.children[i]

        if key not in node.keys:
            return False

        node.keys.remove(key)

        self._update_parent_keys(self.root)

        return True

    def _update_parent_keys(self, node):
        if node.leaf:
            return

        for i, child in enumerate(node.children):
            self._update_parent_keys(child)

            if i > 0 and child.keys:
                node.keys[i - 1] = child.keys[0]

    def display(self):
        level = [self.root]

        while level:
            next_level = []

            for node in level:
                print(node.keys, end="   ")

                if not node.leaf:
                    next_level.extend(node.children)

            print()
            level = next_level

    def display_leaves(self):
        node = self.root

        while not node.leaf:
            node = node.children[0]

        while node:
            print(node.keys, end=" -> ")
            node = node.next

        print("None")


tree = BPlusTree(4)

values = [
    10, 20, 5, 6, 12,
    30, 7, 17, 25, 40,
    3, 8, 15
]

for value in values:
    tree.insert(value)

print("B+ Tree:")
tree.display()

print("\nLeaf Level:")
tree.display_leaves()

print("\nSearch 17:", tree.search(17))
print("Search 100:", tree.search(100))

tree.delete(17)

print("\nAfter deleting 17:")
tree.display()

print("\nLeaf Level:")
tree.display_leaves()