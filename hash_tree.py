from __future__ import annotations
from typing import Dict, List
from abc import ABC, abstractmethod

from utils_classes import *
from consts import MODULO_VALUE, LEAF_CAPACITY, WINDOW_SIZE, MAX_GAP


def hash_function(item: Item) -> int:
    return item.data % MODULO_VALUE


class HashTree:
    def __init__(self, candidates: List[SequenceCandidate]):
        self.root: InteriorNode = InteriorNode(depth=0)
        self.candidates: Set[SequenceCandidate] = set()
        self._create(candidates)

    def _create(self, candidates: List[SequenceCandidate]):
        for c in candidates:
            if c not in self.candidates:
                self._add_sequence(c)
                self.candidates.add(c)
        # print(self.candidates)

    def count_support(self, data_sequences: List[Sequence]) -> List[Tuple[SequenceCandidate, int]]:
        supports = dict.fromkeys(self.candidates, 0)
        for data_seq in data_sequences:
            possible_leaves: Set[LeafNode] = set()
            for i in range(len(data_seq)):
                item, its_time = data_seq[i]
                self.root.gather_leaves(data_seq, item, its_time, possible_leaves)
            for leaf in possible_leaves:
                for candidate in leaf.candidates:
                    if candidate.is_supported_by(data_seq):
                        supports[candidate] += 1

        return [(candidate, supp_val) for candidate, supp_val in supports.items()]

    def _add_sequence(self, candidate: SequenceCandidate):
        self.root.add(candidate)

    def print(self):
        self.root.print()


class Node(ABC):
    def __init__(self, depth):
        self.depth = depth

    @abstractmethod
    def add(self, candidate: SequenceCandidate):
        pass

    @abstractmethod
    def print(self):
        pass


class InteriorNode(Node):
    def __init__(self, depth):
        super().__init__(depth)
        self.children: List[Optional[Node]] = [None] * MODULO_VALUE

    def add(self, candidate: SequenceCandidate):
        flattened = candidate.flatten()
        hash_value = hash_function(flattened[self.depth])
        node = self.children[hash_value]
        if isinstance(node, LeafNode):
            if node.exceeds_after_add(candidate):
                new_interior = InteriorNode(self.depth + 1)
                for c in node.candidates:
                    new_interior.add(c)
                new_interior.add(candidate)
                self.children[hash_value] = new_interior
            else:
                node.add(candidate)

        elif isinstance(node, InteriorNode):
            node.add(candidate)

        else:
            leaf = LeafNode(self.depth + 1)
            leaf.add(candidate)
            self.children[hash_value] = leaf

    def gather_leaves(
            self,
            data_seq: Sequence,
            item: Item,
            time: int,
            supports: Set[LeafNode]
    ):
        for idx in range(len(data_seq)):
            it, its_time = data_seq[idx]
            if item == it and time == its_time:
                continue
            if time - WINDOW_SIZE <= its_time <= time + max(WINDOW_SIZE, MAX_GAP):
                hash_value = hash_function(it)
                node = self.children[hash_value]
                if isinstance(node, InteriorNode):
                    node.gather_leaves(data_seq, it, time, supports)
                elif isinstance(node, LeafNode):
                    supports.add(node)

    def print(self):
        print(f"Interior node depth={self.depth}")
        for n in self.children:
            if isinstance(n, Node):
                n.print()


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

    def count_support(
            self,
            data_seq: Sequence,
            supports: Dict[SequenceCandidate, int]
    ):
        for candidate in self.candidates:
            if candidate.is_supported_by(data_seq):
                supports[candidate] += 1

    def print(self):
        print(f"leaf({self.depth})={self.candidates}")


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
