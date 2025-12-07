from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    # reutnr coord x,y if value is S
    beams = {(x, y) for x, line in enumerate(data) for y, value in enumerate(line) if value == 'S'}
    split = 0
    
    while beams:
        new_beams = set()
        for x, y in beams:
            if x + 1 >= len(data):
                continue
            
            next_cell = data[x + 1][y]
            next_pos = (x + 1, y)
            
            if next_pos in beams:
                continue
            
            if next_cell == '.':
                new_beams.add(next_pos)
            elif next_cell == '^':
                split += 1
                new_beams.update({
                    (x + 1, y + dy) 
                    for dy in [-1, 1] 
                    if 0 <= y + dy < len(data[0])
                })
        
        if not new_beams:
            break
        beams = new_beams
    
    return split

def solve_rec(x, y, data, memo=None):
    if memo is None:
        memo = {}
    
    if (x, y) in memo:
        return memo[(x, y)]
    
    if x + 1 == len(data):
        return 1
    if data[x+1][y] == '.':
        result = solve_rec(x + 1, y, data, memo)
    elif data[x+1][y] == '^':
        total = 0
        if y > 0:
            total += solve_rec(x + 1, y - 1, data, memo)
        if y + 1 < len(data[0]):
            total += solve_rec(x + 1, y + 1, data, memo)
        result = total
    else:
        result = 0
    
    memo[(x, y)] = result
    return result

def part2(data):
    """Solve part 2."""
    for x, line in enumerate(data):
        for y, value in enumerate(line):
            if value == 'S':
                beam = (x, y)

                return solve_rec(beam[0], beam[1], data)

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