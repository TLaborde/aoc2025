from aocd.models import Puzzle
import os
from itertools import combinations
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line.split(",") for line in puzzle_input.split()]


def part1(data):
    """Solve part 1."""
    # calcuclate distance between each 2 points, then sort by min distance
    distances = [
        ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2, i, j)
        for i, (x1, y1, z1) in enumerate(map(lambda p: map(int, p), data))
        for j, (x2, y2, z2) in enumerate(map(lambda p: map(int, p), data[i + 1:]), start=i + 1)
    ]
    distances.sort()
    
    connected = [[i] for i in range(len(data))]
    max_wires = 10 if len(data) == 20 else 1000
    
    wires = 0
    for dist, i, j in distances:
        found_i = next(group for group in connected if i in group)
        found_j = next(group for group in connected if j in group)
        if found_i is not found_j:
            found_i.extend(found_j)
            connected.remove(found_j)
        wires += 1
        if wires >= max_wires:
            break
    
    connected.sort(key=len, reverse=True)
    return len(connected[0]) * len(connected[1]) * len(connected[2])



def part2(data):
    distances = [
        ((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2, i, j)
        for i, (x1, y1, z1) in enumerate(map(lambda p: map(int, p), data))
        for j, (x2, y2, z2) in enumerate(map(lambda p: map(int, p), data[i + 1:]), start=i + 1)
    ]
    distances.sort()
    
    connected = [[i] for i in range(len(data))]

    for dist, i, j in distances:
        found_i = next(group for group in connected if i in group)
        found_j = next(group for group in connected if j in group)
        if found_i is not found_j:
            found_i.extend(found_j)
            connected.remove(found_j)
        if len(connected) == 1:
            break

    return int(data[i][0]) * int(data[j][0])

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        answer_a, answer_b = solve(example.input_data)
        if answer_a != example.answer_a:
            print(f"expected {example.answer_a}, got {answer_a}")
            raise
        if (example.answer_b):
            if answer_b != example.answer_b:
                print(f"expected {example.answer_b}, got {answer_b}")
                raise

    answer_a, answer_b = solve(puzzle.input_data)
    print("A:", answer_a)
    print("B:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b