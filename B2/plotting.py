import random

import numpy as np
from matplotlib import pyplot as plt


def plot_clusters(clusters: dict[tuple, list[np.ndarray]]):
    plt.figure(figsize=(50, 50))
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