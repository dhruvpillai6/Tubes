from collections import Counter, defaultdict, namedtuple
from itertools import permutations

legal_move = namedtuple('legal_move', ['coming_from', 'to'])
move = namedtuple('move', ['coming_from', 'color', 'num_slots', 'from_slots',
                           'going_to', 'to_slots'])


class Color:
    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return f'<Color: {self.color}>'

    def __eq__(self, other):
        return self.color == other.color

    def __hash__(self):
        return hash(self.color)

    def __len__(self):
        return len(self.color)


class Tube:
    def __init__(self, input=None):
        self.first = None
        self.second = None
        self.third = None
        self.fourth = None
        self._slots = [item for item in self]
        self._id = None
        if type(input) == list and len(input) == 4:
            for i, element in enumerate(self):
                if input[i] is not None:
                    self.__setattr__(element, Color(input[i]))

    def __iter__(self):
        yield from [item for item in self.__dir__() if not item.startswith('_')]

    def __repr__(self):
        yield from (f'|  {self.__getattribute__(slot)} |' for slot in self)

    def __str__(self):
        return '\n'.join(f'| {self.__getattribute__(slot)} | - {slot}' for slot in self)

    def __eq__(self, other):
        return all(self._color(slot) == other._color(slot) for slot in self)

    def __hash__(self):
        return hash(tuple((self._color(slot) for slot in self)))

    def _iter_slots(self):
        yield from [self.__getattribute__(item) for item in self.__dir__() if not
        item.startswith('_')]

    @property
    def _empty_slots(self):
        return [slot for slot in self if not self.__getattribute__(slot)]

    @property
    def _is_full(self):
        return all(self._iter_slots())

    @property
    def _is_empty(self):
        return all([item is None for item in self._iter_slots()])

    @property
    def _first_full(self):
        for item in self:
            if self.__getattribute__(item):
                return item
        return self._slots[-1]

    @property
    def _color_to_pour(self):
        return self.__getattribute__(self._first_full)

    @property
    def _slots_to_pour(self):
        if self._is_empty:
            return []
        idx_start = self._slots.index(self._first_full)
        slots_to_pour = [self._first_full]

        if idx_start == len(self._slots):
            return slots_to_pour
        else:
            for slot in self._slots[idx_start:]:
                color = self._color(slot)
                idx = self._slots.index(slot)
                if idx == len(self._slots) - 1:
                    break
                next_idx = idx + 1
                next_color = self._color(self._slots[next_idx])
                if color != next_color:
                    break
                else:
                    slots_to_pour.append(self._slots[next_idx])
        return slots_to_pour


    @property
    def _last_empty(self):
        if self._is_full:
            return None
        last = self._slots[-1]
        for item in self:
            if self._color(item) is None:
                last = item
            elif item:
                return last
        return last

    def _color(self, slot):
        return self.__getattribute__(slot)

    @property
    def _solved(self):
        return len({color for color in self._iter_slots()}) == 1

    @property
    def _colors(self):
        return {color for color in self._iter_slots() if color is not None}

    def _pour_in(self, from_tube, slots_over=None):
        if type(from_tube) is not Tube:
            raise TypeError(f'from_tube is of type {type(from_tube)} when it should '
                            f'be {type(Tube)}')
        elif self._is_full:
            raise RuntimeError('Tube is full')
        elif from_tube._is_empty:
            raise RuntimeError('from_tube is empty')
        elif not self._is_empty:
            if from_tube._color_to_pour != self._color_to_pour:
                raise RuntimeError('colors are not the same')
        slots = slots_over if slots_over else from_tube._slots_to_pour
        for slot in slots:
            if self._is_full:
                raise RuntimeError('Tube is full')
            self.__setattr__(self._last_empty, from_tube._color(slot))
            from_tube.__setattr__(slot, None)

    def _pour_out(self, to_tube):
        raise NotImplementedError


