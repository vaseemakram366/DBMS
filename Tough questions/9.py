# Candidate Key Finder

from itertools import combinations


def closure(attributes, fds):
    result = set(attributes)

    changed = True

    while changed:

        changed = False

        for lhs, rhs in fds:

            if set(lhs).issubset(result):

                old_size = len(result)

                result.update(rhs)

                if len(result) > old_size:
                    changed = True

    return result


def find_candidate_keys(attributes, fds):

    attributes = set(attributes)
    candidate_keys = []

    attribute_list = list(attributes)

    for size in range(1, len(attribute_list) + 1):

        for combination in combinations(
            attribute_list,
            size
        ):

            combination = set(combination)

            # Already contains candidate key
            if any(
                key.issubset(combination)
                for key in candidate_keys
            ):
                continue

            result = closure(combination, fds)

            if result == attributes:
                candidate_keys.append(combination)

    return candidate_keys


attributes = {"A", "B", "C", "D", "E"}

fds = [
    ({"A"}, {"B"}),
    ({"B"}, {"C"}),
    ({"C"}, {"D"}),
    ({"D"}, {"E"})
]

keys = find_candidate_keys(attributes, fds)

print("Candidate Keys:")

for key in keys:
    print(key)