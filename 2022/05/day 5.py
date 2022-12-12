from collections import deque
from copy import deepcopy

sample_data = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

Move = tuple[int, int, int]
Moves = list[Move]
Stacks = list[deque[str]]

def read_data(data:list[str]) -> tuple[Stacks, Moves]:
    section_break = data.index("")
    header = data[:section_break]
    body = data[section_break+1:]

    moves = [format_moves(line) for line in body]
    stacks = format_header(header)

    return stacks, moves

def format_moves(line:str) -> Move:
    words = line.split()
    return int(words[1]), int(words[3]), int(words[5])

def format_header(header:list[str]) -> Stacks:
    char_positions:list[int] = []
    for i in range(len(header[-1])):
        if header[-1][i].isdigit():
            char_positions.append(i)

    stacks = [deque() for _ in char_positions]

    for row_id in reversed(range(0, len(header) -1)):
        for stack_id, position in enumerate(char_positions):
            if len(header[row_id]) <= position:
                continue

            if header[row_id][position].isalpha():
                stacks[stack_id].append(header[row_id][position])

    return stacks

def apply_single_moves(stacks:Stacks, moves:Moves) -> Stacks:
    tmp_stacks = deepcopy(stacks)

    for _, (qty, from_stack, to_stack) in enumerate(moves):
        for _ in range(qty):
            tmp_stacks[to_stack - 1].append(tmp_stacks[from_stack - 1].pop())

    return tmp_stacks

def apply_multiple_moves(stacks:Stacks, moves:Moves) -> Stacks:
    tmp_stacks = deepcopy(stacks)

    for _, (qty, from_stack, to_stack) in enumerate(moves):
        insert_pos = len(tmp_stacks[to_stack - 1])
        for _ in range(qty):
            tmp_stacks[to_stack - 1].insert(insert_pos, tmp_stacks[from_stack - 1].pop())

    return tmp_stacks

def get_stack_tops(stacks:Stacks) -> tuple[str, str, str]:
    tops = tuple([stack[-1] for stack in stacks])
    return tops

stacks, moves = read_data(sample_data.splitlines())
print("Test data single moves stack tops:", get_stack_tops(apply_single_moves(stacks, moves)))
print("Test data multiple moves stack tops:", get_stack_tops(apply_multiple_moves(stacks, moves)))

with open("./day5_data.txt", "rt") as f:
    question_data = f.read().splitlines()

stacks, moves = read_data(question_data)
output_stacks = apply_single_moves(stacks, moves)
print("Question data single moves stack tops:", get_stack_tops(apply_single_moves(stacks, moves)))
print("Question data multiple moves stack tops:", get_stack_tops(apply_multiple_moves(stacks, moves)))