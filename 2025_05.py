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
    # find index in data with empty value
    ranges = []
    to_check = []
    for element in data:
        if '-' in element:
            ranges.append(element.split('-'))
        elif element:  # Skip empty strings
            to_check.append(element)
    total = 0
    for number in to_check:
        for r in ranges:
            if int(r[0]) <= int(number) <= int(r[1]):
                total += 1
                break
    return total


def part2(data):
    """Solve part 2."""
    ranges = []
    for element in data:
        if '-' in element:
            ranges.append(element.split('-'))
    merged_ranges = []
    # Merge overlapping ranges
    for r in sorted(ranges, key=lambda x: int(x[0])):
        if not merged_ranges or int(merged_ranges[-1][1]) < int(r[0]) - 1:
            merged_ranges.append(r)
        else:
            merged_ranges[-1][1] = str(max(int(merged_ranges[-1][1]), int(r[1])))
    
    # Count numbers in all merged ranges
    total = 0
    for r in merged_ranges:
        total += int(r[1]) - int(r[0]) + 1
    return total

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
        # if (example.answer_b):
        #    if answer_b != example.answer_b:
        #        print(f"expected {example.answer_b}, got {answer_b}")
        #        raise

    answer_a, answer_b = solve(puzzle.input_data)
    puzzle.answer_a = answer_a
    if answer_b != "None":
        puzzle.answer_b = answer_b