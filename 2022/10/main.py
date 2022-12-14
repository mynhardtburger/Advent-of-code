sample_data = """noop
addx 3
addx -5"""


long_sample_data = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

import os
from pprint import pprint


def pixel_drawable(cycle: int, x: int) -> int:
    cycle_column = cycle % 40 - 1
    x_range = [x - 1, x, x + 1]
    if cycle_column in x_range:
        return cycle - 1
    return -1


def is_signal_event(cycle: int) -> bool:
    if cycle % 40 == 20:
        return True
    return False


def execute(instructions: list[str]) -> tuple[dict[int, int], list[str]]:
    x = 1
    cycle = 0
    screen = ["." for i in range(40 * 6)]
    signal_strength: dict[int, int] = dict()
    for instruction in instructions:
        if instruction == "noop":
            # start of cycle
            cycle += 1
            if is_signal_event(cycle):
                signal_strength[cycle] = cycle * x

            draw_pixel = pixel_drawable(cycle, x)
            if draw_pixel != -1:
                screen[draw_pixel] = "#"
            continue

        action, value = instruction.split()
        if action == "addx":
            # start of cycle
            cycle += 1
            if is_signal_event(cycle):
                signal_strength[cycle] = cycle * x

            draw_pixel = pixel_drawable(cycle, x)
            if draw_pixel != -1:
                screen[draw_pixel] = "#"

            # 2nd cycle
            cycle += 1
            if is_signal_event(cycle):
                signal_strength[cycle] = cycle * x

            draw_pixel = pixel_drawable(cycle, x)
            if draw_pixel != -1:
                screen[draw_pixel] = "#"

            x += int(value)

    return signal_strength, screen


def draw_screen(screen: list[str]) -> None:
    i = 0
    for y in range(6):
        row = []
        for x in range(40):
            row.append(screen[i])
            i += 1
        print("".join(row))


def test_sample():
    answer, _ = execute(long_sample_data.strip().splitlines())
    assert answer == 13920


def test_question():
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    answer, _ = execute(question_data)
    assert answer == 13920


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    test_ss, test_screen = execute(long_sample_data.strip().splitlines())
    question_ss, question_screen = execute(question_data)
    print("Test| sum of signal strengths:", sum(test_ss.values()))
    draw_screen(test_screen)
    print("Question| sum of signal strengths:", sum(question_ss.values()))
    draw_screen(question_screen)
