import unittest

import yaml

from tubes.model import Game, Tube, Color, move


class TestColor(unittest.TestCase):

    def test_repr(self):
        color = Color('blue')
        self.assertEqual('<Color: blue>', repr(color))

    def test_eq(self):
        self.assertTrue(Color('blue') == Color('blue'))
        self.assertEqual(Color('blue'), Color('blue'))

    def test_len(self):
        self.assertEqual(len(Color('blue')), 4)


class TestTube(unittest.TestCase):

    def setUp(self) -> None:
        self.tube_full = Tube(['red', 'green', 'blue', 'yellow'])
        self.tube_three_full = Tube([None, 'green', 'blue', 'yellow'])
        self.tube_half_full = Tube([None, None, 'blue', 'yellow'])
        self.tube_one_full = Tube([None, None, None, 'yellow'])
        self.tube_empty = Tube([None, None, None, None])

    def test_iterate(self):
        items = iter(self.tube_full)
        self.assertEqual('first', next(items))
        self.assertEqual('second', next(items))
        self.assertEqual('third', next(items))
        self.assertEqual('fourth', next(items))
        with self.assertRaises(StopIteration):
            next(items)

    def test_iter_slots(self):
        items = self.tube_full._iter_slots()
        self.assertEqual(Color('red'), next(items))
        self.assertEqual(Color('green'), next(items))
        self.assertEqual(Color('blue'), next(items))
        self.assertEqual(Color('yellow'), next(items))
        with self.assertRaises(StopIteration):
            next(items)

    def test_empty_slots(self):
        empty_slots = self.tube_full._empty_slots
        self.assertEqual([], empty_slots)
        empty_slots = self.tube_half_full._empty_slots
        self.assertEqual(['first', 'second'], empty_slots)
        empty_slots = self.tube_empty._empty_slots
        self.assertEqual(['first', 'second', 'third', 'fourth'], empty_slots)

    def test_is_full(self):
        self.assertTrue(self.tube_full._is_full)
        self.assertFalse(self.tube_three_full._is_full)
        self.assertFalse(self.tube_half_full._is_full)
        self.assertFalse(self.tube_one_full._is_full)
        self.assertFalse(self.tube_empty._is_full)

    def test_is_empty(self):
        self.assertFalse(self.tube_full._is_empty)
        self.assertFalse(self.tube_three_full._is_empty)
        self.assertFalse(self.tube_half_full._is_empty)
        self.assertFalse(self.tube_one_full._is_empty)
        self.assertTrue(self.tube_empty._is_empty)

    def test_first_full(self):
        self.assertEqual('first', self.tube_full._first_full)
        self.assertEqual('second', self.tube_three_full._first_full)
        self.assertEqual('third', self.tube_half_full._first_full)
        self.assertEqual('fourth', self.tube_one_full._first_full)
        self.assertEqual('fourth', self.tube_empty._first_full)

    def test_color_to_pour(self):
        self.assertEqual(Color('red'), self.tube_full._color_to_pour)
        self.assertEqual(Color('green'), self.tube_three_full._color_to_pour)
        self.assertEqual(Color('blue'), self.tube_half_full._color_to_pour)
        self.assertEqual(Color('yellow'), self.tube_one_full._color_to_pour)
        self.assertEqual(None, self.tube_empty._color_to_pour)

    def test_slots_to_pour(self):
        self.assertEqual(['first'], self.tube_full._slots_to_pour)
        self.assertEqual(['second'], self.tube_three_full._slots_to_pour)
        self.assertEqual(['third'], self.tube_half_full._slots_to_pour)
        self.assertEqual(['fourth'], self.tube_one_full._slots_to_pour)
        self.assertEqual([], self.tube_empty._slots_to_pour)

        tube = Tube(['red', 'red', 'blue', 'yellow'])
        self.assertEqual(['first', 'second'], tube._slots_to_pour)
        tube = Tube(['red', 'red', 'red', 'yellow'])
        self.assertEqual(['first', 'second', 'third'], tube._slots_to_pour)
        tube = Tube(['red', 'red', 'red', 'red'])
        self.assertEqual(['first', 'second', 'third', 'fourth'], tube._slots_to_pour)

    def test_last_empty(self):
        self.assertEqual(None, self.tube_full._last_empty)
        self.assertEqual('first', self.tube_three_full._last_empty)
        self.assertEqual('second', self.tube_half_full._last_empty)
        self.assertEqual('third', self.tube_one_full._last_empty)
        self.assertEqual('fourth', self.tube_empty._last_empty)

    def test_color(self):
        self.assertEqual(Color('red'), self.tube_full._color('first'))
        self.assertEqual(Color('green'), self.tube_three_full._color('second'))
        self.assertEqual(Color('blue'), self.tube_half_full._color('third'))
        self.assertEqual(Color('yellow'), self.tube_one_full._color('fourth'))

    def test_solved(self):
        self.assertFalse(self.tube_full._solved)
        self.assertFalse(self.tube_three_full._solved)
        self.assertFalse(self.tube_half_full._solved)
        self.assertFalse(self.tube_one_full._solved)
        self.assertTrue(self.tube_empty._solved)
        self.assertTrue(Tube(['red', 'red', 'red', 'red'])._solved)

    def test_colors(self):
        self.assertEqual(
            {Color('red'), Color('green'), Color('blue'), Color('yellow')},
            self.tube_full._colors
        )
        self.assertEqual(
            {Color('green'), Color('blue'), Color('yellow')},
            self.tube_three_full._colors
        )
        self.assertEqual(
            {Color('blue'), Color('yellow')},
            self.tube_half_full._colors
        )
        self.assertEqual(
            {Color('yellow')},
            self.tube_one_full._colors
        )
        self.assertEqual(
            set(),
            self.tube_empty._colors)
        self.assertEqual(
            {Color('red'), Color('blue'), Color('yellow')},
            Tube(['red', 'red', 'blue', 'yellow'])._colors
        )
        self.assertEqual(
            {Color('red'), Color('yellow')},
            Tube(['red', 'red', 'red', 'yellow'])._colors
        )
        self.assertEqual(
            {Color('red')},
            Tube(['red', 'red', 'red', 'red'])._colors
        )

    def test_pour_in(self):
        # Argument must be of type `Tube`
        with self.assertRaises(TypeError):
            self.tube_half_full._pour_in(None)
        # Cannot pour into full tube
        with self.assertRaises(RuntimeError):
            self.tube_full._pour_in(self.tube_half_full)
        # Cannot pour from an empty tube
        with self.assertRaises(RuntimeError):
            self.tube_half_full._pour_in(self.tube_empty)
        # Cannot pour if top colors mismatch
        with self.assertRaises(RuntimeError):
            tube_1 = Tube([None, None, None, 'blue'])
            tube_2 = Tube([None, None, 'green', 'blue'])
            tube_1._pour_in(tube_2)

        tube_1 = Tube([None, None, None, 'green'])
        tube_2 = Tube([None, None, 'green', 'blue'])
        tube_1._pour_in(tube_2)
        self.assertEqual(Tube([None, None, 'green', 'green']), tube_1)
        self.assertEqual(Tube([None, None, None, 'blue']), tube_2)

        tube_1 = Tube([None, None, 'green', 'green'])
        tube_2 = Tube([None, None, 'green', 'green'])
        tube_1._pour_in(tube_2)
        self.assertEqual(Tube(['green', 'green', 'green', 'green']), tube_1)
        self.assertEqual(Tube([None, None, None, None]), tube_2)

        tube_1 = Tube([None, None, None, None])
        tube_2 = Tube(['green', 'green', 'green', 'green'])
        tube_1._pour_in(tube_2)
        self.assertEqual(Tube(['green', 'green', 'green', 'green']), tube_1)
        self.assertEqual(Tube([None, None, None, None]), tube_2)


