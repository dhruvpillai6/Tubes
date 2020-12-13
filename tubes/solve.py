import yaml
from model import *

input_file = '../fixtures/test_1.yml'


def main():
    with open(input_file) as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    game = Game(config)
    while not game._solved:
        print(game)
        execute_move(game, pick_move(game))
    print(game)
    # print(game)
    # print(pick_move(game))
    # game._forecast()
    # print(game)
    # print(game._legal_moves)
    # game._push_move(1, 3)
    # game._forecast()
    # print(game)
    # print(game._legal_moves)
    # print(game._moves)
    # game._push_move(2, 3)
    # game._forecast()
    # print(game)
    # print(game._legal_moves)
    # game._push_move(1, 2)
    # game._forecast()
    # print(game)
    # print(game._legal_moves)
    # print(game._color_score_raw)


def pick_move(game):
    game._forecast()
    moves = game._legal_moves
    best_move = min(moves, key=moves.get)
    return best_move


def execute_move(game, move):
    game._push_move(move[0], move[1])


if __name__ == '__main__':
    main()
