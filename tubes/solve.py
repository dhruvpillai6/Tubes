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


class GameState:
    def __init__(self, game=None, moves=None, legal_moves=None):
        self.game = game
        self.moves = moves or []
        self.legal_moves = legal_moves or {}

    @property
    def solved(self) -> bool:
        return self.game._solved

    @property
    def score(self) -> int:
        # This is not yet used, but could be leveraged for less naive move selection
        return self.game._color_score

    def make_move(self, move):
        self.moves.append(move)
        self.game._push_move(*move)


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
    # Queue and visited are utilized as standard BFS structures. The queue stores the
    # unevaluated states, and the visited stores hashes of previously seen states.
    queue = [GameState(game_input)]
    visited = set()
    num_moves_tried = 0

    while queue:
        num_moves_tried += 1

        # take the first element in the queue and get ready to analyze.
        node = queue.pop(0)
        # Also, note that we have visited this node
        visited.add(node.game)

        # In order to prevent inappropriate copying of information from one node to
        # another, copy the node information to avoid making changes to the original.
        if node.solved:
            print('solved!')
            print(game_state.moves)
            print(f'depth: {len(game_state.moves)}')
            return game_state.moves

        # Determine what moves are legal from the given state.
        node.game._forecast()
        legal_moves = node.game._legal_moves

        # Evaluate each legal move for its effect on the state of the game
        for move in legal_moves:
            game_state = deepcopy(node)
            game_state.make_move(move)
            # Leave for debugging.
            # print(game_state.moves)
            if game_state.game not in visited:
                queue.append(game_state)
            if game_state.solved:
                print('solved!')
                print(game_state.moves)
                print(f'depth: {len(game_state.moves)}')
                return game_state.moves
        # Leave for debugging
        # print('depth: ', depth)


if __name__ == '__main__':
    main()
