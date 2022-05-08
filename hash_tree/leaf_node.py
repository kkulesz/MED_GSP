from typing import List

from data_classes.sequence_candidate import SequenceCandidate
from data_classes.item import Item
from hash_tree.node import Node
from consts import LEAF_CAPACITY


class LeafNode(Node):
    def __init__(self, depth):
        super().__init__(depth)
        self.candidates: List[SequenceCandidate] = []
        self.flattened: List[List[Item]] = []

    def add(self, candidate: SequenceCandidate):
        flattened = candidate.flatten()
        if not True in (f == flattened for f in self.flattened):
            self.flattened.append(flattened)
        self.candidates.append(candidate)

    def exceeds_after_add(self, candidate: SequenceCandidate) -> bool:
        flattened = candidate.flatten()
        contains = True in (f == flattened for f in self.flattened)
        return not contains and len(self.flattened) == LEAF_CAPACITY

    def print(self):
        print("  " * self.depth + f"leaf({self.depth})={self.candidates}")