class Game:
    def __init__(self, input):
        num = 1
        self._tubes = []
        for tube in input:
            tube_attr = f'tube_{num}'
            self.__setattr__(tube_attr, Tube(input[tube]))
            self.__getattribute__(tube_attr)._id = num
            self._tubes.append(num)
            num += 1
        self._num_tubes = num
        self._slots = self.tube_1._slots
        self._colors = set()
        for tube in self._iter_tubes():
            self._colors = self._colors.union(tube._colors)
        self._max_len_color = max(self._colors, key=len)
        self._moves = []
        self._legal_moves = {}
        #TODO: valdiate same number of slots per tube, validate multiples of colors
        # is correct

    def __hash__(self):
        return hash(tuple(hash(tube) for tube in self._iter_tubes()))

    @property
    def _color_counter(self):
        colors = []
        for tube in self._iter_tubes():
            for color in tube._iter_slots():
                if color is not None:
                    colors.append(color)
        return Counter(colors)

    @property
    def _solved(self):
        return all([tube._solved for tube in self._iter_tubes()])

    @property
    def _color_score_raw(self):
        colors = defaultdict(int)
        for tube in self._iter_tubes():
            prev = None
            current = None
            nxt = None
            score = 1
            for i, color in enumerate(tube._iter_slots()):
                if color is None:
                    prev = current
                    continue
                if color is not None:
                    current = color
                    if prev is None:
                        if i == len(self._slots) - 1:
                            colors[current] += score
                            continue
                        else:
                            prev = current
                            continue
                    if current != prev:
                        colors[prev] += score
                        score += 1
                        prev = current
                        if i == len(self._slots) - 1:
                            colors[current] += score
                    elif current == prev and i == len(self._slots) - 1:
                        colors[current] += score
        return colors

    @property
    def _color_score(self):
        return sum(self._color_score_raw.values())

    def __iter__(self):
        yield from [tube for tube in self.__dir__() if not tube.startswith('_')]

    def _iter_tubes(self):
        yield from [self.__getattribute__(tube) for tube in self]

    def __str__(self):
        print_list = [self._color_score, self._color_score_raw]
        max_len = 9 + len(self._max_len_color)
        for slot in self._slots:
            row_list = []
            row = ''
            for tube in self._iter_tubes():
                row_list.append(tube._color(slot))
            for color in row_list:
                pad_len = (max_len - len(str(color))) // 2
                left_pad_len = pad_len
                right_pad_len = pad_len
                if pad_len == 0 and (max_len - len(str(color))) > 0:
                    right_pad_len += 1
                entry = f'|{" "  * left_pad_len}{str(color)}{" " * right_pad_len}|'
                row = f'{row}{entry}'
            # new_row = '   |   '.join(str(color) for color in row_list)
            # new_row = f'|   {new_row}   |'
            print_list.append(row)
        return '\n'.join(str(value) for value in print_list)

    def __repr__(self):
        return f'<Game>'

    def _retrieve_tube(self, identity):
        for tube in self._iter_tubes():
            if tube._id == identity:
                return tube
        return None

    def _forecast(self):
        game1 = self
        hash1 = hash(self)
        self._legal_moves = {}
        combs = permutations(self._tubes, 2)
        for comb in combs:
            try:
                self._push_move(comb[0], comb[1])
            except RuntimeError:
                continue
            score = self._color_score
            self._pop_move()
            hash2 = hash(self)
            if hash1 != hash2:
                pass
                # print(comb)
                # raise ValueError
            self._legal_moves[comb] = score
        if not self._legal_moves:
            raise InterruptedError('No Legal Moves Left')
        return 0

    def _push_move(self, from_tube_identity, to_tube_identity):
        from_tube = self._retrieve_tube(from_tube_identity)
        to_tube = self._retrieve_tube(to_tube_identity)
        if from_tube._is_empty or to_tube._is_full:
            raise RuntimeError
        color = from_tube._color_to_pour
        num_slots = min(len(from_tube._slots_to_pour), len(to_tube._empty_slots))
        from_slots = from_tube._slots_to_pour
        while len(from_slots) > num_slots:
            del from_slots[-1]
        slots_filled = [to_tube._last_empty]
        idx = to_tube._slots.index(to_tube._last_empty)
        for i in range(num_slots):
            if i == 0:
                continue
            if idx < 0:
                raise RuntimeError
            idx = idx - 1
            slot = to_tube._slots[idx]
            slots_filled.append(slot)

        cur_move = move(from_tube_identity, color, num_slots, from_slots,
                        to_tube_identity, slots_filled)
        self._moves.append(cur_move)
        to_tube._pour_in(from_tube, from_slots)
        # self._legal_moves = {}
        return cur_move

    def _pop_move(self):
        if not self._moves:
            print('no moves made!')
            return 1
        else:
            undo_move = self._moves.pop()
            coming_from = self._retrieve_tube(undo_move.coming_from)
            color = undo_move.color
            # num_slots = undo_move.num_slots
            from_slots = undo_move.from_slots
            going_to = self._retrieve_tube(undo_move.going_to)
            to_slots = undo_move.to_slots
            for slot in from_slots:
                coming_from.__setattr__(slot, color)
            for slot in to_slots:
                going_to.__setattr__(slot, None)
            # self._legal_moves = {}
            return 0

if __name__ == '__main__':
    obj1 = Tube([None, None, None, 'blue'])
    obj2 = Tube([None, None, None, 'blue'])
    print(obj1 == obj2)
    print(hash(obj1))
    print(hash(obj2))