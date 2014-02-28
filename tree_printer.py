"""Print all the levels of a tree"""


class Tree(object):
    def __init__(self, value, children):
        self.value = value
        self.children = children


def create_print_tree(tree):
    tree_nodes = [tree]
    to_print = ''
    while tree_nodes:
        to_print += "\n"
        to_print += " ".join([tree_node.value for tree_node in tree_nodes])
        new_tree_nodes = []
        for tree_node in tree_nodes:
            new_tree_nodes.extend(tree_node.children)
        tree_nodes = new_tree_nodes
    return to_print


def test_single():
    test_tree = Tree(
        'a',
        []
    )
    result = create_print_tree(test_tree)
    assert result == "\na"


def test_tree_print():
    test_tree = Tree(
        'a',
        [
            Tree('b', []),
            Tree ('c', [])
        ]
    )
    result = create_print_tree(test_tree)
    assert result == "\na\nb c"

if __name__ == '__main__':
    test_single()
    test_tree_print()
