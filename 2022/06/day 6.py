from collections import deque

sample_data = """bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

sample_message = """mjqjpqmgbljsphdztnvjfqwrcgsmlb
bvwbjplbgvbhsrlpgdmjqwftvncz
nppdvjthqldpwncqszvftbrmjlhg
nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg
zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw
"""

def find_marker_end(data:str, marker_length:int) -> int:
    marker = deque(list(data[:marker_length]), maxlen=marker_length)
    for i in range(marker_length, len(data)):
        if len(set(marker)) == marker_length:
            return i
        marker.append(data[i])
    return 0

for line in sample_data.splitlines():
    print("test marker ends", find_marker_end(line, 4))

with open("./day6_data.txt", "rt") as f:
    question_data = f.read().splitlines()

print("question marker end:", find_marker_end(question_data[0], 4))

for line in sample_message.splitlines():
    print("test message ends", find_marker_end(line, 14))
print("question messag end:", find_marker_end(question_data[0], 14))
