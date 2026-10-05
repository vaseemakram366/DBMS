# Database Catalog Dependency Graph

from collections import defaultdict, deque


class DependencyGraph:
    def __init__(self):
        self.graph = defaultdict(set)
        self.reverse_graph = defaultdict(set)

    def add_object(self, name):
        self.graph[name]
        self.reverse_graph[name]

    def add_dependency(self, dependent, dependency):
        self.add_object(dependent)
        self.add_object(dependency)

        self.graph[dependent].add(dependency)
        self.reverse_graph[dependency].add(dependent)

    def get_dependencies(self, object_name):
        return list(self.graph[object_name])

    def get_dependents(self, object_name):
        return list(self.reverse_graph[object_name])

    def find_affected_objects(self, object_name):
        affected = set()
        queue = deque([object_name])

        while queue:
            current = queue.popleft()

            for dependent in self.reverse_graph[current]:
                if dependent not in affected:
                    affected.add(dependent)
                    queue.append(dependent)

        return affected

    def has_cycle(self):
        visited = set()
        visiting = set()

        def dfs(node):
            if node in visiting:
                return True

            if node in visited:
                return False

            visiting.add(node)

            for dependency in self.graph[node]:
                if dfs(dependency):
                    return True

            visiting.remove(node)
            visited.add(node)

            return False

        for node in self.graph:
            if dfs(node):
                return True

        return False

    def display(self):
        for obj, dependencies in self.graph.items():
            print(f"{obj} depends on: {list(dependencies)}")


catalog = DependencyGraph()

catalog.add_dependency(
    "employee_view",
    "employees"
)

catalog.add_dependency(
    "employee_salary_view",
    "employee_view"
)

catalog.add_dependency(
    "salary_report",
    "employee_salary_view"
)

catalog.add_dependency(
    "employee_index",
    "employees"
)

print("Dependency Graph:")
catalog.display()

print("\nObjects depending on employees:")
print(
    catalog.find_affected_objects("employees")
)

print("\nObjects depending on employee_view:")
print(
    catalog.get_dependents("employee_view")
)

print("\nDoes graph contain cycle?")
print(catalog.has_cycle())