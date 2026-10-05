# Dictionary Encoding + Run-Length Encoding Storage Engine

class DictionaryEncoder:
    def __init__(self):
        self.value_to_id = {}
        self.id_to_value = {}

    def encode(self, values):
        encoded = []

        for value in values:
            if value not in self.value_to_id:
                index = len(self.value_to_id)

                self.value_to_id[value] = index
                self.id_to_value[index] = value

            encoded.append(self.value_to_id[value])

        return encoded

    def decode(self, encoded):
        return [
            self.id_to_value[value]
            for value in encoded
        ]


class RunLengthEncoder:
    def encode(self, values):
        if not values:
            return []

        result = []

        current = values[0]
        count = 1

        for value in values[1:]:
            if value == current:
                count += 1
            else:
                result.append((current, count))

                current = value
                count = 1

        result.append((current, count))

        return result

    def decode(self, encoded):
        result = []

        for value, count in encoded:
            result.extend([value] * count)

        return result


class CompressedColumn:
    def __init__(self, values):
        self.original_size = len(values)

        self.dictionary = DictionaryEncoder()
        self.rle = RunLengthEncoder()

        dictionary_encoded = self.dictionary.encode(values)

        self.data = self.rle.encode(dictionary_encoded)

    def decode(self):
        dictionary_ids = self.rle.decode(self.data)

        return self.dictionary.decode(dictionary_ids)

    def display(self):
        print("Dictionary:")
        print(self.dictionary.id_to_value)

        print("\nCompressed Data:")
        print(self.data)

        print("\nDecoded Data:")
        print(self.decode())


departments = [
    "CSE",
    "CSE",
    "CSE",
    "CSE",
    "IT",
    "IT",
    "IT",
    "ECE",
    "ECE",
    "ECE",
    "ECE",
    "ECE"
]

column = CompressedColumn(departments)

column.display()    