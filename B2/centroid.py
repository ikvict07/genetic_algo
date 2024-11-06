import random
from concurrent.futures import ThreadPoolExecutor
import numpy as np

from B2.constants import CLUSTER_SIZE
from B2.main import Point
from B2.plotting import plot_clusters


def main(points: set[Point]) -> None:
    plot_clusters(cluster_by_centroid(points, CLUSTER_SIZE))


def cluster_by_centroid(points: set[Point], k: int) -> dict[tuple, list[np.ndarray]]:
    points_array = np.array([[p.x, p.y] for p in points])
    previous_centroids = None
    clusters = initialize_clusters(points_array, k)

    for _ in range(50):
        new_centers = np.array([find_center_metoid_parallel(np.array(cluster)) for cluster in clusters.values()])

        if previous_centroids is not None and np.all(np.linalg.norm(new_centers - previous_centroids, axis=1) < 1):
            print("Converged")
            break

        previous_centroids = new_centers
        clusters = {tuple(center): [] for center in new_centers}

        for point in points_array:
            closest_centroid = find_closest_to_center(point, new_centers)
            clusters[tuple(closest_centroid)].append(point)
    return clusters


def initialize_clusters(points: np.ndarray, k: int) -> dict[tuple, list[np.ndarray]]:
    initial_clusters = {}
    initial_centroid = points[random.randint(0, len(points) - 1)]
    initial_clusters[tuple(initial_centroid)] = [initial_centroid]

    for _ in range(1, k):
        distances = np.array(
            [min(np.linalg.norm(point - np.array(list(initial_clusters.keys())), axis=1)) for point in points])
        next_centroid = points[np.argmax(distances)]
        initial_clusters[tuple(next_centroid)] = [next_centroid]

    return initial_clusters


def find_center_centroid(points: np.ndarray) -> np.ndarray:
    return np.mean(points, axis=0)


def find_center_metoid_parallel(cluster: np.ndarray) -> np.ndarray:
    with ThreadPoolExecutor() as executor:
        total_distances = list(executor.map(lambda p: np.sum(np.linalg.norm(p - cluster, axis=1)), cluster))
    return cluster[np.argmin(total_distances)]


def find_closest_to_center(point: np.ndarray, centers: np.ndarray) -> np.ndarray:
    distances = np.linalg.norm(centers - point, axis=1)
    return centers[np.argmin(distances)]
