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
    ranges = "".join(data).split(",")
    s = 0
    for r in ranges:
        start, end = map(int, r.split("-"))
        s += sum(
            i for i in range(start, end + 1)
            if (digits := len(s := str(i))) % 2 == 0
            and s[:digits // 2] == s[digits // 2:]
        )
    return s


def part2(data):
    """Solve part 2."""
    ranges = "".join(data).split(",")
    
    def has_repeating_pattern(num_str):
        """Check if number has a repeating pattern."""
        digits = len(num_str)
        return any(
            digits % div == 0 and num_str == num_str[:div] * (digits // div)
            for div in range(1, digits // 2 + 1)
        )
    
    return sum(
        i
        for r in ranges
        for start, end in [map(int, r.split("-"))]
        for i in range(start, end + 1)
        if has_repeating_pattern(str(i))
    )

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
    print("Part 1:", answer_a)
    print("Part 2:", answer_b)
    #puzzle.answer_a = answer_a
    #if answer_b != "None":
    #    puzzle.answer_b = answer_b