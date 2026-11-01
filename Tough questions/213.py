# B+ Tree Index Simulator


from bisect import bisect_left, insort


class Leaf:
    def __init__(self):
        self.keys = []
        self.values = []
        self.next = None


class BPlusTree:
    def __init__(self, order=3):
        self.order = order
        self.root = Leaf()
        self.leaves = [self.root]

    def insert(self, key, value):
        leaf = self.root

        while not isinstance(leaf, Leaf):
            i = bisect_left(leaf.keys, key)
            leaf = leaf.children[i]

        i = bisect_left(leaf.keys, key)

        if i < len(leaf.keys) and leaf.keys[i] == key:
            leaf.values[i] = value
            return

        leaf.keys.insert(i, key)
        leaf.values.insert(i, value)

        if len(leaf.keys) > self.order:
            mid = len(leaf.keys) // 2

            new_leaf = Leaf()
            new_leaf.keys = leaf.keys[mid:]
            new_leaf.values = leaf.values[mid:]

            leaf.keys = leaf.keys[:mid]
            leaf.values = leaf.values[:mid]

            new_leaf.next = leaf.next
            leaf.next = new_leaf

            self.leaves.append(new_leaf)
            self.leaves.sort(key=lambda item: item.keys[0])

            self.rebuild_internal_tree()

    def rebuild_internal_tree(self):
        # Rebuild a search hierarchy over the ordered leaves.
        nodes = self.leaves[:]

        while len(nodes) > 1:
            parents = []

            for start in range(0, len(nodes), self.order + 1):
                children = nodes[start:start + self.order + 1]

                if len(children) == 1:
                    parents.append(children[0])
                    continue

                parent = type("InternalNode", (), {})()
                parent.children = children
                parent.keys = [
                    child.keys[0] for child in children[1:]
                ]
                parents.append(parent)

            nodes = parents

        self.root = nodes[0]

    def search(self, key):
        node = self.root

        while not isinstance(node, Leaf):
            i = bisect_left(node.keys, key)
            node = node.children[i]

        i = bisect_left(node.keys, key)

        if i < len(node.keys) and node.keys[i] == key:
            return node.values[i]

        return None

    def range_query(self, low, high):
        result = []

        leaf = self.root
        while not isinstance(leaf, Leaf):
            leaf = leaf.children[bisect_left(leaf.keys, low)]

        while leaf:
            for key, value in zip(leaf.keys, leaf.values):
                if key > high:
                    return result
                if key >= low:
                    result.append((key, value))

            leaf = leaf.next

        return result


tree = BPlusTree(order=3)

for key, value in [
    (10, "Aman"),
    (20, "Riya"),
    (5, "Karan"),
    (6, "Neha"),
    (12, "Vikas"),
    (30, "Sara"),
    (7, "Mohan")
]:
    tree.insert(key, value)

print("Search 12:", tree.search(12))
print("Search 15:", tree.search(15))
print("Range 6 to 20:", tree.range_query(6, 20))
