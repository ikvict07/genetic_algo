from B2 import centroid, metoid, divisive_centroid
from B2.common import generate_first_20, generate_40k


def main():
    points = generate_first_20()
    points = generate_40k(points)

    divisive_centroid.main(points)


if __name__ == '__main__':
    main()
