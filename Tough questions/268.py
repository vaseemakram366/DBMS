# MapReduce Word Count


class MapReduceWordCount:
    def map_phase(self, text):
        mapped = []

        for word in text.lower().split():
            mapped.append((word, 1))

        return mapped

    def reduce_phase(self, mapped):
        counts = {}

        for word, value in mapped:
            counts[word] = counts.get(word, 0) + value

        return dict(sorted(counts.items()))

    def run(self, text):
        mapped = self.map_phase(text)
        print("Map output:", mapped)

        result = self.reduce_phase(mapped)
        print("Word counts:", result)


text = "database systems are useful and database systems are powerful"

job = MapReduceWordCount()
job.run(text)
