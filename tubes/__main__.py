import yaml

from tubes.model import Game
from tubes.solve import solve

input_file = '../fixtures/test_1.yml'


def main():
    with open(input_file) as file:
        config = yaml.safe_load(file)
    game = Game(config)
    solve(game)


if __name__ == '__main__':
    main()
