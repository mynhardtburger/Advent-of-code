import os

sample_data = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


item_types = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
items = {item_types[i]: i + 1 for i in range(len(item_types))}
# print(items)


def misplaced_item(rucksack: str) -> tuple[int, str, set[str]]:
    item_count = len(rucksack)
    assert item_count % 2 == 0

    comp1 = set(rucksack[: item_count // 2])
    comp2 = set(rucksack[item_count // 2 :])

    intersect = comp1 & comp2
    missplaced = intersect.pop()
    unique_items = comp1 ^ comp2

    return items[missplaced], missplaced, unique_items


def priority_score(lines: list[str]) -> int:
    score = 0
    for line in lines:
        value, missplaced_item, unique_items = misplaced_item(line.strip())
        score += value
    return score


def score_badges(lines: list[str]) -> int:
    score = 0
    for i in range(0, len(lines), 3):
        _, _, sack1 = misplaced_item(lines[i].strip())
        _, _, sack2 = misplaced_item(lines[i + 1].strip())
        _, _, sack3 = misplaced_item(lines[i + 2].strip())

        badge = sack1 & sack2 & sack3
        score += items[badge.pop()]

    return score


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    print("Sample missplaced score:", priority_score(sample_data.splitlines()))
    print("Sample badge score:", score_badges(sample_data.splitlines()))

    print("Question missplaced score:", priority_score(question_data))
    print("Question badge score:", score_badges(question_data))
