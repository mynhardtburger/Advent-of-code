import os
from typing import Callable

sample_data = """A Y
B X
C Z"""

shape_rock = {
    "shape": "rock",
    "beats": "scissor",
    "lose": "paper",
    "score": 1,
}

shape_paper = {
    "shape": "paper",
    "beats": "rock",
    "lose": "scissor",
    "score": 2,
}

shape_scissor = {
    "shape": "scissor",
    "beats": "paper",
    "lose": "rock",
    "score": 3,
}

shapes = {
    "rock": shape_rock,
    "paper": shape_paper,
    "scissor": shape_scissor,
}


round_scores = {
    "lose": 0,
    "draw": 3,
    "win": 6,
}


def score_hand(opp_hand: str, my_hand: str) -> int:
    shape_map = {
        "A": shape_rock,
        "B": shape_paper,
        "C": shape_scissor,
        "X": shape_rock,
        "Y": shape_paper,
        "Z": shape_scissor,
    }

    # draw
    if shape_map[my_hand]["shape"] == shape_map[opp_hand]["shape"]:
        return round_scores["draw"] + shape_map[my_hand]["score"]

    # win
    if shape_map[my_hand]["beats"] == shape_map[opp_hand]["shape"]:
        return round_scores["win"] + shape_map[my_hand]["score"]

    # lose
    return round_scores["lose"] + shape_map[my_hand]["score"]


def reverse_score_hand(opp_hand: str, outcome: str) -> int:
    shape_map = {
        "A": shape_rock,
        "B": shape_paper,
        "C": shape_scissor,
    }

    # Lose
    if outcome == "X":
        my_hand = shape_map[opp_hand]["beats"]
        return round_scores["lose"] + shapes[my_hand]["score"]

    # Draw
    if outcome == "Y":
        my_hand = shape_map[opp_hand]["shape"]
        return round_scores["draw"] + shapes[my_hand]["score"]

    # Win
    my_hand = shape_map[opp_hand]["lose"]
    return round_scores["win"] + shapes[my_hand]["score"]


def total_score(data: list[str], scorer: Callable[[str, str], int]) -> int:
    total: list[int] = []
    for id, game in enumerate(data):
        opp_hand, my_hand = game.split()
        score = scorer(opp_hand, my_hand)
        # print("id:", id, "score:", score)
        total.append(score)
    return sum(total)


if __name__ == "__main__":
    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    print(total_score(sample_data.splitlines(), score_hand))
    print(total_score(sample_data.splitlines(), reverse_score_hand))

    print(total_score(question_data, score_hand))
    print(total_score(question_data, reverse_score_hand))
