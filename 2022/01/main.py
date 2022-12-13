import os
from typing import Optional

sample_data = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def find_max(lines: list[str]) -> tuple[list[int], Optional[int], Optional[int]]:
    calories: list[int] = []
    elf_calories = 0
    max_calories = 0
    max_calories_idx: Optional[int] = None
    for _, line in enumerate(lines):
        if not line:
            calories.append(elf_calories)

            if elf_calories > max_calories:
                max_calories = elf_calories
                max_calories_idx = len(calories) - 1

            elf_calories = 0
        else:
            elf_calories += int(line.strip())

    return (
        calories,
        max_calories,
        max_calories_idx,
    )


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    calories, max_calories, id = find_max(sample_data.splitlines())
    print(calories)
    print(max_calories)
    print(id)

    calories, max_calories, id = find_max(question_data)
    print(calories)
    print(max_calories)
    print(id)

    sum(sorted(calories, reverse=True)[:3])
