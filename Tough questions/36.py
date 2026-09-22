# Trie-Based Full-Text Index

class TrieNode:
    def __init__(self):
        self.children = {}
        self.documents = set()
        self.is_word = False


class FullTextIndex:
    def __init__(self):
        self.root = TrieNode()

    def tokenize(self, text):
        return (
            text.lower()
            .replace(".", "")
            .replace(",", "")
            .split()
        )

    def insert_word(self, word, document_id):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]
            node.documents.add(document_id)

        node.is_word = True

    def add_document(self, document_id, text):
        words = self.tokenize(text)

        for word in words:
            self.insert_word(word, document_id)

    def find_node(self, prefix):
        node = self.root

        for char in prefix.lower():
            if char not in node.children:
                return None

            node = node.children[char]

        return node

    def search_prefix(self, prefix):
        node = self.find_node(prefix)

        if node is None:
            return []

        result = []

        def collect(current, word):
            if current.is_word:
                result.append(
                    (word, sorted(current.documents))
                )

            for char, child in current.children.items():
                collect(child, word + char)

        collect(node, prefix.lower())

        return result

    def search_word(self, word):
        node = self.find_node(word)

        if node is None or not node.is_word:
            return []

        return sorted(node.documents)


index = FullTextIndex()

index.add_document(
    1,
    "database systems use indexing for fast search"
)

index.add_document(
    2,
    "database indexing improves query performance"
)

index.add_document(
    3,
    "distributed database systems process large data"
)

print("Documents containing 'database':")
print(index.search_word("database"))

print("\nPrefix search: 'ind'")
print(index.search_prefix("ind"))

print("\nPrefix search: 'dat'")
print(index.search_prefix("dat"))