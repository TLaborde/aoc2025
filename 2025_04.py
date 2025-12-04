from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    # 2d array with each cell a character
    return [list(line) for line in puzzle_input.splitlines()]


def part1(data):
    """Solve part 1."""
    # for each row, col in data, do something
    free = 0
    for (i, row) in enumerate(data):
        for j in range(len(row)):
            # check all neighbors
            neighbors = 0
            if data[i][j] != "@":
                continue
            for di in [-1, 0, 1]:
                for dj in [-1, 0, 1]:
                    if di == 0 and dj == 0:
                        continue
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(data) and 0 <= nj < len(data[0]):
                        if data[ni][nj] == "@":
                            neighbors += 1
            if neighbors < 4:
                free += 1
    return free


def part2(data):
    change = True
    free = 0
    while change:
        change = False
        new_data = [row.copy() for row in data]
        for (i, row) in enumerate(data):
            for j in range(len(row)):
                # check all neighbors
                neighbors = 0
                if data[i][j] != "@":
                    continue
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if di == 0 and dj == 0:
                            continue
                        ni, nj = i + di, j + dj
                        if 0 <= ni < len(data) and 0 <= nj < len(data[0]):
                            if data[ni][nj] == "@":
                                neighbors += 1
                if neighbors < 4:
                    free += 1
                    change = True
                    new_data[i][j] = "."
        data = new_data
    
    return free

def solve(puzzle_input):
    """Solve the puzzle for the given input."""
    data = parse(puzzle_input)
    solution1 = part1(data)
    solution2 = part2(data)

    return f"{solution1}", f"{solution2}"


if __name__ == "__main__":
    for example in puzzle.examples:
        answer_a, answer_b = solve(example.input_data)
        if answer_a != '13':
            print(f"expected 13, got {answer_a}")
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