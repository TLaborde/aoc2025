from aocd.models import Puzzle
import os
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return puzzle_input


def part1(data):
    """Solve part 1."""
    data = [line.split() for line in data.split('\n')]
    total = 0
    # transpose data to get operations
    data = list(map(list, zip(*data)))
    for i in range(len(data)):
        op = data[i][-1]
        if op == '+':
            total += sum(int(x) for x in data[i][:-1])
        elif op == '*':
            prod = 1
            for x in data[i][:-1]:
                prod *= int(x)
            total += prod

    return total

def reorder(line,ops):
    # generate each number
    numbers = []
    # concat the last digit to each number, remove it from line
    while len(line) > 0:
        new_number = ''
        for i in range(len(line)):
            if ops == '+':
                new_number += line[i][0]
                line[i] = line[i][1:]
            elif ops == '*':
                new_number += line[i][-1]
                line[i] = line[i][:-1]
        # remove empty strings
        line = [x for x in line if x != '']
        numbers.append(int(new_number))
    print(ops, numbers)
    return numbers
def part2(data):
    """Solve part 1."""
    total = 0
    data = [line for line in data.split('\n')]
    data = list(map(list, zip(*data)))
    i = 0
    while i < len(data):
        ops = data[i][-1]
        print(ops, data[i])
        if ops == '+':
            while i < len(data) and any(x != ' ' for x in data[i]):
                vals = [x.strip() for x in data[i][:-1 ] if x != ' '   ]
                total += int(''.join(vals))
                i += 1
        elif ops == '*':
            prod = 1
            while i < len(data) and any(x != ' ' for x in data[i]):
                vals = [x.strip() for x in data[i][:-1 ] if x != ' '   ]
                print(vals)
                prod *= int(''.join(vals))
                i += 1
            total += prod
        i += 1
    print(data)

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