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
    sum = 0
    for bank in data:
        bank = [int(x) for x in bank]
        # get highest value index
        highest_index = bank.index(max(bank))
        #remove the index value
        largest_joltage = bank[highest_index]
        bank[highest_index] = 0
        if highest_index == len(bank) - 1:
            second_highest_index = bank.index(max(bank))
            second_largest_joltage = bank[second_highest_index]
            best = second_largest_joltage * 10 + largest_joltage
        else:
            bank = bank[highest_index:]
            second_highest_index = bank.index(max(bank))
            second_largest_joltage = bank[second_highest_index]
            best = largest_joltage * 10 + second_largest_joltage
        sum += best
    return sum


def part2(data):
    """Solve part 2."""
    sum = 0
    for bank in data:
        bank = [int(x) for x in bank]
        while len(bank) > 12:
            max_value = 0
            for start_index in range(len(bank)):
                # ignore index i in bank
                temp_bank = bank[:]
                temp_bank.pop(start_index)
                current_concat = int("".join(str(x) for x in temp_bank))
                if current_concat > max_value:
                    max_value = current_concat
            bank = [int(x) for x in str(max_value)]
        sum += int("".join(str(x) for x in bank))

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