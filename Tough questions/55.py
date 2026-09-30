# R-Tree Spatial Index

class Rectangle:
    def __init__(self, x1, y1, x2, y2, data=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.data = data

    def area(self):
        return (self.x2 - self.x1) * (self.y2 - self.y1)

    def intersects(self, other):
        return not (
            self.x2 < other.x1 or
            self.x1 > other.x2 or
            self.y2 < other.y1 or
            self.y1 > other.y2
        )

    def contains(self, other):
        return (
            self.x1 <= other.x1 and
            self.y1 <= other.y1 and
            self.x2 >= other.x2 and
            self.y2 >= other.y2
        )

    def enlargement(self, other):
        new_x1 = min(self.x1, other.x1)
        new_y1 = min(self.y1, other.y1)
        new_x2 = max(self.x2, other.x2)
        new_y2 = max(self.y2, other.y2)

        new_area = (
            (new_x2 - new_x1) *
            (new_y2 - new_y1)
        )

        return new_area - self.area()

    def expand(self, other):
        self.x1 = min(self.x1, other.x1)
        self.y1 = min(self.y1, other.y1)
        self.x2 = max(self.x2, other.x2)
        self.y2 = max(self.y2, other.y2)


class RTreeNode:
    def __init__(self, leaf=True):
        self.leaf = leaf
        self.entries = []
        self.bounds = None

    def update_bounds(self):
        if not self.entries:
            self.bounds = None
            return

        first = self.entries[0]

        if self.leaf:
            self.bounds = Rectangle(
                first.x1,
                first.y1,
                first.x2,
                first.y2
            )
        else:
            self.bounds = Rectangle(
                first.bounds.x1,
                first.bounds.y1,
                first.bounds.x2,
                first.bounds.y2
            )

        for entry in self.entries[1:]:
            rect = entry if self.leaf else entry.bounds
            self.bounds.expand(rect)


class RTree:
    def __init__(self, max_entries=3):
        self.max_entries = max_entries
        self.root = RTreeNode(True)

    def choose_leaf(self, node, rect):
        if node.leaf:
            return node

        best = None
        best_enlargement = float("inf")

        for child in node.entries:
            enlargement = child.bounds.enlargement(rect)

            if enlargement < best_enlargement:
                best_enlargement = enlargement
                best = child

        return self.choose_leaf(best, rect)

    def split(self, node):
        entries = node.entries

        node.entries = [entries[0]]

        sibling = RTreeNode(node.leaf)
        sibling.entries = [entries[1]]

        for entry in entries[2:]:
            target = node if len(node.entries) <= len(sibling.entries) else sibling
            target.entries.append(entry)

        node.update_bounds()
        sibling.update_bounds()

        return sibling

    def insert(self, rect):
        leaf = self.choose_leaf(self.root, rect)

        leaf.entries.append(rect)
        leaf.update_bounds()

        if len(leaf.entries) <= self.max_entries:
            return

        sibling = self.split(leaf)

        if leaf is self.root:
            new_root = RTreeNode(False)
            new_root.entries = [leaf, sibling]
            new_root.update_bounds()
            self.root = new_root

    def search(self, query):
        result = []

        def search_node(node):
            if node.bounds and not node.bounds.intersects(query):
                return

            if node.leaf:
                for rect in node.entries:
                    if rect.intersects(query):
                        result.append(rect.data)
            else:
                for child in node.entries:
                    search_node(child)

        search_node(self.root)

        return result


if __name__ == "__main__":
    tree = RTree(max_entries=3)

    locations = [
        Rectangle(10, 10, 20, 20, "Delhi"),
        Rectangle(30, 30, 40, 40, "Noida"),
        Rectangle(50, 50, 60, 60, "Gurgaon"),
        Rectangle(15, 15, 25, 25, "Faridabad"),
        Rectangle(70, 70, 80, 80, "Jaipur"),
        Rectangle(35, 35, 45, 45, "Agra")
    ]

    for location in locations:
        tree.insert(location)

    query = Rectangle(12, 12, 32, 32)

    result = tree.search(query)

    print("Spatial Query Result:")

    for location in result:
        print(location)