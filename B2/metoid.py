import numpy as np

from B2.centroid import initialize_clusters, find_center_metoid_parallel, find_closest_to_center
from B2.constants import CLUSTER_SIZE
from B2.main import Point
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

def main(points: set[Point]) -> None:
    plot_clusters(cluster_by_metoid(points, CLUSTER_SIZE))

