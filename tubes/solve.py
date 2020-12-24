import yaml
from model import *
import random
from copy import deepcopy
from pprint import pprint

input_file = '../fixtures/lvl3.yml'

tree_keys = [('game', None),
             ('hash', None),
             ('legal_moves', []),
             ('moves', []),
             ('solved', False)]


def main():
    with open(input_file) as file:
        config = yaml.load(file, Loader=yaml.SafeLoader)
    game = Game(config)
    solve(game)
    # while not game._solved:
    #     print(game)
    #     move = pick_move(game)
    #     print(move)
    #     execute_move(game, move)
    # print(game)
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
    min_value = min(moves.values())
    min_keys = [move for move in moves if moves[move] == min_value]
    return random.choice(min_keys)


def execute_move(game, move):
    game._push_move(move[0], move[1])


def solve(game_input):
    tree = {
        'game': game_input,
        'solved': game_input._solved,
        'score': game_input._color_score,
        'moves': [],
        'hash': hash(game_input),
        'legal_moves': {}
    }
    moves = []
    queue = []
    visited = []
    orig_dict = tree
    num_moves = 0
    depth = 0
    queue.append(orig_dict)
    while queue:
        depth += 1
        node = queue.pop(0)
        visited.append(hash(node['game']))
        level_dict = deepcopy(node)
        if node['solved']:
            return
        game = node['game']
        game._forecast()
        legal_moves = game._legal_moves
        for move in legal_moves:
            active_dict = deepcopy(level_dict)
            if not active_dict['legal_moves']:
                active_dict['legal_moves'] = {move: {}}
            else:
                active_dict['legal_moves'][move] = {}
            cur_moves = active_dict['moves']
            active_dict = active_dict['legal_moves'][move]
            active_dict['game'] = deepcopy(game)
            active_game = active_dict['game']
            active_game._push_move(move[0], move[1])
            active_dict['solved'] = active_game._solved
            active_dict['score'] = active_game._color_score
            active_dict['moves'] = cur_moves
            active_dict['legal_moves'] = {}
            active_dict['moves'].append(move)
            active_dict['hash'] = hash(active_game)
            print(active_dict['moves'])
            if hash(active_dict['game']) not in visited:
                queue.append(active_dict)
            if active_dict['solved']:
                print('solved!')
                print(active_dict['moves'])
                print('depth: ', len(active_dict['moves']))
                return
        # num_moves += 1
        # if num_moves % 100 == 0:
        #     # with open('../fixtures/test_output.yml', mode='w') as file:
        #     #     yaml.dump(tree, file, Dumper=yaml.Dumper, indent=4)
        #     #     print('done')
        #     print(num_moves)
        print('depth: ', depth)


if __name__ == '__main__':
    main()
