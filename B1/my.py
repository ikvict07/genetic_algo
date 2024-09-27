import random

from matplotlib import patches, pyplot as plt


POPULATION_SIZE = 1000
GENERATIONS = 1000
CHROMOSOME_SIZE = 64
ELITE = POPULATION_SIZE // 100 * 15
MUTATION_RATE = 0.10


def animate_solution(directions: list):
    n, m = 7, 7
    treasures = [(1, 4), (2, 2), (4, 1), (5, 4), (3, 6)]  # Adjusted coordinates
    person_pos = [0, 0]

    fig, ax = plt.subplots()

    ax.set_xticks([x for x in range(1, n + 1)])
    ax.set_yticks([y for y in range(1, m + 1)])
    ax.grid(True)

    ax.set_xlim(0, n)
    ax.set_ylim(0, m)

    for treasure in treasures:
        ax.add_patch(patches.Circle((treasure[1] + 0.5, m - treasure[0] - 0.5), 0.3, color='red'))

    person_patch = patches.Rectangle((person_pos[1], m - person_pos[0] - 1), 1, 1, fill=True, color='cyan')
    ax.add_patch(person_patch)

    for direction in directions:
        if direction == "UP" and person_pos[0] > 0:
            person_pos[0] -= 1
        elif direction == "DOWN" and person_pos[0] < n - 1:
            person_pos[0] += 1
        elif direction == "LEFT" and person_pos[1] > 0:
            person_pos[1] -= 1
        elif direction == "RIGHT" and person_pos[1] < m - 1:
            person_pos[1] += 1

        person_patch.set_xy((person_pos[1], m - person_pos[0] - 1))
        if (person_pos[0], person_pos[1]) in treasures:
            treasures.remove((person_pos[0], person_pos[1]))
            ax.add_patch(patches.Circle((person_pos[1] + 0.5, m - person_pos[0] - 0.5), 0.3, color='green'))

        plt.pause(0.1)

    plt.show()

def main():
    game = Game()

    try:
        game.play_game(generate_population(POPULATION_SIZE))
    except ValueError:
        game_result = game.game_result
        directions = game_result.directions
        animate_solution(directions)



class Gene:
    def __init__(self, gene: str):
        self.gene = gene
        self.operation_type = OperationType.of(gene[0:2])
        self.address = Address(gene[2:8])

class OperationType:
    INC = "00"
    DEC = "01"
    JUMP = "10"
    PRINT = "11"

    @staticmethod
    def of(op: str):
        if op == OperationType.INC:
            return OperationType.INC
        elif op == OperationType.DEC:
            return OperationType.DEC
        elif op == OperationType.JUMP:
            return OperationType.JUMP
        elif op == OperationType.PRINT:
            return OperationType.PRINT
        else:
            raise ValueError("Invalid operation type")

class Address:
    def __init__(self, address: str):
        self.address = address

    def get_int(self) -> int:
        return int(self.address, 2)

class Chromosome:
    def __init__(self, genes: list):
        self.genes = genes

class Person:
    def __init__(self, chromosome: Chromosome):
        self.chromosome = chromosome

class Population:
    def __init__(self, persons: list):
        self.persons = persons

class Direction:
    UP = "LEFT"
    DOWN = "RIGHT"
    LEFT = "UP"
    RIGHT = "DOWN"

    @staticmethod
    def of(bits: str):
        if bits == "00":
            return Direction.UP
        elif bits == "01":
            return Direction.DOWN
        elif bits == "10":
            return Direction.LEFT
        elif bits == "11":
            return Direction.RIGHT
        else:
            raise ValueError("Invalid direction")

def generate_all_possible_combinations() -> list:
    return [format(i, '08b') for i in range(256)]

def generate_population(size: int) -> Population:
    persons = [generate_person() for _ in range(size)]
    return Population(persons)

def generate_person() -> Person:
    combinations = generate_all_possible_combinations()
    genes = [Gene(random.choice(combinations)) for _ in range(CHROMOSOME_SIZE)]
    return Person(Chromosome(genes))

class VirtualMachine:
    def run_virtual_machine(self, person: Person):
        memory = [""] * 64
        self.fill_memory(memory, person)
        pointer = 0
        steps = 0
        while pointer < len(memory):
            steps += 1
            if steps > 500:
                break

            instruction = memory[pointer]
            operation_type = OperationType.of(instruction[0:2])
            address = int(instruction[2:], 2)

            if address < 0 or address >= len(memory):
                pointer += 1
                continue

            if operation_type == OperationType.INC:
                current_val = int(memory[address], 2)
                memory[address] = format((current_val + 1) % 256, '08b')
                pointer += 1

            elif operation_type == OperationType.DEC:
                current_val = int(memory[address], 2)
                memory[address] = format((current_val - 1) % 256, '08b')
                pointer += 1

            elif operation_type == OperationType.JUMP:
                pointer = address

            elif operation_type == OperationType.PRINT:
                yield Direction.of(memory[address][6:8])
                pointer += 1

    def fill_memory(self, memory: list, person: Person):
        genes = person.chromosome.genes
        for i, gene in enumerate(genes):
            operation_type = gene.operation_type
            address = gene.address
            memory[i] = operation_type + address.address

