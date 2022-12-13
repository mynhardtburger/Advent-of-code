import os

sample_data = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def read_pair(pair: str) -> tuple[tuple[int, int], tuple[int, int]]:
    first, second = pair.strip().split(",")
    first_start, first_end = first.split("-")
    second_start, second_end = second.split("-")

    return (int(first_start), int(first_end)), (int(second_start), int(second_end))


def is_subset(first_range: tuple[int, int], second_range: tuple[int, int]) -> bool:
    assert first_range[0] <= first_range[1]
    assert second_range[0] <= second_range[1]

    # Second is contained within first
    if (first_range[0] <= second_range[0]) & (first_range[1] >= second_range[1]):
        return True

    # First is contained within second
    if (second_range[0] <= first_range[0]) & (second_range[1] >= first_range[1]):
        return True

    return False


def is_partial_overlap(
    first_range: tuple[int, int], second_range: tuple[int, int]
) -> bool:
    assert first_range[0] <= first_range[1]
    assert second_range[0] <= second_range[1]

    # Second starts within first
    if (first_range[0] <= second_range[0]) & (first_range[1] >= second_range[0]):
        return True

    # First starts within second
    if (second_range[0] <= first_range[0]) & (second_range[1] >= first_range[0]):
        return True

    return False


def count_subsets(pairs: list[str]) -> int:
    subset_count = 0
    for idx, pair in enumerate(pairs):
        first, second = read_pair(pair)
        subset = is_subset(first, second)
        if subset:
            subset_count += 1

    return subset_count


def count_overlap(pairs: list[str]) -> int:
    overlap_count = 0

    for idx, pair in enumerate(pairs):
        first, second = read_pair(pair)
        subset = is_subset(first, second)
        partial_overlap = is_partial_overlap(first, second)
        if subset or partial_overlap:
            overlap_count += 1

    return overlap_count


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    print("Sample data subset count:", count_subsets(sample_data.splitlines()))
    print("Sample data overlap count:", count_overlap(sample_data.splitlines()))

    print("Question data subset count:", count_subsets(question_data))
    print("Question data overlap count:", count_overlap(question_data))
