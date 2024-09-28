def generate_field(n:int, m:int) -> list[list[int]]:
    return [[0 for _ in range(m)] for _ in range(n)]

def add_treasures(field:list[list[int]], treasures: list[tuple[int, int]]) -> list[list[int]]:
    for x, y in treasures:
        field[x][y] = 1
    return field