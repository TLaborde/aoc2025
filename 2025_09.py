from aocd.models import Puzzle
import os
from collections import deque
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [[int(x) for x in line.split(",")] for line in puzzle_input.split()]


def part1(data):
    """Solve part 1."""
    max_area = 0
    for x1, y1 in data:
        for x2, y2 in data:
            area = abs((x1 - x2+1) * (y1 - y2+1))
            if area > max_area:
                max_area = area
    return max_area
    return 0

def intersects(x1, y1, x2, y2,data):
    for i in range(len(data)):
        x3, y3 = data[i]
        x4, y4 = data[(i + 1) % len(data)] 
        if (min(x1, x2) < max(x3, x4) and
            max(x1, x2) > min(x3, x4) and
            min(y1, y2) < max(y3, y4) and
            max(y1, y2) > min(y3, y4)):
            return True
    return False


def part2(data):
    """Solve part 2."""
    max_area = 0
    for x1, y1 in data:
        for x2, y2 in data:
            area = (1+ abs(x1 - x2)) * (abs(y1 - y2)+1)
            if area > max_area and not intersects(x1, y1, x2, y2, data):
                max_area = area
    return max_area


def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        answer_a, answer_b = solve(example.input_data)
        if answer_a != '50':
            print(f"expected {example.answer_a}, got {answer_a}")
            raise
        if (example.answer_b):
           if answer_b != '24':
               print(f"expected {example.answer_b}, got {answer_b}")
               raise

    answer_a, answer_b = solve(puzzle.input_data)
    print("A:", answer_a)
    print("B:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b