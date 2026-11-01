# B-Tree Index Simulator


class BTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.keys = []
        self.children = []


class BTree:
    def __init__(self, degree=2):
        self.root = BTreeNode()
        self.t = degree

    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0

        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.leaf:
            return False

        return self.search(key, node.children[i])

    def split_child(self, parent, index):
        t = self.t
        full = parent.children[index]
        new_node = BTreeNode(full.leaf)

        middle_key = full.keys[t - 1]

        new_node.keys = full.keys[t:]
        full.keys = full.keys[:t - 1]

        if not full.leaf:
            new_node.children = full.children[t:]
            full.children = full.children[:t]

        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, middle_key)

    def insert(self, key):
        root = self.root

        if len(root.keys) == 2 * self.t - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(root)
            self.split_child(new_root, 0)
            self.root = new_root

        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(0)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            node.keys[i + 1] = key
            return

        while i >= 0 and key < node.keys[i]:
            i -= 1

        i += 1

        if len(node.children[i].keys) == 2 * self.t - 1:
            self.split_child(node, i)

            if key > node.keys[i]:
                i += 1

        self._insert_non_full(node.children[i], key)


tree = BTree(degree=2)

for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    tree.insert(key)

for key in [6, 15, 17, 30]:
    print(f"Search {key}: {tree.search(key)}")
