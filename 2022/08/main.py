sample_data = """30373
25512
65332
33549
35390"""

import os
from dataclasses import dataclass
from math import dist
from pprint import pprint


@dataclass
class LOS:
    up: int = -1
    down: int = -1
    left: int = -1
    right: int = -1
    height: int = -1
    visible: bool = True


LOS_map = list[list[LOS]]
Height_map = list[list[int]]


def data_to_los_map(data: list[str]) -> LOS_map:
    output = []
    for _, row_val in enumerate(data):
        output.append([])
        for _, col_val in enumerate(row_val):
            output[-1].append(LOS(height=int(col_val)))
    return output


def left_right_top_bottom(los_map: LOS_map) -> LOS_map:
    for row_id, row_val in enumerate(los_map):
        for col_id, _ in enumerate(row_val):
            if col_id != 0:
                los_map[row_id][col_id].left = max(
                    los_map[row_id][col_id - 1].height,
                    los_map[row_id][col_id - 1].left,
                )
            if row_id != 0:
                los_map[row_id][col_id].up = max(
                    los_map[row_id - 1][col_id].height,
                    los_map[row_id - 1][col_id].up,
                )
    return los_map


def right_left_bottom_top(los_map: LOS_map) -> LOS_map:
    for row_id, row_val in reversed(list(enumerate(los_map))):
        for col_id, _ in reversed(list(enumerate(row_val))):
            if col_id != len(row_val) - 1:
                los_map[row_id][col_id].right = max(
                    los_map[row_id][col_id + 1].height,
                    los_map[row_id][col_id + 1].right,
                )
            if row_id != len(los_map) - 1:
                los_map[row_id][col_id].down = max(
                    los_map[row_id + 1][col_id].height,
                    los_map[row_id + 1][col_id].down,
                )
    return los_map


def update_visability(los_map: LOS_map) -> tuple[LOS_map, int]:
    total_visable = 0
    for row_id, row_val in enumerate(los_map):
        for col_id, col_val in enumerate(row_val):
            if col_val.height > min(
                col_val.up,
                col_val.down,
                col_val.left,
                col_val.right,
            ):
                los_map[row_id][col_id].visible = True
                total_visable += 1
            else:
                los_map[row_id][col_id].visible = False
    return los_map, total_visable


def create_los_map(data: list[str]) -> tuple[LOS_map, int]:
    los_map = data_to_los_map(data)

    los_map = left_right_top_bottom(los_map)
    los_map = right_left_bottom_top(los_map)
    los_map, total_visable = update_visability(los_map)

    return los_map, total_visable


def los_range(trees: list[LOS], source_height: int, reverse_data: bool = False) -> int:
    if reverse_data:
        trees = list(reversed(trees))

    distance = 0

    for i in range(len(trees)):
        distance += 1
        if trees[i].height >= source_height:
            return distance

    return distance


def transpose(x: list[list[LOS]]) -> list[list[LOS]]:
    return list(map(list, zip(*x)))


def scenic_score(los_map: LOS_map, x: int, y: int) -> int:
    source = los_map[y][x].height
    if x == 0:
        return 0
    if y == 0:
        return 0

    up = los_range(transpose(los_map)[x][:y], source, reverse_data=True)
    left = los_range(los_map[y][:x], source, reverse_data=True)
    down = los_range(transpose(los_map)[x][y + 1 :], source)
    right = los_range(los_map[y][x + 1 :], source)

    return up * down * left * right


def max_scenic_score(los_map: LOS_map) -> int:
    max_score = 0

    for y in range(len(los_map)):
        for x in range(len(los_map[y])):
            max_score = max(scenic_score(los_map, x, y), max_score)

    return max_score


if __name__ == "__main__":
    test_los_map, test_visable = create_los_map(sample_data.splitlines())
    # pprint(test_los_map)
    print("test visable:", test_visable)
    print("test scenic score:", max_scenic_score(test_los_map))

    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    question_los_map, question_visable = create_los_map(question_data)
    print("question visable:", question_visable)
    print("question scenic score:", max_scenic_score(question_los_map))
