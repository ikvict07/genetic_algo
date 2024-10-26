import itertools
import random

from B2 import centroid

LIMIT = 5000


def generate_first_20() -> set['Point']:
    points = set()
    while len(points) < 20:
        points.add(Point(random.randint(-LIMIT, LIMIT), random.randint(-LIMIT, LIMIT)))
    return points

def generate_40k(points: set['Point']) -> set['Point']:
    while len(points) < 40_020:
        random_element = get_random_element(points)
        new_x = random_element.x + random.randint(-100, 100)
        new_y = random_element.y + random.randint(-100, 100)
        points.add(Point(new_x, new_y))
    return points


def get_random_element(s: set):
    index = random.randint(0, len(s) - 1)
    return next(itertools.islice(s, index, index + 1))

def main():
    points = generate_first_20()
    points = generate_40k(points)



    centroid.main(points)


class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"


if __name__ == '__main__':
    main()
