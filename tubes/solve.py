import yaml
from copy import deepcopy

from tubes.model import Game

input_file = '../fixtures/lvl3.yml'

tree_keys = [('game', None),
             ('hash', None),
             ('legal_moves', []),
             ('moves', []),
             ('solved', False)]


def main():
    with open(input_file) as file:
        config = yaml.safe_load(file)
    game = Game(config)
    solve(game)


def solve(game_input):
    """
    Implements a naive BFS solver for the Game. The BFS algorithm has to tackle both
    graph generation and evaluation for criteria--this wrinkle introduces some
    complexity to the final implementation. Namely, the dictionary object, which can
    be very useful for BFS traversal, is not able to be leveraged efficiently in
    order to traverse the graph, as the full structure of the state graph is not
    known ahead of time. Instead, we are forced to calculate possible states and
    evaluate for solution simultaneously.
    :param game_input: Game object
    :return: #TODO: return solution
    """
    # Instantiate the starting node, which corresponds to the starting state of the
    # game. Nodes will be implemented as dictionaries.
    # game stores the game object
    # solved is a boolean indicating whether or not the node is solved
    # The score stores the color_score. This is not yet used, but could be leveraged
    # for less naive move selection.
    # Moves is a list of moves used to arrive at the current state from the starting
    # state
    # hash is a hash of the current game state, used to compare the current state to
    # previously seen states and avoid unnecessary computation
    # legal moves is a dictionary of moves, which result in future nodes for the BFS
    # algorithm
    tree = {
        'game': game_input,
        'solved': game_input._solved,
        'score': game_input._color_score,
        'moves': [],
        'hash': hash(game_input),
        'legal_moves': {}
    }
    # Queue and visited are utilized as standard BFS structures. The queue stores the
    # unevaluated states, and the visited stores hashes of previously seen states.
    queue = []
    visited = []
    orig_dict = tree
    num_moves_tried = 0

    # First, append the starting state to the queue.
    queue.append(orig_dict)
    while queue:
        num_moves_tried += 1

        # take the first element in the queue and get read to analyze. Also,
        # note that we have visited this node
        node = queue.pop(0)
        visited.append(hash(node['game']))

        # In order to prevent inappropriate copying of information from one node to
        # another, copy the node information to avoid making changes to the original.
        level_dict = deepcopy(node)
        if node['solved']:
            print('solved!')
            print(active_dict['moves'])
            print('depth: ', len(active_dict['moves']))
            return

        # Determine what moves are legal from the given state.
        game = node['game']
        game._forecast()
        legal_moves = game._legal_moves

        # Evaluate each legal move for its effect on the state of the game
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
            # Leave for debugging.
            # print(active_dict['moves'])
            if hash(active_dict['game']) not in visited:
                queue.append(active_dict)
            if active_dict['solved']:
                print('solved!')
                print(active_dict['moves'])
                print('depth: ', len(active_dict['moves']))
                return
        # Leave for debugging
        # print('depth: ', depth)


if __name__ == '__main__':
    main()
