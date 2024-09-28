import random
from B1.old_v.virtual_machine import Instruction, Register, Pair


class Person:
    gens: list[Pair[Instruction, Register]]

    def __init__(self, gens: list[Pair[Instruction, Register]]):
        self.gens = gens

    def __str__(self) -> str:
        return str(self.gens)
    def __repr__(self) -> str:
        return str(self.gens)

def _generate_person(instruction_count: int, instruction_len: int) -> list[list[int]]:
    population = []
    for i in range(instruction_count):
        chromosome = []
        for j in range(instruction_len):
            chromosome.append(random.randint(0, 1))
        population.append(chromosome)
    return population

def generate_person(count: int) -> Person:
    population = []
    for person in _generate_person(count, 8):
        instruction = Instruction(str(person[0]) + str(person[1]))
        register = Register(int("".join(map(str, person[2:])), 2))
        population.append(Pair(instruction, register))

    return Person(population)

def generate_population(count: int) -> list[Person]:
    return [generate_person(64) for _ in range(count)]