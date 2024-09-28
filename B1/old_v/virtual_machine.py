from enum import Enum
from typing import List, TypeVar, Generic, Generator, Union
import copy
T = TypeVar('T')
U = TypeVar('U')


class Instruction(Enum):
    INC: str = '00'
    DEC: str = '01'
    JUMP: str = '10'
    PRINT: str = '11'

    def __str__(self) -> str:
        return self.value
    def __repr__(self) -> str:
        return self.value

class Register:
    register: int

    def __init__(self, register: int):
        self.register = register

    def __str__(self) -> str:
        return str(bin(self.register)[2:].zfill(6))

    def __repr__(self) -> str:
        return str(bin(self.register)[2:].zfill(6))


class Pair(Generic[T, U]):
    first: T
    second: U

    def __init__(self, first: T, second: U):
        self.first = first
        self.second = second


    def __str__(self) -> str:
        return f"{self.first}, {self.second}"

    def __repr__(self) -> str:
        return f"{self.first}{self.second}"


def count_ones_in_binary(n: int) -> int:
    return bin(n).count('1')


class StepType(Enum):
    TOP: str = 'H'
    BOTTOM: str = 'D'
    LEFT: str = 'L'
    RIGHT: str = 'P'

    @staticmethod
    def get_type(prefix: str, value: int) -> 'StepType':
        prefix_value = prefix.count("1")
        if count_ones_in_binary(prefix_value + value) <= 2:
            return StepType.TOP
        elif count_ones_in_binary(prefix_value + value) <= 4:
            return StepType.BOTTOM
        elif count_ones_in_binary(prefix_value + value) <= 6:
            return StepType.RIGHT
        else:
            return StepType.LEFT


def run_virtual_machine(instructions1: List[Pair[Instruction, Register]]) -> Generator[StepType, None, None]:
    instructions = copy.deepcopy(instructions1)
    current_register: Register = Register(0)
    last_register: Register = Register(len(instructions))
    iterations = 0
    while current_register.register < last_register.register:
        iterations += 1
        if iterations > 500:
            break
        instruction_type = instructions[current_register.register].first
        register = instructions[current_register.register].second
        if register.register >= last_register.register:
            current_register.register += 1
            if instruction_type == Instruction.JUMP or instruction_type == Instruction.PRINT:
                break
            continue

        new_instruction = instructions[register.register]
        if isinstance(new_instruction, Pair):
            instruction_type = new_instruction.first
            register = new_instruction.second
        else:
            raise TypeError(f"Expected a pair, but got {type(new_instruction)}")
        match instruction_type:
            case Instruction.INC:
                if new_instruction.second.register == 2 ** 7 - 1:
                    new_instruction.second.register = 0
                    new_instruction.first = Instruction.DEC
                else:
                    new_instruction.second.register += 1
                current_register.register += 1

            case Instruction.DEC:
                if new_instruction.second.register == 0:
                    new_instruction.second.register = 2 ** 7 - 1
                    new_instruction.first = Instruction.INC
                else:
                    new_instruction.second.register -= 1
                current_register.register += 1

            case Instruction.JUMP:
                current_register.register = register.register
            case Instruction.PRINT:
                move_to = StepType.get_type(new_instruction.first.value, new_instruction.second.register)
                yield move_to
                current_register.register += 1