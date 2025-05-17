from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Node:
    id: int
    children: list[Node]


tree_sample = Node(
    1,
    [
        Node(
            2,
            [
                Node(
                    5,
                    [
                        Node(9, []),
                        Node(10, []),
                    ],
                ),
                Node(6, []),
            ],
        ),
        Node(3, []),
        Node(
            4,
            [
                Node(
                    7,
                    [
                        Node(11, []),
                        Node(12, []),
                    ],
                ),
                Node(8, []),
            ],
        ),
    ],
)


def breadth_first_search(id: int, tree: Node):
    if tree.id == id:
        return tree

    else:
        return breadth_first_search


# continue