class GameResult:
    def __init__(self, person: Person, steps: int, treasures: int, directions: list):
        self.person = person
        self.steps = steps
        self.treasures = treasures
        self.directions = directions

class Game:
    def __init__(self):
        self.game_result = None

    def play_game(self, population: Population) -> Person:
        print(f"Population size: {len(population.persons)}")
        virtual_machine = VirtualMachine()
        person_to_fitness = {}
        for i in range(GENERATIONS):
            print(f"Generation: {i}")
            pair = self.run_generation(population, virtual_machine, person_to_fitness)
            best_person = pair[0]
            print(f"Best person found steps {pair[1][1]} treasures: {pair[1][0]}: {best_person}")
            population = generate_new_population(person_to_fitness)
        return self.run_generation(population, virtual_machine, person_to_fitness)[0]

    def run_generation(self, population: Population, virtual_machine: VirtualMachine, person_to_fitness: dict):
        best_person = population.persons[0]
        best_fitness = 0.0
        best_steps = 0
        best_collected = 0
        for person in population.persons:
            field = Field(7, [Treasure(1, 4), Treasure(2, 2), Treasure(4, 1), Treasure(5, 4), Treasure(3, 6)])
            x, y, collected, steps = 0, 0, 0, 0
            directions = list(virtual_machine.run_virtual_machine(person))
            for direction in directions:
                if collected == len(field.treasures):
                    if steps > field.size * field.size:
                        break
                    print("All treasures collected")
                    print(f"Person: {person}")
                    print(f"Steps: {steps}")
                    print(f"Collected: {collected}")
                    print(f"Directions: {directions}")
                    print(f"Ended at: {x}, {y}")
                    directions = directions[:steps]
                    self.game_result = GameResult(person, steps, collected, directions)
                    raise ValueError("All treasures collected")
                steps += 1
                if direction == Direction.UP:
                    if y > 0: y -= 1
                elif direction == Direction.DOWN:
                    if y < field.size - 1: y += 1
                elif direction == Direction.LEFT:
                    if x > 0: x -= 1
                elif direction == Direction.RIGHT:
                    if x < field.size - 1: x += 1
                if field.field[x][y] == 1:
                    collected += 1
                    field.field[x][y] = 0
            fitness = calculate_fitness(collected, steps, field.size)
            person_to_fitness[person] = fitness
            if fitness > best_fitness:
                best_fitness = fitness
                best_person = person
                best_steps = steps
                best_collected = collected

        assert steps == len(directions)
        return best_person, (best_collected, best_steps)

def generate_new_population(person_to_fitness: dict) -> Population:
    sorted_persons = sorted(person_to_fitness.items(), key=lambda item: item[1], reverse=True)
    elite = [person for person, _ in sorted_persons[:ELITE]]
    new_population = elite.copy()
    while len(new_population) < POPULATION_SIZE:
        first = select_person(sorted_persons)
        second = select_person(sorted_persons)
        child = crossover(first, second)
        child = mutate(child)
        new_population.append(child)
    return Population(new_population)

def mutate(person: Person) -> Person:
    genes = person.chromosome.genes.copy()
    for i in range(len(genes)):
        if random.random() < MUTATION_RATE:
            genes[i] = generate_random_gene()
    return Person(Chromosome(genes))

def generate_random_gene() -> Gene:
    combinations = generate_all_possible_combinations()
    return Gene(random.choice(combinations))

def crossover(first: Person, second: Person) -> Person:
    first_genes = first.chromosome.genes
    second_genes = second.chromosome.genes
    crossover_point = random.randint(0, CHROMOSOME_SIZE - 1)
    new_genes = [first_genes[i] if i < crossover_point else second_genes[i] for i in range(CHROMOSOME_SIZE)]
    return Person(Chromosome(new_genes))

def select_person(sorted_persons: list) -> Person:
    tournament_size = 2
    tournament = random.sample(sorted_persons, tournament_size)
    return max(tournament, key=lambda item: item[1])[0]

class Treasure:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

class Field:
    def __init__(self, size: int, treasures: list):
        self.size = size
        self.treasures = treasures
        self.field = [[0] * size for _ in range(size)]
        for treasure in treasures:
            self.field[treasure.x][treasure.y] = 1

def calculate_fitness(collected: int, steps: int, field_size: int) -> float:
    fitness = collected * field_size * 10 - float(steps)

    if collected == field_size:
        fitness += 1000.0

    if steps > field_size * field_size:
        fitness /= 2

    return max(fitness, 0.0)
if __name__ == '__main__':
    plt.close('all')
    main()