from numpy.ma.core import multiply

from B1.game import game
from B1.virtual_machine import run_virtual_machine, StepType
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def plot_field(n: int, m: int, treasures: list[tuple[int, int]], person_pos: list[int]):
    fig, ax = plt.subplots()

    ax.set_xticks([x for x in range(1, n + 1)])
    ax.set_yticks([y for y in range(1, m + 1)])
    ax.grid(True)

    ax.set_xlim(0, n)
    ax.set_ylim(0, m)

    for treasure in treasures:
        ax.add_patch(patches.Circle((treasure[1] - 0.5, m - treasure[0] + 0.5), 0.3, color='red'))

    ax.add_patch(patches.Rectangle((person_pos[1], m - person_pos[0] - 1), 1, 1, fill=True, color='blue'))

    plt.draw()
    plt.pause(0.5)
    plt.clf()


def main() -> None:
    n, m = 7, 7
    treasures = [(1, 4), (2, 2), (4, 1), (5, 4), (3, 6)]
    num_of_generations = 500
    population_size = 500
    mutation_rate = 0.05
    best_to_leave = 50
    person = game(n, m, treasures, num_of_generations, population_size, mutation_rate, best_to_leave)

    person_pos = [0, 0]
    plot_field(n, m, treasures, person_pos)

    for step in run_virtual_machine(person.gens):
        if step == StepType.RIGHT and person_pos[1] < m - 1:
            person_pos[1] += 1
        elif step == StepType.LEFT and person_pos[1] > 0:
            person_pos[1] -= 1
        elif step == StepType.TOP and person_pos[0] > 0:
            person_pos[0] -= 1
        elif step == StepType.BOTTOM and person_pos[0] < n - 1:
            person_pos[0] += 1
        if (person_pos[0] + 1, person_pos[1] + 1) in treasures:
            treasures.remove((person_pos[0] + 1, person_pos[1] + 1))

        plot_field(n, m, treasures, person_pos)

    plt.show()


if __name__ == '__main__':
    main()
