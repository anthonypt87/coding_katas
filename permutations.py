"""Given a string, print all it's permutations using its letters"""
from collections import namedtuple
import unittest

State = namedtuple('State', 'string_so_far letters_left')


def permutation(string):
    states = [State('', string)]

    result = []
    while states:
        state = states.pop()

        if not state.letters_left:
            result.append(state.string_so_far)
            continue

        for i in range(len(state.letters_left)):
            new_string_so_far = state.string_so_far + state.letters_left[i]
            new_letters_left = remove_character_at_position(
                state.letters_left,
                i
            )
            states.append(
                State(
                    new_string_so_far,
                    new_letters_left
                )
            )

    return result


def remove_character_at_position(string, position):
    return string[:position] + string[position + 1:]


class PermutationTest(unittest.TestCase):

    def test_single_item(self):
        self.assertEqual(
            permutation('a'),
            ['a']
        )

    def test_two_letter_string(self):
        self.assertEqual(
            permutation('ab'),
            ['ba', 'ab']
        )

    def test_dupes(self):
        self.assertEqual(
            permutation('aa'),
            ['aa', 'aa']
        )

    def test_three(self):
        self.assertEqual(
            sorted(permutation('abc')),
            sorted(['abc', 'acb', 'bca', 'bac', 'cab', 'cba'])
        )


class RemoveCharacterAtPositionTest(unittest.TestCase):
    def test_remove_character_at_position(self):
        self.assertEqual(
            remove_character_at_position('abc', 1),
            'ac'
        )


if __name__ == '__main__':
    unittest.main()
