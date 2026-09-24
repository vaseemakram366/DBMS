# Serializable Snapshot Isolation (SSI) Simulator

class Transaction:
    def __init__(self, tid):
        self.tid = tid
        self.reads = set()
        self.writes = set()
        self.active = True
        self.committed = False
        self.aborted = False


class SSISimulator:
    def __init__(self):
        self.transactions = {}
        self.data = {}
        self.readers = {}
        self.writers = {}

    def begin(self, tid):
        self.transactions[tid] = Transaction(tid)
        print(f"{tid}: BEGIN")

    def read(self, tid, key):
        tx = self.transactions[tid]

        if not tx.active:
            return None

        tx.reads.add(key)
        self.readers.setdefault(key, set()).add(tid)

        value = self.data.get(key)

        print(f"{tid}: READ {key} -> {value}")

        return value

    def write(self, tid, key, value):
        tx = self.transactions[tid]

        if not tx.active:
            return

        tx.writes.add(key)
        self.writers.setdefault(key, set()).add(tid)

        self.data[key] = value

        print(f"{tid}: WRITE {key} = {value}")

    def build_dependencies(self):
        graph = {
            tid: set()
            for tid in self.transactions
        }

        for key in self.readers:
            readers = self.readers[key]
            writers = self.writers.get(key, set())

            for reader in readers:
                for writer in writers:
                    if reader != writer:
                        graph[reader].add(writer)

        for key in self.writers:
            writers = list(self.writers[key])

            for i in range(len(writers)):
                for j in range(i + 1, len(writers)):
                    t1 = writers[i]
                    t2 = writers[j]

                    graph[t1].add(t2)
                    graph[t2].add(t1)

        return graph

    def has_cycle_from(self, graph, start):
        visited = set()
        stack = [(start, set())]

        while stack:
            node, path = stack.pop()

            if node in path:
                return True

            if node in visited:
                continue

            visited.add(node)

            new_path = path | {node}

            for neighbor in graph[node]:
                stack.append(
                    (neighbor, new_path)
                )

        return False

    def validate(self, tid):
        graph = self.build_dependencies()

        if self.has_cycle_from(graph, tid):
            print(
                f"{tid}: SSI conflict detected"
            )

            return False

        return True

    def commit(self, tid):
        tx = self.transactions[tid]

        if not tx.active:
            return False

        if not self.validate(tid):
            self.abort(tid)
            return False

        tx.active = False
        tx.committed = True

        print(f"{tid}: COMMIT")

        return True

    def abort(self, tid):
        tx = self.transactions[tid]

        tx.active = False
        tx.aborted = True

        print(f"{tid}: ABORT")


db = SSISimulator()

db.data["A"] = 100
db.data["B"] = 200

db.begin("T1")
db.begin("T2")

db.read("T1", "A")
db.write("T1", "B", 300)

db.read("T2", "B")
db.write("T2", "A", 500)

db.commit("T1")
db.commit("T2")