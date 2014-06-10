import unittest
import sys
max_int = sys.maxint
min_int = -max_int - 1


class Node(object):
    def __init__(self, value, left, right):
        self.left = left
        self.right = right
        self.value = value

    def __repr__(self):
        return 'Node %s' % self.value


class TreeState(object):

    def __init__(
        self,
        node,
        largest_subtree,
        largest_subtree_length,
        min_value,
        max_value,
        is_bst
    ):
        self.node = node
        self.largest_subtree = largest_subtree
        self.largest_subtree_length = largest_subtree_length
        self.min_value = min_value
        self.max_value = max_value
        self.is_bst = is_bst

    def copy_with_different_bst(self, new_bst):
        return TreeState(
            self.node,
            self.largest_subtree,
            self.largest_subtree_length,
            self.min_value,
            self.max_value,
            new_bst
        )


def largest_subtree(tree):
    state = TreeState(tree, None, None, None, None, None)
    return largest_subtree_helper(state).largest_subtree


def largest_subtree_helper(tree_state):
    node = tree_state.node

    if node is None:
        return TreeState(None, None, 0, None, None, True)

    left_tree_state = largest_subtree_helper(
        TreeState(node.left, None, None, None, None, None)
    )
    right_tree_state = largest_subtree_helper(
        TreeState(node.right, None, None, None, None, None)
    )

    if left_tree_state.is_bst and right_tree_state.is_bst:
        is_node_in_between = is_node_between(left_tree_state, right_tree_state, node)
        if is_node_in_between:
            return TreeState(
                node,
                node,
                left_tree_state.largest_subtree_length + right_tree_state.largest_subtree_length + 1,
                left_tree_state.min_value if left_tree_state.min_value is not None else node.value,
                right_tree_state.max_value if right_tree_state.max_value is not None else node.value,
                True
            )

    if left_tree_state.largest_subtree_length > right_tree_state.largest_subtree_length:
        return left_tree_state.copy_with_different_bst(False)
    else:
        return right_tree_state.copy_with_different_bst(False)

def is_node_between(left_state, right_state, node):
    left_max_value = left_state.max_value if left_state.max_value else min_int
    right_min_value = right_state.min_value if right_state.min_value else max_int
    return left_max_value < node.value < right_min_value


class LargestSubtreeTest(unittest.TestCase):

    def test_single_node(self):
        node = Node(1, None, None)
        self.assertEqual(largest_subtree(node), node)

    def test_two_nodes(self):
        node = Node(
            1,
            Node(0, None, None),
            None
        )
        self.assertEqual(largest_subtree(node), node)

    def test_non_bst(self):
        child = Node(1, None, None)
        node = Node(
            0,
            child,
            None
        )
        self.assertEqual(largest_subtree(node), child)

    def test_large_bst(self):
        little_guy = Node(
            2,
            Node(0, None, None),
            Node(8, None, None)
        )
        thing = Node(
            15,
            Node(
                10,
                Node(5, None, None),
                Node(
                    7,
                    little_guy,
                    Node(
                        5,
                        Node(3, None, None),
                        None
                    )
                )
            ),
            Node(20, None, None)
        )
        self.assertEqual(largest_subtree(thing), little_guy)

if __name__ == '__main__':
    unittest.main()
