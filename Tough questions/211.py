# Binary Search Tree Index


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class BSTIndex:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        self.root = self._insert(self.root, key, value)

    def _insert(self, node, key, value):
        if node is None:
            return Node(key, value)

        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value

        return node

    def search(self, key):
        current = self.root

        while current:
            if key == current.key:
                print(f"Found {key}: {current.value}")
                return current.value
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        print(f"Key {key} not found")
        return None

    def inorder(self, node=None):
        if node is None:
            node = self.root
            if node is None:
                return

        if node.left:
            self.inorder(node.left)

        print(node.key, end=" ")

        if node.right:
            self.inorder(node.right)


index = BSTIndex()

index.insert(50, "Aman")
index.insert(30, "Riya")
index.insert(70, "Karan")
index.insert(20, "Neha")
index.insert(40, "Vikas")

index.search(40)
index.search(60)

print("Sorted keys:", end=" ")
index.inorder()
print()
