sample_data = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

sample2_data = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

import os
from pprint import pprint

#  Positive is down or right, Negative is up or left.
Position = tuple[int, int]  # (X, Y)
Vector = tuple[int, int]  # (X, Y) difference between two positions.


def tail_move(head: Position, tail: Position) -> Vector:
    move: Vector

    vec = (head[0] - tail[0], head[1] - tail[1])
    # print("vector:", vec)
    # Touching when vector X and Y is <= 1. Then no move.
    if abs(vec[0]) <= 1 and abs(vec[1]) <= 1:
        move = (0, 0)
    else:
        # Not touching. Calculate move for tail.
        tmp_move = [0, 0]

        # X movement
        if vec[0] <= -1:
            tmp_move[0] = -1
        if vec[0] >= 1:
            tmp_move[0] = 1
        if vec[0] == 0:
            tmp_move[0] = 0

        # Y movement
        if vec[1] <= -1:
            tmp_move[1] = -1
        if vec[1] >= 1:
            tmp_move[1] = 1
        if vec[1] == 0:
            tmp_move[1] = 0

        move = tuple(tmp_move)

    return move


def read_moves(data: list[str]) -> list[Vector]:
    moves = []
    for line in data:
        direction, steps = line.split()
        for i in range(int(steps)):
            if direction == "R":
                moves.append((1, 0))
            if direction == "D":
                moves.append((0, -1))
            if direction == "L":
                moves.append((-1, 0))
            if direction == "U":
                moves.append((0, 1))

    return moves


def apply_move(position: Position, move: Vector) -> Position:
    return (position[0] + move[0], position[1] + move[1])


def track_tail(moves: list[Vector]) -> set[Position]:
    # initialize head and tail
    head = (0, 0)
    tail = (0, 0)
    tail_visited: set[Position] = set()
    tail_visited.add(tail)

    # board = [["." for i in range(6)] for i in range(5)]
    # board[0][0] = "s"
    # board[tail[1]][tail[0]] = "T"
    # board[head[1]][head[0]] = "H"
    # pprint(list(reversed(board)))
    # print()

    # process moves
    for move in moves:
        # print(move)
        head = apply_move(head, move)
        # print("tail move:", tail_move(head, tail))
        tail = apply_move(tail, tail_move(head, tail))
        tail_visited.add(tail)

        # board = [["." for i in range(6)] for i in range(5)]
        # board[0][0] = "s"
        # board[tail[1]][tail[0]] = "T"
        # board[head[1]][head[0]] = "H"
        # pprint(list(reversed(board)))
        # print()

    return tail_visited


def track_multi_tail(moves: list[Vector], knots: int = 9) -> set[Position]:
    # initialize head and tail
    head = (0, 0)
    tails: list[Position] = [(0, 0) for i in range(knots)]
    tail_visited: set[Position] = set()
    tail_visited.add(tails[-1])

    # board = [["." for i in range(26)] for i in range(21)]
    # for i in range(len(tails)):
    #     board[tails[i][1]][tails[i][0]] = str(i+1)
    # board[0][0] = "s"
    # board[head[1]][head[0]] = "H"
    # pprint(list(reversed(board)), compact=True, width=200)
    # print()

    for move in moves:
        head = apply_move(head, move)
        tails[0] = apply_move(tails[0], tail_move(head, tails[0]))

        for i in range(1, len(tails)):
            tails[i] = apply_move(tails[i], tail_move(tails[i - 1], tails[i]))
        tail_visited.add(tails[-1])

        # board = [["." for i in range(26)] for i in range(21)]
        # for i in range(len(tails)):
        #     board[tails[i][1]][tails[i][0]] = str(i+1)
        # board[0][0] = "s"
        # board[head[1]][head[0]] = "H"
        # print(move)
        # pprint(list(reversed(board)), compact=True, width=200)
        # print()

    return tail_visited


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    test_moves = read_moves(sample_data.splitlines())
    test_tail_positions = track_tail(test_moves)

    test_multi_moves = read_moves(sample2_data.splitlines())
    test_tail_multi_positions = track_multi_tail(test_multi_moves)
    print("Test| tail positions visited:", len(test_tail_positions))
    print("Test| tail multi positions visited:", len(test_tail_multi_positions))

    question_moves = read_moves(question_data)
    question_tail_positions = track_tail(question_moves)
    question_tail_multi_positions = track_multi_tail(question_moves)
    print("Question| tail positions visited:", len(question_tail_positions))
    print("Question| tail multi positions visited:", len(question_tail_multi_positions))
