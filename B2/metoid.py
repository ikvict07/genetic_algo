from concurrent.futures import ThreadPoolExecutor

import numpy as np

from B2.centroid import initialize_clusters
from B2.common import Point, find_closest_to_center, check_solution
from B2.constants import CLUSTER_SIZE
from B2.plotting import plot_clusters


def cluster_by_metoid(points: set[Point], k: int) -> dict[tuple, list[np.ndarray]]:
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


def find_center_metoid_parallel(cluster: np.ndarray) -> np.ndarray:
    with ThreadPoolExecutor() as executor:
        total_distances = list(executor.map(lambda p: np.sum(np.linalg.norm(p - cluster, axis=1)), cluster))
    return cluster[np.argmin(total_distances)]


def main(points: set[Point]) -> None:
    result = cluster_by_metoid(points, CLUSTER_SIZE)
    check_solution(result)
    plot_clusters(result)
