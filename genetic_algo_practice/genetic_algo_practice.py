from __future__ import annotations

import random
import dataclasses

# make a fitness function


def fit(x: float, y: float):
    return (x * 2 + y * 2) / 5 + 69


def fit_to_solution(solution: Solution):
    return fit(solution.x, solution.y)


# create solutions


@dataclasses.dataclass
class Solution:
    x: int
    y: int


def create_solutions():
    solutions = []

    for _ in range(1, 1000):
        solutions.append(Solution(random.randint(1, 100), random.randint(1, 100)))

    return solutions


# find the best solutions


def find_best_solutions(solutions: list[Solution]):
    return sorted(solutions, key=fit_to_solution, reverse=True)


# selection function


def select_from_best_solutions(solutions: list[Solution]):
    return solutions[0:10]


# mutation function


def mutate_selected_solutions(solutions: list[Solution]):
    # mutate the value by increasing it by 1
    return list(map(lambda s: Solution(s.x + 1, s.y + 1), solutions))


# generate new solutions


def generate_solutions_from_best_solutions(solutions: list[Solution]):
    lowest_best_solution = solutions.copy().pop()
    highest_best_solution = solutions[0]

    new_solutions = []

    for _ in range(1, 1000):
        new_solutions.append(
            Solution(
                random.randint(lowest_best_solution.x, highest_best_solution.x),
                random.randint(lowest_best_solution.y, highest_best_solution.y),
            )
        )

    return new_solutions


# start


def main():
    solutions = create_solutions()
    best_solutions = find_best_solutions(solutions)
    count = 1

    while best_solutions[0].x <= 999 and best_solutions[0].y <= 999:
        print(f"== GEN {count} ==")
        print(f"best solution: {best_solutions[0]}")

        count += 1

        selected_solutions = select_from_best_solutions(best_solutions)
        mutated_solutions = mutate_selected_solutions(selected_solutions)
        best_solutions = generate_solutions_from_best_solutions(mutated_solutions)


main()
