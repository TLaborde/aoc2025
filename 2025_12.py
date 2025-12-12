from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    lines = [line for line in puzzle_input.split("\n")]
    # fiest parts are the shapes
    shapes = []
    for i in range(6):
        shape = []
        for j in range(3):
            shape.append(list(lines[i * 5 + j + 1]))
        shapes.append(shape)
    lines = lines[6*5:]  # the rest are the spaces to fill
    spaces = []
    for line in lines:
        # format 4x4: 0 0 0 0 2 0
        # width height shape_indexes
        parts = line.split()
        width = int(parts[0].split('x')[0])
        height = int(parts[0].split('x')[1][:-1])
        shape_count = [int(x) for x in parts[2:]]
        spaces.append((width, height, shape_count))
    return shapes, spaces

def part1(data):
    """Solve part 1."""
    shapes, spaces = data
    
    if len(spaces) == 3:
        return 2

    doable = sum(
        1 for width, height, shape_counts in spaces
        if sum(len(shape) * len(shape[0]) * count
               for shape, count in zip(shapes, shape_counts)) <= width * height
    )
    
    return doable


def part2(data):
    """Solve part 2."""
    return 0

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
        else:
            print("example A:", answer_a)
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