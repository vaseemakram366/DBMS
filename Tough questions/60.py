# Skip List Index

import random


class SkipListNode:
    def __init__(self, key, value, level):
        self.key = key
        self.value = value
        self.forward = [None] * (level + 1)


class SkipList:
    def __init__(self, max_level=6, probability=0.5):
        self.max_level = max_level
        self.probability = probability
        self.level = 0

        self.header = SkipListNode(
            None,
            None,
            max_level
        )

    def random_level(self):
        level = 0

        while (
            random.random() < self.probability
            and level < self.max_level
        ):
            level += 1

        return level

    def search(self, key):
        current = self.header

        for level in range(
            self.level,
            -1,
            -1
        ):
            while (
                current.forward[level]
                and current.forward[level].key < key
            ):
                current = current.forward[level]

        current = current.forward[0]

        if current and current.key == key:
            return current.value

        return None

    def insert(self, key, value):
        update = [None] * (
            self.max_level + 1
        )

        current = self.header

        for level in range(
            self.level,
            -1,
            -1
        ):
            while (
                current.forward[level]
                and current.forward[level].key < key
            ):
                current = current.forward[level]

            update[level] = current

        current = current.forward[0]

        if current and current.key == key:
            current.value = value
            return

        new_level = self.random_level()

        if new_level > self.level:
            for level in range(
                self.level + 1,
                new_level + 1
            ):
                update[level] = self.header

            self.level = new_level

        new_node = SkipListNode(
            key,
            value,
            new_level
        )

        for level in range(new_level + 1):
            new_node.forward[level] = (
                update[level].forward[level]
            )

            update[level].forward[level] = new_node

    def delete(self, key):
        update = [None] * (
            self.max_level + 1
        )

        current = self.header

        for level in range(
            self.level,
            -1,
            -1
        ):
            while (
                current.forward[level]
                and current.forward[level].key < key
            ):
                current = current.forward[level]

            update[level] = current

        current = current.forward[0]

        if not current or current.key != key:
            return False

        for level in range(self.level + 1):
            if update[level].forward[level] != current:
                continue

            update[level].forward[level] = (
                current.forward[level]
            )

        while (
            self.level > 0
            and self.header.forward[self.level] is None
        ):
            self.level -= 1

        return True

    def display(self):
        print("\nSkip List")

        for level in range(
            self.level,
            -1,
            -1
        ):
            current = self.header.forward[level]

            values = []

            while current:
                values.append(
                    f"{current.key}:{current.value}"
                )
                current = current.forward[level]

            print(
                f"Level {level}: "
                + " -> ".join(values)
            )


if __name__ == "__main__":
    index = SkipList()

    index.insert(10, "Aman")
    index.insert(20, "Rahul")
    index.insert(30, "Priya")
    index.insert(40, "Neha")
    index.insert(50, "Karan")
    index.insert(60, "Simran")

    index.display()

    print("\nSearch 30:")
    print(index.search(30))

    print("\nSearch 35:")
    print(index.search(35))

    print("\nDelete 30:")
    index.delete(30)

    index.display()

    print("\nSearch 30:")
    print(index.search(30))