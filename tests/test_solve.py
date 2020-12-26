import unittest

import yaml

from tubes.model import Game
from tubes.solve import solve


class TestSolve(unittest.TestCase):
    def test_solve(self):
        with open('fixtures/lvl3.yml') as file:
            config = yaml.safe_load(file)
        game = Game(config)
        moves = solve(game)
        for move in moves:
            game._push_move(*move)
        self.assertTrue(game._solved)


if __name__ == '__main__':
    unittest.main()
