from typing import List

from utils_classes import SequenceCandidate, Item, Element
from hash_tree.hash_tree import HashTree


def convert_to_candidates(ints: List[List[List[int]]]) -> List[SequenceCandidate]:
    result = []
    for c in ints:
        elements = []
        for el in c:
            items = []
            for it in el:
                items.append(Item(it))
            elements.append(Element(items))
        result.append(SequenceCandidate(elements))
    return result


if __name__ == '__main__':
    input_seqs = [
        [
            [1], [2], [3]
        ],
        [
            [1, 2], [3]
        ],
        [
            [1], [2, 3]
        ],
        [
            [1, 2, 3]
        ]
    ]
    input_candidates = convert_to_candidates(input_seqs)

    tree = HashTree(input_candidates)
    tree.print()
