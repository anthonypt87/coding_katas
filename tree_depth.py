"""Get tree depth from tree"""
import unittest


class Tree(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children


def recursive_max_length(tree):
    if not tree.children:
        return 1
    else:
        return 1 + max(
            max_length(child) for child in tree.children
        )


def max_length(tree):
    current_depth_and_nodes = [(tree, 1)]
    final_lengths = []
    for node, depth in current_depth_and_nodes:
        if not node.children:
            final_lengths.append(depth)
            continue

        for child in node.children:
            current_depth_and_nodes.append(
                (child, (depth + 1))
            )
    return max(final_lengths)


class MaxLengthTests(unittest.TestCase):

    def test_length_one(self):
        node = Tree('a', [])
        assert max_length(node) == 1

    def test_length_2(self):
        node = Tree('a', [Tree('b', [])])
        assert max_length(node) == 2

    def test_length_3(self):
        node = Tree(
            'a', [
                Tree(
                    'b', [
                        Tree('d', [])
                    ]
                ),
                Tree('c', [])
            ]
        )
        assert max_length(node) == 3

if __name__ == '__main__':
     unittest.main()
