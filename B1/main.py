from B1.game import game


def main() -> None:
    n, m = 7, 7
    treasures = [(1, 4), (2, 2), (4, 1), (5, 4), (3, 6)]
    num_of_generations = 500
    population_size = 50
    game(n, m, treasures, num_of_generations, population_size)


if __name__ == '__main__':
    main()
