import unittest


def count_islands(island_map):
    island_count = 0
    explored_positions = set()
    for y in range(len(island_map)):
        for x in range(len(island_map[y])):

            position = (y, x)
            value = island_map[y][x]

            if position in explored_positions:
                continue

            if value == 'X':
                island_coordinates = get_all_island_coordinates(
                    position,
                    island_map
                )
                island_count += 1
                explored_positions.update(island_coordinates)
            else:
                explored_positions.add(position)

    return island_count


def get_all_island_coordinates(position, island_map):
    island_coordinates = set()

    positions_to_explore = [position]
    already_explored = set()
    while True:
        if not positions_to_explore:
            break
        position = positions_to_explore.pop()
        if position in already_explored:
            continue
        already_explored.add(position)
        if island_map[position[0]][position[1]] == 'O':
            continue
        else:
            island_coordinates.add(position)
            for neighbor in get_neighbors(
                position,
                len(island_map),
                len(island_map[0])
            ):
                positions_to_explore.append(neighbor)
    return island_coordinates


def get_neighbors(position, max_y, max_x):
    directions = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    new_positions = []
    for direction in directions:
        new_positions.append((
            direction[0] + position[0],
            direction[1] + position[1]
        ))

    return [
        pos for pos in new_positions if max_y > pos[0] >= 0 and
        max_x > pos[1] >= 0
    ]


class IslandCounterTest(unittest.TestCase):

    def test_single_element(self):
        self._test_island_count([['X']], 1)

    def _test_island_count(self, islands, expected_count):
        self.assertEqual(count_islands(islands), expected_count)

    def test_no_things(self):
        self._test_island_count([['O']], 0)

    def test_one_x_with_os(self):
        self._test_island_count([['O'], ['X']], 1)

    def test_merge_xes(self):
        self._test_island_count([['X'], ['X']], 1)

    def test_complicated(self):
        self._test_island_count([['X', 'X', 'O'], ['X', 'O', 'X']], 2)


if __name__ == '__main__':
    unittest.main()
