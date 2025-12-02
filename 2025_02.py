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
    sum = 0
    for r in ranges:
        start, end = map(int, r.split("-"))
        for i in range(start, end + 1):
            #get number of digits in i
            digits = len(str(i))
            if digits % 2 == 0:
                mid = digits // 2
                left = str(i)[:mid]
                right = str(i)[mid:]
                if left == right:
                    #print(f"adding {i}")
                    sum += i
    return sum


def part2(data):
    """Solve part 2."""
    ranges = "".join(data).split(",")
    sum = 0
    for r in ranges:
        start, end = map(int, r.split("-"))
        for i in range(start, end + 1):
            #get number of digits in i
            digits = len(str(i))
            # get all the divisors of digits
            divisors = []
            for d in range(1, digits //2 + 1):
                if digits % d == 0:
                    divisors.append(d)
            for div in divisors:
                # if each segment of length div is the same
                segments = [str(i)[j:j+div] for j in range(0, digits, div)]
                if all(s == segments[0] for s in segments):
                    print(f"adding {i}")
                    sum += i
                    break
    return sum

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