from typing import Dict, List

from hash_tree.node import Node
from utils_classes import SequenceCandidate, Item, Sequence
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
        print(f"leaf({self.depth})={self.candidates}")