class TestGame(unittest.TestCase):
    def setUp(self) -> None:
        with open('fixtures/lvl3.yml') as file:
            config = yaml.safe_load(file)
        self.game = Game(config)

    def test_parse_config(self):
        # self.assertEqual(self.game._num_tubes, len(self.game._tubes))  # TODO: Use me
        self.assertEqual(self.game._num_tubes, 4)  # TODO: This is an OBO error
        self.assertEqual([1, 2, 3], self.game._tubes)

        self.assertTrue(hasattr(self.game, 'tube_1'))
        self.assertIsInstance(self.game.tube_1, Tube)
        self.assertEqual(Tube(['blue', 'blue', 'green', 'blue']), self.game.tube_1)
        self.assertTrue(hasattr(self.game, 'tube_2'))
        self.assertIsInstance(self.game.tube_2, Tube)
        self.assertEqual(Tube(['blue', 'green', 'green', 'green']), self.game.tube_2)
        self.assertTrue(hasattr(self.game, 'tube_3'))
        self.assertIsInstance(self.game.tube_3, Tube)
        self.assertEqual(Tube([]), self.game.tube_3)

        self.assertEqual({Color('blue'), Color('green')}, self.game._colors)

    def test_color_counter(self):
        counter = self.game._color_counter
        self.assertEqual(4, counter[Color('blue')])
        self.assertEqual(4, counter[Color('green')])

    def test_solved(self):
        self.assertFalse(self.game._solved)
        with open('fixtures/game_solved.yml') as file:
            config = yaml.safe_load(file)
        game_solved = Game(config)
        self.assertTrue(game_solved._solved)

    def test_color_score_raw(self):
        self.assertEqual({Color('green'): 4, Color('blue'): 5},
                         dict(self.game._color_score_raw))

    def test_color_score(self):
        self.assertEqual(9, self.game._color_score)

    def test_iterate(self):
        items = iter(self.game)
        self.assertEqual('tube_1', next(items))
        self.assertEqual('tube_2', next(items))
        self.assertEqual('tube_3', next(items))
        with self.assertRaises(StopIteration):
            next(items)

    def test_iter_tubes(self):
        items = self.game._iter_tubes()
        self.assertEqual(Tube(['blue', 'blue', 'green', 'blue']), next(items))
        self.assertEqual(Tube(['blue', 'green', 'green', 'green']), next(items))
        self.assertEqual(Tube([]), next(items))
        with self.assertRaises(StopIteration):
            next(items)

    def test_str(self):
        expected = '\n'.join([
            "9",
            "defaultdict(<class 'int'>, {<Color: blue>: 5, <Color: green>: 4})",
            "|<Color: blue> ||<Color: blue> ||     None     |",
            "|<Color: blue> ||<Color: green>||     None     |",
            "|<Color: green>||<Color: green>||     None     |",
            "|<Color: blue> ||<Color: green>||     None     |",
        ])
        self.assertEqual(expected, str(self.game))

    def test_repr(self):
        self.assertEqual('<Game>', repr(self.game))

    def test_retrieve_tube(self):
        self.assertEqual(Tube(['blue', 'blue', 'green', 'blue']),
                         self.game._retrieve_tube(1))
        self.assertEqual(Tube(['blue', 'green', 'green', 'green']),
                         self.game._retrieve_tube(2))
        self.assertEqual(Tube([]), self.game._retrieve_tube(3))

    def test_forecast(self):
        self.assertEqual({}, self.game._legal_moves)
        self.assertEqual(0, self.game._forecast())
        self.assertEqual({(1, 3): 7, (2, 3): 8}, self.game._legal_moves)

        with open('fixtures/game_no_legal_moves.yml') as file:
            config = yaml.safe_load(file)
        game = Game(config)
        with self.assertRaises(InterruptedError):
            game._forecast()

    def test_push_move(self):
        with open('fixtures/game_simple_transfer.yml') as file:
            config = yaml.safe_load(file)
        game = Game(config)
        expected_move = move(coming_from=1, from_slots=['third'],
                             going_to=2, to_slots=['second'],
                             num_slots=1, color=Color('green'))
        self.assertEqual([], game._moves)
        self.assertEqual(expected_move, game._push_move(1, 2))
        self.assertEqual(Tube([None, None, None, 'blue']), game.tube_1)
        self.assertEqual(Tube([None, 'green', 'green', 'green']), game.tube_2)
        self.assertEqual([expected_move], game._moves)

    def test_pop_move(self):
        with open('fixtures/game_simple_transfer_complete.yml') as file:
            config = yaml.safe_load(file)
        game = Game(config)
        self.assertEqual(1, game._pop_move())
        game._moves = [move(coming_from=1, from_slots=['third'],
                            going_to=2, to_slots=['second'],
                            num_slots=1, color=Color('green'))]
        self.assertEqual(0, game._pop_move())
        self.assertEqual(Tube([None, None, 'green', 'blue']), game.tube_1)
        self.assertEqual(Tube([None, None, 'green', 'green']), game.tube_2)
        self.assertEqual([], game._moves)


if __name__ == '__main__':
    unittest.main()
