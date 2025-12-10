from aocd import data
from aocd.models import Puzzle
import os
from itertools import combinations
import z3
# import puzzle
filename = os.path.basename(__file__)
year, day = filename[:-3].split("_")[:2]
puzzle = Puzzle(year=int(year), day=int(day))


def parse(puzzle_input):
    """Parse input."""
    return [line for line in puzzle_input.split("\n")]


def part1(data):
    """Solve part 1."""
    total_presses = 0
    for line in data:
        line = line.split(" ")
        lights = (line[0][1:-1])[::-1]
        # transfor lights string into binary number with '#' as 1 and '.' as 0
        lights = int(lights.replace("#", "1").replace(".", "0"), 2)
        buttons = line[1:-1]
        binary_buttons = []
        for button in buttons:
            button = button[1:-1].split(",")
            # button has number that are the index in a binary number, calculate the sum
            binary_button = 0
            for b in button:
                index = int(b)
                binary_button ^= (1 << index)
            binary_buttons.append(binary_button)
        i = 1
        while True:
            combinations_found = False
            for combo in combinations(binary_buttons, i):
                combo_sum = 0
                for c in combo:
                    combo_sum ^= c
                if combo_sum == lights:
                    combinations_found = True
                    total_presses += len(combo)
                    break
            if not combinations_found:
                i +=1
            else:
                break
    return total_presses


def part2(data):
    total = 0
    for line in data:
        line = line.split(" ")
        joltages = [int(x) for x in line[-1][1:-1].split(",")]
        buttons = []
        for b in line[1:-1]:
            button = set(int(x) for x in b[1:-1].split(","))
            buttons.append(button)
        print(joltages, buttons)
        presses = [
            z3.Int(f"press{i}") for i in range(len(buttons))
        ]

        s = z3.Optimize()
        s.add(z3.And([press >= 0 for press in presses]))
        s.add(z3.And([
            sum(presses[j] for j, button in enumerate(buttons) if i in button) == joltage
                for i, joltage in enumerate(joltages)
        ]))
        s.minimize(sum(presses))
        m = s.model()
        for press in presses:
            total += m[press].as_long()
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