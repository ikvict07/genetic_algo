import random

from B1.old_v.evo_algo import Person
from B1.old_v.evo_algo import generate_population
from B1.old_v.field import generate_field, add_treasures
from B1.old_v.virtual_machine import run_virtual_machine, StepType, Pair, Instruction, Register


def get_new_population(person_to_fitness: list[tuple[Person, tuple[int, int]]], mutation_rate: int, best_count: int) -> list[
    Person]:
    should_be_num = len(person_to_fitness)

    person_to_fitness.sort(key=lambda x: x[1], reverse=True)
    assert person_to_fitness[0][1] >= person_to_fitness[-1][1]
    # Save the best
    new_population: list[Person] = [person_to_fitness[i][0] for i in range(best_count)]

    children_count = should_be_num - len(new_population)
    for _ in range(children_count):
        parent1: Person = select_parent(person_to_fitness)
        parent2: Person = select_parent(person_to_fitness)
        while parent1 == parent2:
            parent2 = select_parent(person_to_fitness)
        child: list[Pair[Instruction, Register]] = []
        for i in range(len(parent1.gens)):

        # child = crossover(parent1, parent2).gens

        # for j in range(len(parent1.gens) // 2):
        #     child.append(parent1.gens[j])
        # for j in range(len(parent2.gens) // 2, len(parent2.gens)):
        #     child.append(parent2.gens[j])
        # assert len(child) == len(parent1.gens)
        # for n, j in enumerate(child):
        #     if random.random() < mutation_rate:
        #         f = Instruction(str(random.randint(0, 1)) + str(random.randint(0, 1)))
        #         s = Register(random.randint(0, 255))
        #         child[n] = Pair(f, s)

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


def game(n: int, m: int, treasures: list[tuple[int, int]], num_of_generations: int, population_size: int,
         mutation_rate: float, best_to_leave: int) -> Person:
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
                k = 0
                for decision in decisions:
                    new_position = calculate_new_position(start_position, decision, n, m)
                    if field[new_position[0]][new_position[1]] == 1:
                        collected += 1
                        field[new_position[0]][new_position[1]] = 0
                    start_position = new_position
                    k += 1
                if collected == len(treasures):
                    print(f"Solution found with {k} steps " + str(person))
                    return person

                fitness = (collected, -k)

                person_to_fitness.append((person, fitness))

            mmax: tuple[Person, tuple[int, int]] = max(person_to_fitness, key=lambda x: x[1])
            print(f"Best solution found: steps: {k} treasures {collected} with {mmax[0]}")

            starting_population = get_new_population(person_to_fitness, mutation_rate, best_to_leave)

        user_input = input("Solution not found. Do you want to run another 500 generations? (yes/no): ")
        if user_input.lower() != 'yes':
            break
    return None


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
def select_parent(person_to_fitness: list[tuple[Person, tuple[int, int]]]) -> Person:
    tournament_size = 50
    selected = random.sample(person_to_fitness, tournament_size)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]


# def crossover(parent1: Person, parent2: Person) -> Person:
#     citiesLen = len(parent1.gens)
#
#     start, end = sorted(random.sample(range(citiesLen), 2))
#     child = Person(gens=[None for _ in range(citiesLen)])
#     child.gens[start:end] = parent1.gens[start:end]
#
#     index:int = end
#
#     for gene in parent2.gens:
#         if gene not in child.gens:
#             if index == citiesLen:
#                 index = 0
#             child.gens[index] = gene
#             index += 1
#
#     return child