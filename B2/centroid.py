import random
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
import numpy as np
from matplotlib import pyplot as plt

from B2.main import Point

CLUSTER_SIZE = 20


def main(points: set[Point]) -> None:
    points_array = np.array([[p.x, p.y] for p in points])
    previous_centroids = None
    clusters = initialize_clusters(points_array, CLUSTER_SIZE)

    for _ in range(50):  # Iterations for convergence
        new_centers = np.array([find_center_metoid_parallel(np.array(cluster)) for cluster in clusters.values()])


        if previous_centroids is not None and np.all(np.linalg.norm(new_centers - previous_centroids, axis=1) < 1):
            print("Converged")
            break

        previous_centroids = new_centers
        clusters = {tuple(center): [] for center in new_centers}

        for point in points_array:
            closest_centroid = find_closest_to_center(point, new_centers)
            clusters[tuple(closest_centroid)].append(point)

    check_solution(clusters)
    plot_clusters(clusters)


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


def plot_clusters(clusters: dict[tuple, list[np.ndarray]]):
    plt.figure(figsize=(10, 10))
    colors = ['#%06X' % random.randint(0, 0xFFFFFF) for _ in range(len(clusters))]

    for color, (center, points) in zip(colors, clusters.items()):
        cluster_points = np.array(points)
        plt.scatter(cluster_points[:, 0], cluster_points[:, 1], c=color,
                    label=f'Cluster centered at ({center[0]:.2f}, {center[1]:.2f})')
        plt.scatter(center[0], center[1], c=color, edgecolor='black', s=200, marker='.')

    plt.xlim(-5000, 5000)
    plt.ylim(-5000, 5000)
    plt.xlabel('X Coordinate')
    plt.ylabel('Y Coordinate')
    plt.title('Clusters Visualization')
    plt.grid(True)
    plt.show()


def check_solution(clusters: dict[tuple, list[np.ndarray]]):
    for center, points in clusters.items():
        mean_distance = np.mean([np.linalg.norm(np.array(center) - point) for point in points])
        if mean_distance > 500:
            print(f"Cluster with center {center} has mean distance of {mean_distance:.2f}")
