from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split()]


def part1(data):
    """Solve part 1."""
    start= 50
    count = 0
    for line in data:
        if line.startswith("R"):
            start += int(line[1:])
        elif line.startswith("L"):
            start -= int(line[1:])
        start = (start + 100) % 100
        if start == 0:
            count += 1
    return count


def part2(data):
    """Solve part 2."""
    start= 50
    count = 0
    for line in data:
        c = int(line[1:])
        count += c // 100
        c = c % 100
        if line.startswith("R"):
            if start + c > 100:
                count += 1
            start += c
        elif line.startswith("L"):
            if start > 0 and start - c < 0:
                count += 1
            start -= c
        start = (start + 100) % 100
        if start == 0:
            count += 1
    return count

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
            if answer_b != "6":
                print(f"expected {example.answer_b}, got {answer_b}")
                raise

    answer_a, answer_b = solve(puzzle.input_data)
    print("A:", answer_a)
    print("B:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b