import itertools
import random

import numpy as np

from B2.constants import LIMIT


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

def check_solution(clusters: dict[tuple, list[np.ndarray]]):
    for center, points in clusters.items():
        mean_distance = np.mean([np.linalg.norm(np.array(center) - point) for point in points])
        if mean_distance > 500:
            print(f"Cluster with center {center} has mean distance of {mean_distance:.2f}")

def find_closest_to_center(point: np.ndarray, centers: np.ndarray) -> np.ndarray:
    distances = np.linalg.norm(centers - point, axis=1)
    return centers[np.argmin(distances)]
class Point:
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"