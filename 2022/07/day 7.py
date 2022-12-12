from collections import defaultdict, deque
from dataclasses import dataclass
from typing import Optional

sample_date = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""


@dataclass
class FileItem:
    name: str
    size: int


@dataclass
class DirectoryItem:
    name: str
    contents: dict


Directory_listing = defaultdict[tuple[str, ...], dict[str, int]]


def read_commands(data: list[str]) -> Directory_listing:
    directory_structure = dict()
    cursor = []
    for line in data:
        params = line.strip().split()

        # command
        if params[0] == "$":
            if params[1] == "cd":
                cursor = change_dir(cursor, params)
                continue
            if params[1] == "ls":
                continue
        if params[0] == "dir":
            directory_structure
        if params[0].isdigit():
            path = tuple([*cursor])
            directory_structure[path][params[1]] = int(params[0])

    return directory_structure


def change_dir(cursor: list[str], params: list[str]) -> list[str]:
    if params[2] == "..":
        if len(cursor) > 0:
            cursor.pop()
    elif params[2] == "/":
        return []
    else:
        cursor.append(params[2])
    return cursor


def total_gt(paths: Directory_listing, threshold: int = 0) -> int:
    total_size = 0
    directory_single_sizes: defaultdict[tuple, int] = defaultdict(int)
    for path, file in paths.items():
        directory_single_sizes[path] = sum([size for size in file.values()])

    directory_cum_sizes: defaultdict[tuple, int] = defaultdict(int)
    for path, size in directory_single_sizes.items():
        directory_cum_sizes[path] = size
        if path != ("/",):
            directory_cum_sizes[path[:-1]] += size

    for path, size in directory_cum_sizes.items():
        if path == ("/",):
            continue
        if size <= threshold:
            total_size += size
    return total_size


test_directories = read_commands(sample_date.splitlines())

# print(read_commands(sample_date.splitlines()))
print("test data total size:", total_gt(test_directories, 100000))

with open("./day7_data.txt", "rt") as f:
    question_data = f.read().splitlines()

question_directories = read_commands(question_data)
# print("question data total size:", total_gt(question_directories, 100000))
