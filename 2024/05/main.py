import os
from typing import Dict, Set, List

dir_path = os.path.dirname(os.path.realpath(__file__))

# each key's value is a set of numbers that can come after it (map of successors)
succmap: Dict[int, Set[int]] = {}


def update_successors(args: List[int]):
    """
    Update the succmap with the given args (second args comes after the first arg).
    """
    if args[0] not in succmap:
        succmap[args[0]] = set()

    succmap[args[0]].add(args[1])


def validate_update(update: List[int]) -> bool:
    """
    Validate the ordering of the given update according to the map of successors.
    """
    for i, page in enumerate(update):
        if i == len(update) - 1:
            continue

        if update[i + 1] not in succmap.get(page, set()):
            return False

    return True


def fix_update(update: List[int]) -> List[int]:
    # update as a set
    update_set = set(update)

    # number of successors for each update in the update set
    successor_counts = []
    for i, page in enumerate(update):
        # size of intersection of the update set and all the successors of the current page
        successors = len(update_set.intersection(succmap.get(page, set())))
        successor_counts.append(successors)

    fixed_update = [-1] * len(update)
    for i, cnt in enumerate(successor_counts):
        # by knowing the number of successors in the original update list, we can find the correct index
        new_i = len(update) - cnt - 1
        fixed_update[new_i] = update[i]

    return fixed_update


with open(os.path.join(dir_path, 'input.txt'), 'r') as f:
    reading_rules = True
    correct_count = 0
    incorrect_count = 0
    for line in f:
        if reading_rules:
            if line == '\n':
                reading_rules = False
                continue

            update_successors([int(x) for x in line.split('|')])
        else:
            update = [int(x) for x in line.split(',')]

            if validate_update(update):
                correct_count += update[len(update) // 2]
            else:
                fixed_update = fix_update(update)
                incorrect_count += fixed_update[len(fixed_update) // 2]

    print(correct_count)
    print(incorrect_count)
