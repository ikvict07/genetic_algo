import random

from B1.evo_algo import Person
from B1.evo_algo import generate_population
from B1.field import generate_field, add_treasures
from B1.virtual_machine import run_virtual_machine, StepType, Pair, Instruction, Register


def get_new_population(person_to_fitness: list[tuple[Person, int]], best_count: int) -> list[Person]:
    mutation_rate = 0.001
    should_be_num = len(person_to_fitness)

    person_to_fitness.sort(key=lambda x: x[1], reverse=True)

    # Save the best
    new_population: list[Person] = [person_to_fitness[i][0] for i in range(best_count)]

    children_count = should_be_num - len(new_population)
    for _ in range(children_count):
        parent1: Person = select_parent(person_to_fitness)
        parent2: Person = select_parent(person_to_fitness)
        child: list[Pair[Instruction, Register]] = []
        for i in range(len(parent1.gens)):
            if random.random() < mutation_rate:
                child.append(Pair(Instruction(str(random.randint(0, 1)) + str(random.randint(0, 1))),
                                  Register(random.randint(0, 255))))
            else:
                if random.random() < 0.5:
                    child.append(parent1.gens[i])
                else:
                    child.append(parent2.gens[i])
        new_population.append(Person(child))

    return new_population


def game(n: int, m: int, treasures: list[tuple[int, int]], num_of_generations: int, population_size: int) -> str:
    starting_population = generate_population(population_size)
    while True:
        for generation in range(num_of_generations):
            print("Generation " + str(generation))
            person_to_fitness = []
            for person in starting_population:
                field = generate_field(n, m)
                add_treasures(field, treasures)

                collected = 0
                start_position = (0, 0)

                decisions = run_virtual_machine(person.gens)
                for decision in decisions:
                    new_position = calculate_new_position(start_position, decision, n, m)
                    if field[new_position[0]][new_position[1]] == 1:
                        collected += 1
                        field[new_position[0]][new_position[1]] = 0
                    start_position = new_position

                person_to_fitness.append((person, collected))
                if collected == len(treasures):
                    print("Solution found " + str(person))
                    return str(person)
            mmax: tuple[Person, int] = max(person_to_fitness, key=lambda x: x[1])
            print(f"Best solution found: treasures {mmax[1]} with {mmax[0]}")
            starting_population = get_new_population(person_to_fitness, 5)

        user_input = input("Solution not found. Do you want to run another 500 generations? (yes/no): ")
        if user_input.lower() != 'yes':
            break
    return "No solution found"


def calculate_new_position(position: tuple[int, int], step_type: StepType, n: int, m: int) -> tuple[int, int]:
    x, y = position
    match step_type:
        case StepType.TOP:
            if x - 1 < 0:
                return x, y
            return x - 1, y
        case StepType.BOTTOM:
            if x + 1 >= n:
                return x, y
            return x + 1, y
        case StepType.LEFT:
            if y - 1 < 0:
                return x, y
            return x, y - 1
        case StepType.RIGHT:
            if y + 1 >= m:
                return x, y
            return x, y + 1


# Tournament selection
def select_parent(person_to_fitness: list[tuple[Person, int]]) -> Person:
    tournament_size = 3
    selected = random.sample(person_to_fitness, tournament_size)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]
