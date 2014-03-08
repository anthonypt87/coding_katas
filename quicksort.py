import unittest


def quicksort(numbers):
    if len(numbers) <= 1:
        return numbers

    pivot = numbers[0]

    less_than = []
    same_as = []
    greater_than = []

    for number in numbers:
        if number < pivot:
            less_than.append(number)
        elif number == pivot:
            same_as.append(number)
        else:
            greater_than.append(number)

    return quicksort(less_than) + same_as + quicksort(greater_than)


class QuickSortTest(unittest.TestCase):

    def test_single_number(self):
        self.assertEqual(quicksort([1]), [1])

    def test_two_numbers_out_of_order(self):
        self.assertEqual(quicksort([3, 1]), [1, 3])

    def test_three_numbers(self):
        self.assertEqual(quicksort([3, 1, 2]), [1, 2, 3])


if __name__ == '__main__':
    unittest.main()
