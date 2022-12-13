import os
from collections import defaultdict
from dataclasses import dataclass
from operator import index

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

Paths = tuple[str, ...]
File = dict[str, int]
Directory_listing = defaultdict[Paths, File]


def read_commands(data: list[str]) -> Directory_listing:
    directory_structure = defaultdict(dict)
    wd = ["/"]
    for line in data:
        params = line.strip().split()

        # command
        if params[0] == "$":
            if params[1] == "cd":
                wd = change_dir(wd, params)
                continue
            if params[1] == "ls":
                continue

        # dir
        if params[0] == "dir":
            continue

        # file
        if params[0].isdigit():
            path = tuple([*wd])
            directory_structure[path][params[1]] = int(params[0])

    return directory_structure


def change_dir(wd: list[str], params: list[str]) -> list[str]:
    if params[2] == "..":
        if len(wd) > 0:
            wd.pop()
    elif params[2] == "/":
        return ["/"]
    else:
        wd.append(params[2])
    return wd


def get_sizes(paths: Directory_listing) -> defaultdict[Paths, int]:
    # Calculate size of files in directories
    file_sizes: defaultdict[Paths, int] = defaultdict(int)
    for path, file in paths.items():
        file_sizes[path] = sum([size for size in file.values()])

    # Allocate directory size to parent directories
    directory_sizes: defaultdict[Paths, int] = defaultdict(int)
    for path, size in file_sizes.items():
        for i in range(len(path)):
            directory_sizes[path[: i + 1]] += size

    return directory_sizes


def total_gt(directory_sizes: defaultdict[Paths, int], threshold: int = 0) -> int:

    # Calculate total size for directories below threshold size
    total_size = sum([size for size in directory_sizes.values() if size <= threshold])

    return total_size


def size_of_dir_to_delete(
    directory_sizes: defaultdict[Paths, int],
    system_size: int = 70000000,
    required_freespace: int = 30000000,
) -> int:
    current_freespace = system_size - directory_sizes[("/",)]
    space_to_be_freed = max(required_freespace - current_freespace, 0)

    to_be_deleted_size = system_size
    for dirsize in directory_sizes.values():
        if dirsize > space_to_be_freed:
            if dirsize < to_be_deleted_size:
                to_be_deleted_size = dirsize

    return to_be_deleted_size


if __name__ == "__main__":
    test_directories = read_commands(sample_date.splitlines())
    test_directory_sizes = get_sizes(test_directories)
    # print(read_commands(sample_date.splitlines()))
    print("test data total size:", total_gt(test_directory_sizes, 100000))
    print("test data to be deleted:", size_of_dir_to_delete(test_directory_sizes))

    basedir = os.path.dirname(__file__)
    with open(os.path.join(basedir, "data.txt"), "rt") as f:
        question_data = f.read().splitlines()

    question_directories = read_commands(question_data)
    question_directory_sizes = get_sizes(question_directories)
    print("question data total size:", total_gt(question_directory_sizes, 100000))
    print(
        "question data to be deleted:", size_of_dir_to_delete(question_directory_sizes)
    )
