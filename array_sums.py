import unittest


def find_pair_sums(numbers, k):
    numbers = set(numbers)

    output = set()
    for number in numbers:
        target_number = k - number
        if target_number in numbers:
            output.add(
                (
                    min(number, target_number),
                    max(number, target_number)
                )
            )

    return output


class FindPairsSumsTest(unittest.TestCase):

    def test_find_pairs(self):
        self.assertEqual(find_pair_sums([0, 1], 1), set([(0, 1)]))
        self.assertEqual(
            find_pair_sums([0, 1, 2, 3], 3),
            set(
                [
                    (1, 2),
                    (0, 3),
                ]
            )
        )


if __name__ == '__main__':
    unittest.main()
