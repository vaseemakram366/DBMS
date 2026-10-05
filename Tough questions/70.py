# Inverted Index with Positional Phrase Search

import re
from collections import defaultdict


class PositionalInvertedIndex:
    def __init__(self):
        self.index = defaultdict(lambda: defaultdict(list))

    def tokenize(self, text):
        return re.findall(r"\b\w+\b", text.lower())

    def add_document(self, doc_id, text):
        words = self.tokenize(text)

        for position, word in enumerate(words):
            self.index[word][doc_id].append(position)

    def search_word(self, word):
        word = word.lower()

        if word not in self.index:
            return []

        return list(self.index[word].keys())

    def search_phrase(self, phrase):
        words = self.tokenize(phrase)

        if not words:
            return []

        first_word = words[0]

        if first_word not in self.index:
            return []

        result = []

        for doc_id, positions in self.index[first_word].items():

            for start in positions:
                matched = True

                for offset, word in enumerate(words[1:], 1):
                    if doc_id not in self.index.get(word, {}):
                        matched = False
                        break

                    if start + offset not in self.index[word][doc_id]:
                        matched = False
                        break

                if matched:
                    result.append(doc_id)
                    break

        return result

    def display(self):
        for word, documents in sorted(self.index.items()):
            print(word, dict(documents))


index = PositionalInvertedIndex()

index.add_document(
    1,
    "database systems are very important"
)

index.add_document(
    2,
    "advanced database systems use indexing"
)

index.add_document(
    3,
    "database indexing improves query performance"
)

index.add_document(
    4,
    "distributed systems use database technology"
)


print("Documents containing 'database':")
print(index.search_word("database"))

print("\nDocuments containing phrase 'database systems':")
print(index.search_phrase("database systems"))

print("\nDocuments containing phrase 'query performance':")
print(index.search_phrase("query performance"))

print("\nInverted Index:")
index.display()