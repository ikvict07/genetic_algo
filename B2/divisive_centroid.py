import numpy as np

from B2.centroid import cluster_by_centroid
from B2.common import Point, check_solution
from B2.constants import CLUSTER_SIZE
from B2.plotting import plot_clusters


def cluster_by_divisive(points: set[Point], k: int) -> dict[tuple, list[np.ndarray]]:
    start = cluster_by_centroid(points, 2)
    return divisive(start, k)



def divisive(clusters: dict[tuple, list[np.ndarray]], k: int) -> dict[tuple, list[np.ndarray]]:
    while len(clusters) < k:
        cluster = max(clusters, key=lambda c: len(clusters[c]))
        new_cluster = cluster_by_centroid(set(map(lambda x: Point(x=x[0], y=x[1]), clusters[cluster])), 2)
        clusters.pop(cluster)
        clusters.update(new_cluster)
    print(len(clusters))
    return clusters

def main(points: set[Point]) -> None:
    result = cluster_by_divisive(points, CLUSTER_SIZE)
    check_solution(result)
    plot_clusters(result)